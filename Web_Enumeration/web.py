import base64
from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re
import sys

try:
    a1 = sys.argv[1]
    if a1.startswith('http'):
        pass
    else:
        a1 = 'https://' + a1
except IndexError:
    # print(e)
    a1 = 'https://www.google.com'

argument = 20


def scrap_emails():
    global a1
    print("target:", a1)
    # argument = input("number of link you want to search:")
    global argument
    # print(a1, argument)
    user_url = a1
    urls = deque([user_url])

    print(f'Running test on first {argument} links...')

    # print(urls)
    scraped_urls = set()
    emails = set()

    count = 0

    try:
        while len(urls):
            if count >= int(argument):
                print("\nProcess complete.\n")
                break
            count += 1
            url = urls.popleft()
            scraped_urls.add(url)

            parts = urllib.parse.urlsplit(url)
            base_url = '{0.scheme}://{0.netloc}'.format(parts)

            path = url[:url.rfind('/') + 1] if '/' in parts.path else url
            print('[%d] Processing %s' % (count, url))
            try:
                response = requests.get(url)
                # response = requests.get('https://rru.ac.in/dr-akshat-mehta/', verify=False)
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                continue

            # noinspection RegExpRedundantEscape
            new_emails = set(re.findall(r'[a-zA-Z0-9\.\-+_]+@[a-zA-Z0-9\.\-+_]+\.[a-z]+', response.text, re.I))
            emails.update(new_emails)

            soup = BeautifulSoup(response.text, features='lxml')

            for anchor in soup.find_all("a"):
                link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
                if link.startswith('/'):
                    link = base_url + link
                elif not link.startswith('http'):
                    link = path + link
                # if not link in urls and not link in scraped_urls:
                if not link in urls and not link in scraped_urls:
                    urls.append(link)
    except KeyboardInterrupt:
        print('[-]KeyboardInterrupt Closing...')

    s = user_url[8:]
    s = s.replace('/', '_')
    with open(f"result/mail.txt", 'w') as f:
        for mail in emails:
            print(mail)
            f.write(f"{mail}\n")

    with open(f"result/links.txt", 'w') as f:
        for a in scraped_urls:
            # print(mail)
            f.write(f"{a}\n")
    return 0


if __name__ == '__main__':
    scrap_emails()
    pass
