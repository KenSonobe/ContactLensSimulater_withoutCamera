from classes import Src
from detection import detection
from adjustment import adjustment
from contact import contact

import cv2 as cv


def img_read():
    name = input("\n名前を入力して下さい: ")

    img = cv.imread(name + ".jpg", 1)

    if img is None:
        print("<!> その画像は存在しません <!>")
        src = img_read()
    else:
        src = Src(img, name)

    return src


def img_show(title, img):
    cv.imshow(title, img)
    key = cv.waitKey(0)
    cv.destroyAllWindows()

    return key


# ================================================================
def main():
    src = img_read()

    print("name: {}\n".format(src.name))

    img_show('-FACE-    continue = (Press eny key)', cv.resize(src.img, (540, 720)))

    # 中心判定
    detection(src)

    # 調節
    adjustment(src)

    # コンタクト貼り付け
    contact(src)

    key = img_show('-RESULT-    save = (Press < s >),  end = (Press other key)', cv.resize(src.result, (540, 720)))

    if key == ord('s') or key == ord('S'):
        cv.imwrite("result_" + src.name + ".jpg", src.result)
        print("\n保存しました")

    cv.destroyAllWindows()


# ================================================================

if __name__ == "__main__":
    main()
