# This program automates the process of collecting, converting, and compiling
# large volumes of data. It is intended for use only by Kumho Eng, Inc.

from os import listdir
from helpers import compile_dirs, convert_data, averages

# Config -- Change to inputs for ease of client use
data_dir = "C:\\Users\\jmweb\\Code\\kumho-compiler\\Data"
mixers = listdir(data_dir)
target_data = ["DPG", "PH", "PT"]
target_time = "0002 (Float).DAT"

# Location of FTView File Viewer (to convert .DAT to .CSV via command line)
ftvfv = ("C:\\Users\\jmweb\\Desktop\\FTViewFileViewer.exe")

compiled_dirs = compile_dirs(data_dir, mixers, target_data)
converted_dir = convert_data(compiled_dirs, target_time, ftvfv)
averages(converted_dir, target_time)
