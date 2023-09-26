#!/usr/bin/env python3

import cv2, numpy                                                                                                                          # Importing cv2 for image processing and numpy for mathematical operations

if __name__ == "__main__":                                                                                                                 # If this program is the main namespace then only run it
    video_capture = cv2.VideoCapture(0)                                                                                                    # Selecting the Camera for Capturing video
    while cv2.waitKey(1) != 113:                                                                                                           # Running the Program till ’q’ is pressed
        ret, original_frame = video_capture.read()                                                                                         # ret -> return True if frame is successfully read, original_frame -> image given by the camera
        if not ret:                                                                                                                        # check if getting the frame is successful or not
            break                                                                                                                          # if not then break
        gray_scale_frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)                                                                # converting the frame to gray scale image
        gray_scale_frame_blurred = cv2.blur(gray_scale_frame, (5, 5))                                                                      # blurring the image to get more accuracy and decrease load on cpu
        balls = cv2.HoughCircles(gray_scale_frame_blurred, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=10, maxRadius=40)    # Detecting circles in the blurred image with some parameters set experimetally for a ball
        if balls is not None:                                                                                                              # checks if there is a ball or not
            balls = numpy.uint8(numpy.around(balls))                                                                                       # converts the float values in the balls matrix to integers (to be specific unsigned integer of 8 bits)
            for ball in balls[0]:                                                                                                          # iterate through the detected balls
                h, k, r = ball[0], ball[1], ball[2]                                                                                        # get the center (h, k) and radius r of the ball detected
                cv2.circle(original_frame, (h, k), r, (0, 255, 0), 2)                                                                      # mark a circle with centre (h, k) and radius r to mark the detected ball
                cv2.circle(original_frame, (h, k), 1, (0, 0, 255), 3)                                                                      # mark a point at the centre of the circle above
        cv2.imshow("Ball Detection", original_frame)                                                                                       # Showing the image with marked balls if found
    video_capture.release()                                                                                                                # Release the Video Capture
    cv2.destroyAllWindows()                                                                                                                # Destroy all the OpenCV windows created by this program during its runtime
