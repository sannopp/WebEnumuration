# url= https://3kh0.github.io/dinosaur-game/
import time
import pyautogui
from PIL import ImageGrab


def hit(key):
    pyautogui.keyDown(key)


def is_colide():
    for i in range(680, 730):
        for j in range(530, 540):
            if data[i, j] < 90:
                return True
    return False


if __name__ == '__main__':
    print('dinogame in 3 second...')
    time.sleep(3)
    hit('up')
    while True:
        image = ImageGrab.grab().convert('L')
        data = image.load()
        if is_colide():
            hit('up')
        # for i in range(690, 720):
        #     for j in range(530, 540):
        #         data[i, j] = 0
        # image.show()
        # break
        # image.show()

