from pynput import keyboard
import time

log = []


def on_press(key):
    try:
        s = f'{key.char}           pressed  {time.asctime(time.gmtime())}'
        print(s)
    except AttributeError:
        s = f'{key} pressed  {time.asctime(time.gmtime())}'
        print(s)
    log.append(s)

def on_release(key):
    try:
        s = f'{key.char}           released  {time.asctime(time.gmtime())}'
        print(s)
    except AttributeError:
        s = f'{key} released  {time.asctime(time.gmtime())}'
        print(s)
    log.append(s)
    if key == keyboard.Key.esc:
        # Stop listener
        return False


# Collect events until
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
with open('log.txt', 'w') as f:
    for i in log:
        f.write(f'{i} \n')
