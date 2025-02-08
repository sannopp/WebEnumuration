import tkinter as tk
# import PIL.Image
# import PIL.ImageTk
# import cv2
# from functools import partial
import threading
# import imutils
import web
import portscanner
import dir_search
import waybackurl
# from functools import partial

set_width = 900
set_height = 600

root = tk.Tk()
root.title('Web Enumeration')
root.geometry("900x600")
root.minsize(800, 500)
# root.configure()


def print_search():
    l1.config(text=f"Target: {search.get()}")
    pass


search = tk.StringVar()
f1 = tk.Frame(root)
tk.Entry(f1, textvariable=search, width=55, font="comicsansms 13 italic").pack(side='left', padx=6)
tk.Button(f1, text="Print", command=print_search, font="comicsansms 9 italic", anchor='e').pack()
l1 = tk.Label(root, text="Target:", font="comicsansms 13 italic", padx=6)
f1.pack(anchor='w', pady=5, padx=6)
l1.pack(anchor='w')

from1 = tk.StringVar()
to1 = tk.StringVar()
thread1 = tk.StringVar()
email_link = tk.StringVar()
Checkbutton1 = tk.IntVar()
x11 = 0
x12 = 0
x13 = 0
x14 = 0
x15 = 0
x16 = 0


def port_scanner_btn():
    s = search.get()
    if s.startswith("http://"):
        s = s[7:]
    if s.startswith("https://"):
        s = s[8:]
    # print(s)
    portscanner.target = s
    a = int(from1.get())
    b = int(to1.get())
    x = int(thread1.get())
    t1 = threading.Thread(target=portscanner.portscanner, args=(x, a, b))
    # portscanner.portscanner(x, a, b)  # port scanning
    # t1.start()

    global x11
    if x11 == 0:
        x11 = 0
        t1.start()
        # portscanner.portscanner(x, a, b)


def Port_Scan():
    global from1, to1, thread1
    f2 = tk.Frame(root)
    tk.Label(f2, text="Port Scan", font="comicsansms 13 bold", pady=1).pack()
    tk.Label(f2, text="Port Range:", font="comicsansms 13").pack(side='left')
    tk.Label(f2, text="From=", font="comicsansms 13").pack(side='left')
    tk.Entry(f2, textvariable=from1, width=8, font="comicsansms 13 italic").pack(side='left')
    tk.Label(f2, text="To=", font="comicsansms 13").pack(side='left')
    tk.Entry(f2, textvariable=to1, width=8, font="comicsansms 13 italic").pack(side='left')
    tk.Label(f2, text="Threads=", font="comicsansms 13").pack(side='left')
    tk.Entry(f2, textvariable=thread1, width=8, font="comicsansms 13 italic").pack(side='left')
    tk.Label(f2, text="", font="comicsansms 13").pack(side='left')
    tk.Button(f2, text="Scan", command=port_scanner_btn, font="comicsansms 9 italic").pack()
    f2.pack()


def email_btn():
    # print(email_link.get())
    web.a1 = search.get()
    web.argument = int(email_link.get())
    t1 = threading.Thread(target=web.scrap_emails)  # email scraping
    global x12
    if x12 == 0:
        x12 = 0
        t1.start()
        # web.scrap_emails()


def email():
    global email_link
    f3 = tk.Frame(root)
    tk.Label(f3, text="Email Scraper", font="comicsansms 13 bold", pady=1).pack()
    tk.Label(f3, text="Number of Links you want to search=", font="comicsansms 13").pack(side='left')
    tk.Entry(f3, textvariable=email_link, width=8, font="comicsansms 13 italic").pack(side='left')
    tk.Label(f3, text="", font="comicsansms 13").pack(side='left')
    tk.Button(f3, text="Search", command=email_btn, font="comicsansms 9 italic").pack()
    f3.pack()


def cert():
    s = search.get()
    if s.startswith("http://"):
        s = s[7:]
    if s.startswith("https://"):
        s = s[8:]
    web.a1 = s
    t1 = threading.Thread(target=web.subdomain_crtsh)  # subdomains from cert.sh website
    global x13
    if x13 == 0:
        x13 = 0
        t1.start()
        # web.subdomain_crtsh()


