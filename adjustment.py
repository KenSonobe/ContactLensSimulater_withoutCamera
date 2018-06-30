import cv2 as cv


def adjustment(src):
    bright(src.img, src.left, -1)
    bright(src.img, src.right, 1)

    src.set_skin(skin(src.img, src.left, src.right))

    return


def bright(img, eye, direction):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    value = [0 for i in range(9)]
    for i in range(3):
        for j in range(3):
            idx = int(i * 3 + j)
            value[idx] = hsv[eye.y - 10 + i * 10, eye.x + (int(eye.length / 2) + 20) * direction - 10 + j * 10, 2]

    value.sort()

    eye.set_bright(value[2])

    print(eye.bright)

    return


def skin(img, left, right):
    y = (left.y + right.y) / 2
    x = (left.x + right.x) / 2

    color = [[0 for i in range(3)] for j in range(9)]
    sum = [[0 for i in range(2)] for j in range(9)]

    for i in range(3):
        for j in range(3):
            idx = int(i * 3 + j)
            for k in range(3):
                color[idx][k] = int(img[int(y + (-10 + i * 10)), int(x + (-10 + j * 10)), k])
            sum[idx][0] = color[idx][0] + color[idx][1] + color[idx][2]
            sum[idx][1] = idx

    sum.sort()

    return color[sum[0][1]]
