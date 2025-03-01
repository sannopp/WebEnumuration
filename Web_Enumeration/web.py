import base64
from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re
import sys
import os

# Ensure result directory exists
os.makedirs("result", exist_ok=True)

try:
    a1 = sys.argv[1]
    if not a1.startswith('http'):
        a1 = 'https://' + a1
except IndexError:
    a1 = 'https://www.google.com'

argument = 20  # Default number of links to crawl


def scrap_emails():
    global a1
    print("Target:", a1)
    
    user_url = a1
    urls = deque([user_url])  # Queue to store URLs for processing

    print(f'Running test on first {argument} links...\n')

    scraped_urls = set()
    emails = set()
    count = 0

    try:
        while urls:
            if count >= int(argument):
                print("\nProcess complete.\n")
                break
            count += 1
            url = urls.popleft()
            scraped_urls.add(url)

            parts = urllib.parse.urlsplit(url)
            base_url = f"{parts.scheme}://{parts.netloc}"
            path = url[:url.rfind('/') + 1] if '/' in parts.path else url
            
            print(f'[{count}] Processing {url}')

            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
            except (requests.exceptions.RequestException, requests.exceptions.ConnectionError):
                continue

            # Extract emails using regex
            new_emails = set(re.findall(r'[a-zA-Z0-9.\-+_]+@[a-zA-Z0-9.\-+_]+\.[a-z]+', response.text, re.I))
            emails.update(new_emails)

            # Parse page content for additional links
            soup = BeautifulSoup(response.text, "html.parser")  # Use built-in parser to avoid lxml dependency issues

            for anchor in soup.find_all("a", href=True):
                link = anchor["href"]
                if link.startswith('/'):
                    link = base_url + link
                elif not link.startswith('http'):
                    link = path + link

                if link not in urls and link not in scraped_urls:
                    urls.append(link)

    except KeyboardInterrupt:
        print('[-] KeyboardInterrupt Closing...')

    # Save extracted emails
    with open("result/mail.txt", 'w') as f:
        for mail in emails:
            f.write(f"{mail}\n")

    # Save visited links
    with open("result/links.txt", 'w') as f:
        for link in scraped_urls:
            f.write(f"{link}\n")

    # Print extracted emails after completion
    print("\nExtracted Emails:")
    if emails:
        for email in emails:
            print(email)
    else:
        print("No emails found.")
    
    print("Results saved to result/mail.txt")

    return 0


if __name__ == '__main__':
    scrap_emails()
