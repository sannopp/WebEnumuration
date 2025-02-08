import tkinter
import PIL.Image
import PIL.ImageTk
import cv2
from functools import partial
import threading
import imutils

set_width = 900
set_height = 506

stream = cv2.VideoCapture('Img/run_out.mp4')

def play(s):
    print(f'play {s}')
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + s)
    grabbed, frame1 = stream.read()
    frame1 = imutils.resize(frame1, width=set_width, height=set_height)
    frame1 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame1))
    canvas.image = frame1
    canvas.create_image(0, 0, image=frame1, anchor=tkinter.NW)


window = tkinter.Tk()
window.title('Third Umpire Review')

cv_img = cv2.cvtColor(cv2.imread("Img/wp753589.jpg"), cv2.COLOR_BGR2RGB)

canvas = tkinter.Canvas(window, width=set_width, height=set_height)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
img_on_canvas = canvas.create_image(0, 0, ancho=tkinter.NW, image=photo)
canvas.pack()


def out(s):
    thread = threading.Thread(target=out_check, args=(s, ))
    thread.daemon = 1
    thread.start()
    if s == 0:
        print('Not Out ')
    else:
        print('Out')


def out_check(s1):
    if s1 == 0:
        frame = cv2.cvtColor(cv2.imread("Img/not_out.png"), cv2.COLOR_BGR2RGB)
    else:
        frame = cv2.cvtColor(cv2.imread("Img/out.png"), cv2.COLOR_BGR2RGB)
    # frame = imutils.resize(frame, width=set_width, height=set_height)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    print(s1)
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)


# buttons
btn = tkinter.Button(window, text='<< Previous fast', width=50, command=partial(play, -25))
btn.pack()
btn = tkinter.Button(window, text='<< Previous slow', width=50, command=partial(play, -2))
btn.pack()
btn = tkinter.Button(window, text='>> Next fast', width=50, command=partial(play, 25))
btn.pack()
btn = tkinter.Button(window, text='>> Next slow', width=50, command=partial(play, 2))
btn.pack()
btn = tkinter.Button(window, text='Not Out', width=50, command=partial(out, 0))
btn.pack()
btn = tkinter.Button(window, text='Out', width=50, command=partial(out, 1))
btn.pack()

window.mainloop()
