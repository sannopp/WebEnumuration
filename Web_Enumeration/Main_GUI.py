import tkinter as tk
import threading
import sys
import web
import portscanner
import dir_search
import io

# Initialize GUI
root = tk.Tk()
root.title('Web Enumeration Tool')
root.geometry("900x650")
root.configure(bg="#1e1e1e")  # Dark mode background

# Frame for Output Box
output_frame = tk.Frame(root, bg="#1e1e1e")
output_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Styled Output Text Box
output_text = tk.Text(output_frame, height=15, width=100, wrap='word', bg="#2d2d2d", fg="white",
                      font=("Consolas", 12), insertbackground="white", relief="flat")
output_text.pack(fill="both", expand=True, padx=10, pady=10)
output_text.insert(tk.END, "Results will be displayed here...\n")

# Function to display output inside GUI output box
def print_output(text):
    output_text.insert(tk.END, text + "\n")
    output_text.see(tk.END)

# Redirect standard output to GUI
class RedirectText(io.StringIO):
    def write(self, string):
        print_output(string)

sys.stdout = RedirectText()  # Redirects print() output to the GUI

# Title Label
title_label = tk.Label(root, text="Web Enumeration Tool", font=("Arial", 18, "bold"), bg="#1e1e1e", fg="white")
title_label.pack(pady=10)

# User Input for Target URL
search = tk.StringVar()
frame_target = tk.Frame(root, bg="#1e1e1e")
tk.Label(frame_target, text="Target URL:", font=("Arial", 12), bg="#1e1e1e", fg="white").pack(side='left', padx=5)
tk.Entry(frame_target, textvariable=search, width=50, font=("Consolas", 12), bg="#2d2d2d", fg="white", relief="flat").pack(side='left', padx=5)
frame_target.pack(pady=5)

# Function to execute port scanning and display results
def port_scanner_btn():
    target = search.get().replace("http://", "").replace("https://", "")
    a = int(from1.get())
    b = int(to1.get())
    x = int(thread1.get())

    def run_scan():
        portscanner.target = target
        portscanner.portscanner(x, a, b)

        with open("result/port.txt", "r") as file:
            result = file.read()
        print_output(f"\n🔍 Port Scan Results:\n{result}")

    threading.Thread(target=run_scan).start()

# Port Scanning UI
frame_port_scan = tk.Frame(root, bg="#1e1e1e")
tk.Label(frame_port_scan, text="Port Scan", font=("Arial", 12, "bold"), bg="#1e1e1e", fg="white").pack(side='top', pady=2)
from1, to1, thread1 = tk.StringVar(), tk.StringVar(), tk.StringVar()
tk.Label(frame_port_scan, text="From:", font=("Arial", 11), bg="#1e1e1e", fg="white").pack(side='left', padx=2)
tk.Entry(frame_port_scan, textvariable=from1, width=6, bg="#2d2d2d", fg="white", relief="flat").pack(side='left', padx=2)
tk.Label(frame_port_scan, text="To:", font=("Arial", 11), bg="#1e1e1e", fg="white").pack(side='left', padx=2)
tk.Entry(frame_port_scan, textvariable=to1, width=6, bg="#2d2d2d", fg="white", relief="flat").pack(side='left', padx=2)
tk.Label(frame_port_scan, text="Threads:", font=("Arial", 11), bg="#1e1e1e", fg="white").pack(side='left', padx=2)
tk.Entry(frame_port_scan, textvariable=thread1, width=6, bg="#2d2d2d", fg="white", relief="flat").pack(side='left', padx=2)
tk.Button(frame_port_scan, text="Scan", command=port_scanner_btn, font=("Arial", 10, "bold"), bg="#008CBA", fg="white", relief="flat").pack(side='left', padx=5)
frame_port_scan.pack(pady=5)

# Function to execute email extraction
def email_btn():
    web.a1 = search.get()
    web.argument = int(email_link.get())

    def run_email_scraper():
        web.scrap_emails()

        with open("result/mail.txt", "r") as file:
            result = file.read()
        print_output(f"\n📧 Email Extraction Results:\n{result}")

    threading.Thread(target=run_email_scraper).start()

# Email Extraction UI
frame_email = tk.Frame(root, bg="#1e1e1e")
tk.Label(frame_email, text="Email Extraction", font=("Arial", 12, "bold"), bg="#1e1e1e", fg="white").pack(side='left', padx=5)
email_link = tk.StringVar()
tk.Entry(frame_email, textvariable=email_link, width=6, bg="#2d2d2d", fg="white", relief="flat").pack(side='left', padx=5)
tk.Button(frame_email, text="Search", command=email_btn, font=("Arial", 10, "bold"), bg="#008CBA", fg="white", relief="flat").pack(side='left', padx=5)
frame_email.pack(pady=5)

# Function to execute directory bruteforce
def dirsearch_btn():
    target = search.get()

    def run_dirsearch():
        dir_search.run_directory_search(target)

        with open("result/dirs.txt", "r") as file:
            result = file.read()
        print_output(f"\n📂 Directory Bruteforce Results:\n{result}")

    threading.Thread(target=run_dirsearch).start()

# Directory Bruteforcing UI
frame_dir = tk.Frame(root, bg="#1e1e1e")
tk.Label(frame_dir, text="Directory Search", font=("Arial", 12, "bold"), bg="#1e1e1e", fg="white").pack(side='left', padx=5)
tk.Button(frame_dir, text="Run", command=dirsearch_btn, font=("Arial", 10, "bold"), bg="#008CBA", fg="white", relief="flat").pack(side='left', padx=5)
frame_dir.pack(pady=5)

# Run the main event loop
root.mainloop()