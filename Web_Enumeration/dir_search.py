from queue import Queue
import requests
from colorama import Fore
import threading
import sys

try:
    a1 = sys.argv[1]
    if a1.startswith('http'):
        pass
    else:
        a1 = 'https://' + a1
except IndexError:
    # print(e)
    a1 = "https://ldce.ac.in"
    # print("target:", a1)
url = a1
# url = "https://www.geeksforgeeks.org/"
d1 = []
q = Queue()
s = "directory-list-2.3-small_edited"
# fill Queue with lines


def fill_lines():
    with open(f"wordlist/{s}.txt") as f1:     # change file address
        lines = f1.readlines()
    for line in lines:
        # line.strip()
        m1_url = url + '/' + line.strip() + "/"
        q.put(m1_url)

# check directory if available


def dir_search_check(m_url):
    # with open("D:/html/directory-list-lowercase-2.3-small.txt") as f1:
    #     lines = f1.readlines()
    # for line in lines:
    #     # line.strip()
    #     m_url = url + line.strip() + "/"
    try:
        r = requests.get(m_url)
        if not 399 < r.status_code < 500:
            d1.append(f'{m_url}       #{r.status_code}')
            print(f'{m_url}       #{r.status_code}')
            return True
        else:
            return False
    except Exception as e:
        # print(e)
        pass

# check all directories from queue


def worker():
    try:
        while not q.empty():
            m_url = q.get()
            dir_search_check(m_url)
    except KeyboardInterrupt:
        print(Fore.YELLOW, 'KeyboardInterrupt Exiting...')

# save results to file


def write_dir_results():
    # with open(f"{url[8:]}_direct.txt", 'w') as results:
    #     for i in d1:
    #         results.write(i)
    results = open("result/dirs.txt", 'a')
    for i in d1:
        results.write(f'{i} \n')
    results.close()
    print('results save to: dirs.txt')

# run worker function using threads for speed


def dir_search_run():
    # with open(f"wordlist/{wordlist}.txt") as f1:     # change file address
    #     lines = f1.readlines()
    # for line in lines:
    #     line.strip()
        # m1_url = url + '/' + line.strip() + "/"
        # q.put(m1_url)
    print(Fore.YELLOW, f'searching directories for {url}', Fore.GREEN)
    thread_list = []
    for i in range(120):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()


def run():
    fill_lines()
    dir_search_run()
    write_dir_results()


if __name__ == '__main__':
    dir_search_run()
    write_dir_results()
