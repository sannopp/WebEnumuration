import os
import re
import zipfile
import tarfile
import shutil

def is_compressed_file(filename, target_folder):
    with open(filename, 'rb') as f:
        header = f.read(8)
    if header.startswith(b'PK') :
        # print(filename)
        is_apk = False
        try:
            with zipfile.ZipFile(filename, 'r') as zf:
                if "[Content_Types].xml" in zf.namelist():
                    if not ("manifest.json" in zf.namelist()):
                        print(filename, ": Doc file")
                        return False
                elif 'AndroidManifest.xml' in zf.namelist() and 'classes.dex' in zf.namelist():
                    is_apk = True
            pass
        except Exception as e:
            # print(e)
            print(filename, ": Bad Zip")
            return False
            pass
        if is_apk:
            if not os.path.exists("apk"):
                os.mkdir("apk")
            shutil.move(filename, os.path.join("./apk", os.path.basename(filename)))
            # os.rename(filename, os.path.join("./apk", os.path.basename(filename)))
            print(filename, ": apk")
        else:
            os.rename(filename, os.path.join(target_folder, os.path.basename(filename+"_zip")))
            print(filename, ": zip")
    elif tarfile.is_tarfile(filename):
        os.rename(filename, os.path.join(target_folder, os.path.basename(filename+"_tar")))
        print(filename, ": tar")
    elif header.startswith(b'Rar!\x1A\x07\x00') or header.startswith(b'Rar!\x1A\x07\x01'):
        print(filename, ": rar")
        os.rename(filename, os.path.join(target_folder, os.path.basename(filename+"_rar")))
    elif header.startswith(b'7z\xbc\xaf\x27\x1c'):
        print(filename, ": 7z")
        os.rename(filename, os.path.join(target_folder, os.path.basename(filename+"_7z")))
    elif header.startswith(b'!<arch>'):
        print(filename, ": arch")
        os.rename(filename, os.path.join(target_folder, os.path.basename(filename+"_arch")))
    elif header.startswith(b'\x1f\x8b\x08') or header.startswith(b'\x1f\x8b\x07'):
        print(filename, ": Gzip")
        os.rename(filename, os.path.join(target_folder, os.path.basename(filename+"_G_zip")))


def main():
    # move the compressed files from 'sample' to 'archive' 
    target_folder = 'archive'
    if not os.path.exists(target_folder):
        os.mkdir(target_folder)
    for filename in os.listdir('./sample'):
        if filename.endswith('.py') or filename == target_folder:
            continue
        is_compressed_file("./sample/"+filename, target_folder)

if __name__ == '__main__':
    # place all files in "sample" directory
    # run the script in parent directory of 'sample'
    # it will move all the apk and compressed files to seprate folder
    main()

print("\nDone...\n")