def dns_dumpster():
    s = search.get()
    if s.startswith("http://"):
        s = s[7:]
    if s.startswith("https://"):
        s = s[8:]
    if s.startswith("www."):
        s = s[4:]
    web.a1 = s
    t1 = threading.Thread(target=web.dns_dumpster)  # subdomains from DNSDumpster online tool
    global x14
    if x14 == 0:
        x14 = 0
        t1.start()
        # web.dns_dumpster()


def subdomain():
    f4 = tk.Frame(root)
    tk.Label(f4, text="Find subdomain", font="comicsansms 13 bold", pady=1).pack()
    tk.Button(f4, text="Find from cert.sh", command=cert, font="comicsansms 11 italic").pack(side='left')
    tk.Label(f4, text=" ", font="comicsansms 13 bold", pady=1).pack(side='left')
    tk.Button(f4, text="Find from DNSDumpster", command=dns_dumpster, font="comicsansms 11 italic").pack(side='left')
    f4.pack()


def way_back_btn():
    waybackurl.a1 = search.get()
    t1 = threading.Thread(target=waybackurl.way_back_url)  # web.archive.org  way back urls
    global x15
    if x15 == 0:
        x15 = 0
        t1.start()
        # waybackurl.way_back_url()


def way_back():
    f5 = tk.Frame(root)
    tk.Label(f5, text="Way Back urls : ", font="comicsansms 13 bold", pady=1).pack(side='left')
    tk.Button(f5, text="Find", command=way_back_btn, font="comicsansms 11 italic").pack()
    f5.pack()


def dirsearch_btn():
    dir_search.url = search.get()
    x = Checkbutton1.get()
    if x == 1:
        s = "apache-user-enum-1.0"
    elif x == 2:
        s = "directory-list-1.0"
    elif x == 3:
        s = "directory-list-2.3-medium"
    elif x == 4:
        s = "directory-list-2.3-small_edited"
    elif x == 5:
        s = "directory-list-2.3-small_original"
    elif x == 6:
        s = "directory-list-lowercase-2.3-medium"
    elif x == 7:
        s = "directory-list-lowercase-2.3-small"
    else:
        s = "directory-list-2.3-small_edited"
    dir_search.s = s
    dir_search.run()
    # dir_search.dir_search_run(s)  # find hidden directories
    # dir_search.write_dir_results()


def dir_search11():
    f6 = tk.Frame(root)
    tk.Label(f6, text="Directory search", font="comicsansms 13 bold", pady=1).pack()
    tk.Label(f6, text="wordlist:", font="comicsansms 11", pady=1).pack(side='left')
    global Checkbutton1

    tk.Radiobutton(f6, text="apache-user-enum-1.0", variable=Checkbutton1, value=1, indicator=0,
                   ).pack()
    tk.Radiobutton(f6, text="directory-list-1.0", variable=Checkbutton1, value=2, indicator=0,
                   ).pack()
    tk.Radiobutton(f6, text="directory-list-2.3-medium", variable=Checkbutton1, value=3, indicator=0,
                   ).pack(fill='x')
    tk.Radiobutton(f6, text="directory-list-2.3-small_edited", variable=Checkbutton1, value=4, indicator=0,
                   ).pack()
    tk.Radiobutton(f6, text="directory-list-2.3-small_original", variable=Checkbutton1, value=5, indicator=0,
                   ).pack()
    # tk.Label(f6, text="  ").pack()
    tk.Radiobutton(f6, text="directory-list-lowercase-2.3-medium", variable=Checkbutton1, value=6, indicator=0,
                   ).pack()
    tk.Radiobutton(f6, text="directory-list-lowercase-2.3-small", variable=Checkbutton1, value=7, indicator=0,
                   ).pack()
    tk.Button(f6, text="dirsearch", command=dirsearch_btn, font="comicsansms 11 italic").pack(side='right')
    f6.pack()


Port_Scan()
email()
subdomain()
way_back()
dir_search11()
root.mainloop()
