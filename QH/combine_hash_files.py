import os

def main():
    if not os.path.exists('all.txt'):
        with open('all.txt', 'w') as f:
            pass
        pass
    lines_set = set()
    for filename in ['FileHash-MD5.txt', 'FileHash-SHA1.txt', 'FileHash-SHA256.txt']:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line != '':
                    lines_set.add(line)
    with open('all.txt', 'w') as a:
        for line in lines_set:
            a.write(line + '\n')

if __name__ == '__main__':
    # It will combine all the unique hashes from 'FileHash-MD5.txt', 'FileHash-SHA1.txt', 'FileHash-SHA256.txt' to `all.txt`
    main()

print("Done...")
