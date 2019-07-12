# This program automates the process of collecting, converting, and compiling
# to Excel large volumes of data. It is intended for use only by Kumho Eng Inc.

from os import listdir
from os.path import join, dirname
from conversion import compile_dirs, convert_data

# Config -- Change to inputs for ease of client use
data_dir = join(dirname(__file__), "Data")
mixers = listdir(data_dir)
target_data = ["DPG", "PH", "PT"]
target_time = "0002 (Float).DAT"

# Location of FTView File Viewer (to convert .DAT to .CSV via command line)
ftvfv = ("E:\\FTViewFileViewer.exe")

compiled_dirs = compile_dirs(data_dir, mixers, target_data)
convert_data(compiled_dirs, target_time, ftvfv)
