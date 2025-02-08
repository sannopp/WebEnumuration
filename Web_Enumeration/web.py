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


# noinspection PyUnusedLocal
def subdomain_crtsh():
    global a1
    try:
        if a1.startswith('https://'):
            a1 = a1[8:]
        else:
            a1 = a1
    except IndexError:
        # print(e)
        a1 = 'www.google.com'
    a = 'https://crt.sh/?q=' + a1
    print("target:", a1)
    print("finding subdomains from cert.sh site...")
    r1 = requests.get(a)
    r = r1.content
    soup = BeautifulSoup(r, 'html.parser')
    table = soup.find_all('table')
    # print(len(table))
    # print(table[2])
    x = set()
    x1 = table[2].stripped_strings
    # noinspection PyUnusedLocal
    i = 0
    j = -1
    # noinspection PyUnusedLocal
    k = 1
    for item in x1:
        j += 1
        if j > 11:
            # if 2 < k < 7:
            #     k += 1
            #     continue
            # if k > 6:
            #     k = 1
            #     # print(k)
            #     continue
            # k += 1
            if '=' in item:
                continue
            try:
                i = int(item[0])
            except ValueError:
                x.add(item)
                # print(e)
                # break
        # if j > 4325:
        #     print(j, "===", item)
    # print(len(x))
    # print(x)
    with open(f'result/cert.sh_domains.txt', 'w') as f:
        for aa in x:
            b = aa.encode('utf8')
            r = str(b)
            print(r)
            # print(b.decode('utf8'))
            f.write(f'{r}\n')
    # columns = [column for i, column in enumerate(x.find_all("td")) if i % 2 == 1]
    # print(type(columns))
    # cert_domains = set(re.findall(r'<td>', tr, re.I))
    print("cert_domains complete")


def dns_dumpster():
    global a1
    try:
        if a1.startswith('https://'):
            a1 = a1[8:]
        else:
            a1 = a1
    except IndexError:
        # print(e)
        a1 = 'google.com'
    # domain = "google.com"
    domain = a1
    print(f'Running dns-dumpster on:{domain}...')
    dnsdumpster_url = 'https://dnsdumpster.com/'

    req = requests.session().get(dnsdumpster_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    csrf_middleware = soup.findAll('input', attrs={'name': 'csrfmiddlewaretoken'})[0]['value']
    # self.display_message('Retrieved token: %s' % csrf_middleware)

    cookies = {'csrftoken': csrf_middleware}
    headers = {'Referer': dnsdumpster_url,
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/92.0.4515.107 Safari/537.36'}
    data = {'csrfmiddlewaretoken': csrf_middleware, 'targetip': domain, 'user': 'free'}
    req = requests.session().post(dnsdumpster_url, cookies=cookies, data=data, headers=headers)

    if req.status_code != 200:
        print(
            "Unexpected status code from {url}: {code}".format(
                url=dnsdumpster_url, code=req.status_code),
            file=sys.stderr,
        )
        return []

    if 'There was an error getting results' in req.content.decode('utf-8'):
        print("There was an error getting results", file=sys.stderr)
        return []

    # soup = BeautifulSoup(req.content, 'html.parser')
    res = {}
    xls_data = None
    try:
        pattern = r'/static/xls/' + domain + '-[0-9]{12}\.xlsx'
        # print("hello\n", req.content)
        xls_url = re.findall(pattern, req.content.decode('utf-8'))[0]
        xls_url = 'https://dnsdumpster.com' + xls_url
        xls_data = base64.b64encode(requests.session().get(xls_url).content)
    except Exception as err:
        print(err)
    finally:
        res['xls_data'] = xls_data
    # print(res['xls_data'])
    # print(res)
    xls_retrieved = res['xls_data'] is not None
    print("\n\n\nRetrieved XLS hosts? {} (accessible in 'xls_data')".format(xls_retrieved))
    print(repr(base64.b64decode(res['xls_data'])[:20]) + '...')  # to save it somewhere else.
    open(f'result/dns_dumpster.xlsx', 'wb').write(base64.b64decode(res['xls_data']))  # example of saving xlsx
    print(f"dnsdumpster results stored in:dns_{domain}.xlsx")
    pass


if __name__ == '__main__':
    scrap_emails()
    subdomain_crtsh()
    dns_dumpster()
    pass
