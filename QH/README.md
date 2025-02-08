# Files for OTX sample processing

</br>

## create combined hash file

- copy all the OTX hash folders that you want to combine.
- run the [combine_hash_files_from_all_subdirectory.py](combine_hash_files_from_all_subdirectory.py) file.
- It will look for this three files in all subdirectories `FileHash-MD5.txt, FileHash-SHA1.txt, FileHash-SHA256.txt` and create the combined hash file `all.txt` in all subdirectories separately.
- after that it will create one `all.txt` file in current directory it is combined hash file of all the OTX hash folder.
- because the uploading hash limit is 10k there is a variable `limit = 9998` in script it will divide the combined hash file `all.txt` to multiple parts of 9998 lines to uploade on site.


</br>

## Copying folders from `Sample-Share` location

- put all the OTX Sample-Share path in file `input.txt`. example path: `\\192.168.21.11\Sample-Share\sample_search\20230830-131318`

- run the [copy_folders.bat](copy_folders.bat) file. It will copy all the folders path specified in [input.txt](input.txt) to `New Folder`.

</br>

## move all sample files from multiple folders to `sample` directory

- goto newly created `New Folder` where all the Sample-Share folders are copied
- run the [move_files_to_sample_folder.py](move_files_to_sample_folder.py) file.
- It will move all the samples from all subdirectory to new `sample` folder

</br>

## Check for apk or compressed files in `sample` folder

- run the [check_archive.py](check_archive.py) file.
- run this file in same direcdirectory as `sample`. not inside `sample` folder.
- It will create apk folder for apk and `archive` folder for compressed files

</br>

## unzip the files in archive folder and hashing

- unzip all files and delete these files after unzip. these files will have postfix like `_zip, _tar, _rar, _G_zip`.
- now run the [move_files_to_current_directory.py](move_files_to_current_directory.py)
- It will move all the files to current directory, delete empty folders, rename all the files to md5.
- now we can move all these files to `sample` folder and perform the previous step again to check for archives.

</br>


## running the scanner with batch files

- the files [autorun_scanner.py.bat](autorun_scanner.py.bat) and [autorun_android.bat](autorun_android.bat) are used to run the scanner for apk and samples to save few clicks 
- It will prompt for path on running
- **change the `cd` path accordingly to use it**

</br>

## finding undetected PE & NON-PE

- put the scanner results in `scan_report.xlsx` file under `scanner-sample` sheet name. you can change this accordingly as per need.
- run the [find_undetected.py](find_undetected.py) file (while running this file the Excel file should be close)
- it will create one column `ND` for No Detection to filter out the results.
- in the sheet named `undetected` it will write the undetected PE in `A` column and NON-PE in `B` column from second row.

</br>

## moving the undetected PE & NON-PE to separate folders to upload on AMCS

- if performed previous step you will have PE files in first column & NON-PE files in second column under sheet named 'undetected'
- if any error in the results modify it accordingly
- run the [move_pe_nonpe_files.py](move_pe_nonpe_files.py) file.
- It will move all the files starting from second row of `A` column to `PE` folder and from `B` column to `NON_PE` folder under sheet named 'undetected'.

_you can use [scan_report.xlsx](scan_report.xlsx) as template._
