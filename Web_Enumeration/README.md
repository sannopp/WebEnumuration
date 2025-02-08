# Web Enumeration Tool

---

This is Web Enumeration Tool with GUI to automate tasks like
* port scanning
* Directory Bruteforce
* Find WayBack Urls
* Scrap Emails
* Find SubDomains and other info

## About

---
 This is a python tool designed to enumerate subdomains of websites using
the cert.sh and dnsdumpster. 
 </br>
 The Port Scanning is done thorough
simple and basic technique in port scanning you give
inputs the range of port in 'from' and 'to' the range
 of ports you want to look for, and you can also 
 decide the number of threads.
 </br> 
 In Directory Bruteforce you select the wordlist from
 given options and start attack.
 </br>
 For finding the WayBack Urls it's very simple you 
 just hit the button, and you are good to go.
 </br>
 For email scrapping you give the limit how many links 
 you want to scrap it will start from the target and 
 first it will scrap all the links in that page 
 than look for email addresses in all webpage content
 and do the same for all links we find in page.
 

## Screenshots

---
<img width="608" alt="image" src="https://user-images.githubusercontent.com/79740895/152483612-91a0d25d-d1cb-4343-b5ce-af759cc438ff.png">

---
## Installation

---

```
   git clone https://github.com/Aftab700/Python_Projects.git
```

  

### Recommended Python Version:

---

This Tool currently supports Python 3.

* The recommended version for Python 3.9.5

---
This project is located inside Directory "Web_Enumeration"
change the Directory:

 ```
      cd Python_Projects/Web_Enumeration
 ```

## Dependencies:

---
This tool depends on the ```beautifulsoup4, colorama, imutils, opencv_python, Pillow and requests``` python modules.
</br></br>
These dependencies can be installed using the requirements file:

* Installation on Windows:

      pip install -r requirements.txt

* Installation on Linux:

      sudo pip install -r requirements.txt

## Run

---
Run the ```Main_GUI.py``` file:
* Windows:
```
       Python Main_GUI.py
```
* Linux:
```
       sudo python3 Main_GUI.py
```

---

[YouTube Link:](https://youtu.be/LwGD5K5S9Fg)
