import os
import shutil
import hashlib
import stat


def move_files_to_PE_NONPE_directory():
    if not os.path.exists("sample"):
        os.mkdir("sample")
    for root, dirs, files in os.walk('.'):
        for file in files:
            src = os.path.join(root, file)
            dst = os.path.join('sample/', file)
            if src == dst or src.endswith(".txt") or src.endswith(".py") or src.endswith(".csv"):
                continue
            # if os.path.exists(dst):
            #     os.remove(src)
            #     continue
            shutil.move(src, dst)
            print(src)


if __name__ == "__main__":
    move_files_to_PE_NONPE_directory()
    pass


