#!/usr/bin/env python3

import cv2, numpy, math

sample_space = 5
tolerence = 20

def dist(c_1, c_2):
    return math.sqrt((c_1[0]-c_2[0])**2+(c_1[1]-c_2[1])**2)
def detectBalls(frames):
    frames_circles = []
    for frame in frames:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hist = cv2.equalizeHist(gray)
        blur = cv2.GaussianBlur(hist, (13, 13), cv2.BORDER_DEFAULT)
        height, width = blur.shape[:2]
        minR = round(width/40)
        maxR = round(width/20)
        minDis = round(width/7)
        circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, minDis, param1=14, param2=25, minRadius=minR, maxRadius=maxR)
        if circles is not None:
            circles = numpy.round(circles[0, :]).astype("int")
            frame_circles = []
            for (x, y, r) in circles:
                frame_circles.append((x, y, r))
            frames_circles.append(frame_circles)
    if len(frames_circles) > 1:
        reference_circles = frames_circles[1]
    else:
        return None
    prev_min_dist, score = None, {i:0 for i in range(len(reference_circles))}
    for circles in frames_circles[1:]:
        index = None
        for i, circle in enumerate(reference_circles):
            dist_circles = {(circle, compare_circle): dist(circle, compare_circle) for compare_circle in circles}
            min_dist = min(list(dist_circles.values()))
            if min_dist > tolerence:
                break
            if prev_min_dist == None or min_dist < prev_min_dist:
                prev_min_dist = min_dist
                index = i
        if index != None:
            score[index] += 1
    score = {j: score[j] for j in reversed(sorted(score, key=lambda i: score[i]))}
    if len(score) > 0:
        best_circle = list(score.keys())[0]
        if score[best_circle] > 0:
            return reference_circles[best_circle]
        else:
            return None
    else:
        return None

if __name__ == "__main__":
    video_capture = cv2.VideoCapture(0)
    while cv2.waitKey(1) != 113:
        frames = []
        for _ in range(sample_space):
            ret, frame = video_capture.read()
            if not ret:
                print("Error in Reading the Frame from the Camera")
                continue
            frames.append(frame)
        ball = detectBalls(frames)
        if ball != None:
            cv2.circle(frames[0], (ball[0], ball[1]), ball[2], (0, 255, 0), 2)
            cv2.rectangle(frames[0], (ball[0]-1, ball[1]-1), (ball[0]+1, ball[1]+1), (255, 0, 0), -1)
        cv2.imshow("Ball Detection", frames[0])
    video_capture.release()
    cv2.destroyAllWindows()
