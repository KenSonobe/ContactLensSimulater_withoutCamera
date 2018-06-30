from classes import Contact

import cv2 as cv


def contact(src):
    con = Contact(cv.imread('rei1.png', -1))
    con.resize(src.left.length, src.right.length)

    set(src.result, src.h, src.w, src.left, con.left, src.skin)
    set(src.result, src.h, src.w, src.right, con.right, src.skin)

    return


def set(img, h, w, eye, con, skin):
    control = eye.bright / 255
    for y in range(con.length):
        for x in range(con.length):
            img_y = int(eye.y - con.length / 2 + y)
            img_x = int(eye.x - con.length / 2 + x)
            if img_y > 0 and img_y < h and img_x > 0 and img_y < w:
                red = img[img_y, img_x, 2]
                green = img[img_y, img_x, 1]
                blue = img[img_y, img_x, 0]
                if red / (blue + 1) < (skin[2] / (skin[0] * 1.2)) or green < skin[1] / 2:
                    if con.img[y, x] < 100:
                        # 目の色
                        img[img_y, img_x, 0] = ((35 * control) * 4 + img[img_y, img_x, 0]) / 5
                        img[img_y, img_x, 1] = ((55 * control) * 4 + img[img_y, img_x, 1]) / 5
                        img[img_y, img_x, 2] = ((90 * control) * 4 + img[img_y, img_x, 2]) / 5

    return
