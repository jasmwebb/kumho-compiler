#!/usr/bin/env python3
"""
Automates organizing and synthesizing data into meaningful graphs.
"""
import os

from collections import OrderedDict
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from csv import DictReader
from datetime import date
from statistics import mean, StatisticsError
from subprocess import run
from time import time


def configure(dev=False):
    """Configures application to user's needs."""
    if dev:
        os.chdir("data")

    def validate_input(user_input, upper_bound):
        """Validates the user's input."""
        try:
            user_input = int(user_input)
        except ValueError:
            print("🚨 Please enter an integer.")
            return None

        if user_input < 0:
            print("🚨 Please enter a positive integer or zero.")
            return None

        if user_input > upper_bound:
            print("🚨 Please enter a positive integer within the given"
                  " contraints.")
            return None

        return user_input

    # Configure target directory
    dirs = tuple(_dir for _dir in os.listdir()
                 if os.path.isdir(_dir) and not _dir.endswith("CSV"))
    target_dir = None

    print("\n📁 Select directory to analyze:")

    for i, _dir in enumerate(dirs):
        print(f"\t{i} | {_dir}")

    while target_dir is None:
        ans = input("> ")
        target_dir = validate_input(ans, len(dirs) - 1)

    target_dir = dirs[target_dir]

    # Configure target hour
    target_hr = None

    print("\n🕑 Enter hour to isolate: (24-hour format, ex: 2:00 PM -> 14)")

    while target_hr is None:
        ans = input("> ")
        target_hr = validate_input(ans, 24)

    return target_dir, target_hr


def convert_setup(dirname, hr):
    """Creates a directory for the converted files and returns a map object of
    command line commands used to convert all DAT files within the given
    directory that contain float values from the given hour.
    Additionally returns the name of the newly created directiry and the number
    of files to convert for logging.
    """
    # Create a directory for the converted files if it doesn't already exist
    csv_dir = f"{dirname} CSV"

    try:
        os.mkdir(csv_dir)
    except FileExistsError:
        pass

    # Go into parent directory of files to convert
    os.chdir(dirname)

    # Format hour if one-digit to avoid capturing unexpected files
    # -- ex: endswith(9) matches 09 and 19
    if hr < 10:
        hr = f"0{hr}"

    files = tuple(file for file in os.listdir()
                  if file.endswith(f"{hr} (Float).DAT"))

    def interpolate_args(filename):
        """Interpolates given filename into list of command line arguments for
        subprocess.run
        "FTViewFileViewer.exe" /sd FILE ../CSV DIRNAME/FILENAME.csv
        """
        ftview = os.path.normpath("../FTViewFileViewer.exe")
        dest = os.path.normpath(f"../{csv_dir}/{filename.rstrip('.DAT')}.csv")

        return [ftview, "/sd", filename, dest]

    return map(interpolate_args, files), csv_dir, len(files)


def calc_avg(filename):
    """Calculates the average of all the values in a given CSV. Returns the
    CSV's date and the average.
    """
    _yyyy, _m, _d, *_ = filename.split()
    file_date = date(int(_yyyy), int(_m), int(_d))

    with open(filename, "r") as csv_file:
        reader = DictReader(csv_file)

        try:
            avg = mean(float(row["Value"]) for row in reader)
        except StatisticsError:
            # Empty CSV
            avg = 0

    return file_date, avg


def main():
    """Main entry point"""

    # Configure app
    target_dir, target_hr = configure(True)

    # Convert specified files to CSV
    cmds, csvs, num_files = convert_setup(target_dir, target_hr)

    print(f"\n🌱 Converting {num_files} files to CSV... "
          "(This may take a minute.)")

    start_time = time()

    # -- Run the commands concurrently
    with ThreadPoolExecutor() as executor:
        executor.map(run, cmds)

    print(f"🌼 Done! ({int(time() - start_time)} seconds)")

    # Calculate average of each CSV
    os.chdir(os.path.normpath(f"../{csvs}"))
    csvs = os.listdir()

    print("\n🧮 Calculating averages... ")

    start_time = time()

    with ProcessPoolExecutor() as executor:
        avgs = executor.map(calc_avg, csvs)
        data = {_date: _avg for _date, _avg in avgs}

    print(f"📋 Done! ({int(time() - start_time)} seconds)")

    data = OrderedDict(sorted(data.items()))

    # TODO - Plot averages


if __name__ == "__main__":
    main()
