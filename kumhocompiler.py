# This program automates the process of collecting, converting, and compiling
# large volumes of data. It is intended for use only by Kumho Eng, Inc.

from os import listdir
from os.path import abspath
from helpers import compile_dirs, convert_data, averages

# Config and user input
ftvfv = abspath("FTViewFileViewer.exe")
all_dirs = listdir()

print("Which directory contains the data? ".upper().ljust(80, '='))
for i, dir in enumerate(all_dirs):
    print(f"{i}: {dir}")
data_dir = int(input("\t> "))
data_dir = abspath(all_dirs[data_dir])

print("What data will be compiled? ".upper().ljust(80, '='))
print("Press ENTER after each entry. Press ENTER again when finished.\n"
      + '-'*80)
target_data = []
while True:
    data_type = input("\t> ").upper()
    if not data_type:
        break
    target_data.append(data_type)

print("Data from what time will be compiled? ".upper().ljust(80, '='))
print("Enter the hour in 24-hour format (ex: 2 PM is 14, 4 AM is 04),"
      " then press ENTER.\n" + '-'*80)
target_time = "00" + input("\t> ") + " (Float).DAT"

# Automation
compiled_dirs = compile_dirs(data_dir, target_data)
converted_dir = convert_data(compiled_dirs, target_time, ftvfv)
averages(converted_dir, target_time)
