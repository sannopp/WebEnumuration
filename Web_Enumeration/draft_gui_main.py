import tkinter as tk
import PIL.Image
import PIL.ImageTk
import cv2
from functools import partial
import threading
import imutils
import web
import portscanner
# import dir_search
import waybackurl
from functools import partial

set_width = 900
set_height = 600

root = tk.Tk()
root.title('Web Enumeration')
root.geometry("900x600")
root.minsize(800, 500)
# root.configure(bg='blue')
current_window = "x"


def printInput():
    inp = search.get()
    tk.Label(root, text=f"Provided Input: {inp}", font="comicsansms 13 italic").grid(row=1, column=0)


search = tk.StringVar()
tk.Entry(root, textvariable=search, width=55, font="comicsansms 13 italic").grid(row=0, column=0)
printButton = tk.Button(root, text="Print", command=printInput, pady=2, padx=3).grid(row=0, column=1)
tk.Label(root, text="Provided Input: ", font="comicsansms 13 italic").grid(row=1, column=0)


def port_btn():
    portscanner.target = search.get()
    a = int(from1.get())
    b = int(to1.get())
    x = int(thread1.get())
    # print(f"{thread1, from_, to_} tk")
    # print(f"{int(from1.get()), to1.get(), thread1.get()} tk2")
    portscanner.portscanner(x, a, b)  # port scanning
    with open("result/port.txt", 'r') as f:
        tk.Label(root, text=f"{f.read()}", font="comicsansms 13", pady=4).grid(row=80, column=0)


from1 = tk.StringVar()
to1 = tk.StringVar()
thread1 = tk.StringVar()
email_link = tk.StringVar()


def Port_Scan():
    global from1, to1, thread1
    tk.Label(root, text="Port Scan", font="comicsansms 13 bold", pady=4).grid(row=13, column=0)
    tk.Label(root, text="Port Range:", font="comicsansms 13", pady=4).grid(row=14, column=0)
    tk.Label(root, text="From=", font="comicsansms 13", pady=4).grid(row=14, column=1)
    tk.Entry(root, textvariable=from1, width=8, font="comicsansms 13 italic").grid(row=14, column=2)
    tk.Label(root, text="To=", font="comicsansms 13", pady=4).grid(row=14, column=3)
    tk.Entry(root, textvariable=to1, width=8, font="comicsansms 13 italic").grid(row=14, column=4)
    tk.Label(root, text="Thread=", font="comicsansms 13", pady=4).grid(row=15, column=1)
    tk.Entry(root, textvariable=thread1, width=8, font="comicsansms 13 italic").grid(row=15, column=2)
    tk.Button(root, text="Scan", command=port_btn, pady=2, padx=3).grid(row=16, column=1)


def email_btn():
    print(email_link.get())
    web.a1 = search.get()
    web.argument = int(email_link.get())
    web.scrap_emails()        # email scraping
    with open("result/mail.txt", 'r') as f:
        tk.Label(root, text=f"emails:{f.read()}", font="comicsansms 13", pady=4).grid(row=81, column=0)


def email():
    tk.Label(root, text="Email Scraper", font="comicsansms 13 bold", pady=4).grid(row=23, column=0)
    tk.Label(root, text="Number of Links you want to search:", font="comicsansms 13", pady=4).grid(row=24, column=0)
    tk.Entry(root, textvariable=email_link, width=8, font="comicsansms 13 italic").grid(row=24, column=1)
    tk.Button(root, text="Search", command=email_btn, pady=2, padx=3).grid(row=24, column=3)


def subdomain_btn():
    pass


def subdomain():
    tk.Label(root, text="Subdomain finder", font="comicsansms 13 bold", pady=4).grid(row=30, column=0)


Port_Scan()
email()
subdomain()

# statusvar = tk.StringVar()
# statusvar.set("Ideal")
# sbar = tk.Label(root, textvariable=statusvar, relief='sunken', anchor="w").grid(row=33, column=1)
# sbar.pack(side='bottom', fill='x')
root.mainloop()
