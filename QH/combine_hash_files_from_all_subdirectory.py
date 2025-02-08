import os
import re

def create_all_txt(dir_path):
    if not os.path.exists(f'{dir_path}/all.txt'):
        with open(f'{dir_path}/all.txt', 'w') as f:
            pass
        pass
    lines_set = set()
    for filename in [f'{dir_path}/FileHash-MD5.txt', f'{dir_path}/FileHash-SHA1.txt', f'{dir_path}/FileHash-SHA256.txt']:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line != '':
                    lines_set.add(line)
    with open(f'{dir_path}/all.txt', 'w') as a:
        for line in lines_set:
            a.write(line + '\n')
            pass
        pass
    pass

def main():
    dir_list = []
    for dir_path in os.listdir("."):
        if os.path.isdir(dir_path):
            print(dir_path)
            dir_list.append(dir_path)
            try:
                create_all_txt(dir_path)
            except Exception as e:
                print(e)
                pass
    if not os.path.exists('all.txt'):
        with open('all.txt', 'w') as f:
            pass
        pass
    lines_set = set()
    for path_dir in dir_list:
        with open(f'{path_dir}/all.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line != '':
                    lines_set.add(line)
    with open(f'all.txt', 'w') as a:
        for line in lines_set:
            a.write(line + '\n')
        pass
    print("\nFile of combined hash created: all.txt")


def split_file(file_name, limit):
    file_list = []
    current_file = None
    lines_read = 0

    with open(file_name, 'r') as f:
        current_file_name = file_name[:-4] + '_part-' + str(len(file_list)+1) + '.txt'
        current_file = open(current_file_name, 'w')
        file_list.append(current_file_name)
        lines_read = 0
        for line in f:
            if lines_read == limit:
                if current_file:
                    current_file.close()
                    # print(current_file_name)
                current_file_name = file_name[:-4] + '_part-' + str(len(file_list)+1) + '.txt'
                current_file = open(current_file_name, 'w')
                file_list.append(current_file_name)
                lines_read = 0
            current_file.write(line)
            lines_read += 1

    if current_file:
        current_file.close()
        # print(current_file_name)

    return file_list


if __name__ == '__main__':
    # it will create all.txt of combine hashes in all subdirectories
    # create all.txt of all subdirectories
    # It will also divide files based on 'limit' value which is number of max lines in file
    main()
    file_name = 'all.txt'
    limit = 9998
    file_list = split_file(file_name, limit)
    print('\nThe split files are:\n')
    for file_name in file_list:
        print(file_name)


print("\n\nDone...\n")
