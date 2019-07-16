# This program automates the process of collecting, converting, and compiling
# large volumes of data. It is intended for use only by Kumho Eng, Inc.

from os import listdir
from glob import glob
from helpers import compile_dirs, convert_data, averages

# Config
# TODO - select folder within cwd
data_dir = "C:\\Users\\jmweb\\Code\\kumho-compiler\\Data"
mixers = listdir(data_dir)

# Config - User input
# target_data = []
# print("What data will be compiled? ".upper().ljust(80, '='))
# print("Press ENTER after each entry. Press ENTER again when finished.\n"
#       + '-'*80)
# while True:
#     data_type = input("\t> ").upper()
#     if not data_type:
#         break
#     target_data.append(data_type)
# print("Data from what time will be compiled? ".upper().ljust(80, '='))
# print("Enter the hour in 24-hour format (ex: 2 PM is 14, 4 AM is 04),"
#       " then press ENTER.\n" + '-'*80)
# target_time = "00" + input("\t> ") + " (Float).DAT"

# Location of FTView File Viewer (to convert .DAT to .CSV via command line)
# TODO - way to locate this file without user input
# ftvfv = ("C:\\Users\\jmweb\\Desktop\\FTViewFileViewer.exe")
print(glob("**/FTViewFileViewer.exe", recursive=True))

# compiled_dirs = compile_dirs(data_dir, mixers, target_data)
# converted_dir = convert_data(compiled_dirs, target_time, ftvfv)
# averages(converted_dir, target_time)
