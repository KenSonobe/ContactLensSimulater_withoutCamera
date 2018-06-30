import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


# 黒目検出
def detection(src):
    face_cascade_path = '/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml'
    eye_cascade_path = '/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_eye.xml'

    face_cascade = cv.CascadeClassifier(face_cascade_path)
    eye_cascade = cv.CascadeClassifier(eye_cascade_path)

    cut_img = [0, 0]
    canny_img = [0, 0]

    eyeP = [[0, 0, 0, 0], [0, 0, 0, 0]]

    src_gray = cv.cvtColor(src.img, cv.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(src_gray)

    for x, y, w, h in faces:
        cv.rectangle(src.copy, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = src.copy[y: y + h, x: x + w]
        face_gray = src_gray[y: y + h, x: x + w]

        eyes = eye_cascade.detectMultiScale(face_gray)

        eye_num = 0
        i = 0

        for (ex, ey, ew, eh) in eyes:
            cv.rectangle(face, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

            cut_img[i] = src.img[y + ey:y + ey + eh, x + ex:x + ex + ew]

            if ew > 30 and eh > 30:
                eyeP[eye_num] = [x + ex, y + ey, x + ex + ew, y + ey + eh]
                src_preprocessed = cv.cvtColor(cv.GaussianBlur(cut_img[i], (9, 9), 0), cv.COLOR_BGR2GRAY)
                canny_img[eye_num] = cv.Canny(src_preprocessed, threshold1=90, threshold2=50)

                plt.imshow(cv.cvtColor(canny_img[eye_num], cv.COLOR_GRAY2BGR))
                plt.show()
                cv.waitKey(0)

                eye_num += 1

            if eye_num == 2:
                break

            i += 1

    x, y, length = [0, 0], [0, 0], [0, 0]

    for i in range(2):
        x[i], y[i], length[i] = detection_circle(canny_img, cut_img, i)

    for i in range(2):
        x[i] += eyeP[i][0]
        y[i] += eyeP[i][1]

    if x[0] > x[1]:
        temp_y, temp_x, temp_l = y[0], x[0], length[0]
        y[0], x[0], length[0] = y[1], x[1], length[1]
        y[1], x[1], length[1] = temp_y, temp_x, temp_l

    src.set_eye(y[0], x[0], y[1], x[1], length[0], length[1])

    return


def detection_circle(canny_img, cut_img, i):
    circles = cv.HoughCircles(canny_img[i], cv.HOUGH_GRADIENT, dp=8, minDist=999, minRadius=70, maxRadius=80)

    eye_circles = np.copy(cut_img[i])

    x, y, r = 0, 0, 0
    if circles is not None and len(circles) > 0:

        circles = circles[0]
        for (x, y, r) in circles:
            x, y, r = int(x), int(y), int(r)

            cv.circle(eye_circles, (x, y), r, (255, 255, 0), 4)

        plt.imshow(cv.cvtColor(eye_circles, cv.COLOR_BGR2RGB))
        plt.show()

    return x, y, r
