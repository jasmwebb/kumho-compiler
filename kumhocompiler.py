#!/usr/bin/env python3
"""
Automates organizing and synthesizing data into meaningful graphs.
"""
import os
import time

from concurrent.futures import ThreadPoolExecutor
from subprocess import run


def configure(dev=False):
    """Configures application to user's needs."""
    if dev:
        os.chdir("data")


    def valid_input(user_input, upper_bound):
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
    dirs = tuple(dir for dir in os.listdir()
                 if os.path.isdir(dir) and not dir.endswith("CSV"))
    target_dir = None

    print("\n📁 Select directory to analyze:")

    for i, directory in enumerate(dirs):
        print(f"\t{i} | {directory}")

    while target_dir is None:
        ans = input("> ")
        target_dir = valid_input(ans, len(dirs) - 1)

    target_dir = dirs[target_dir]

    # Configure target hour
    target_hr = None

    print("\n🕑 Enter hour to isolate: (24-hour format, ex: 2:00 PM -> 14)")

    while target_hr is None:
        ans = input("> ")
        target_hr = valid_input(ans, 24)

    return target_dir, target_hr


def to_csv(dir, hr):
    """Converts all DAT files containing float values from the given hour
    within the given directory.
    """
    # Create a directory for the converted files if it doesn't already exist
    csv_dir = f"{dir} CSV"

    try:
        os.mkdir(csv_dir)
    except FileExistsError:
        pass

    # Go into parent directory of files to convert
    os.chdir(dir)

    # Format hour if one-digit to avoid capturing unexpected files
    # -- ex: endswith(9) matches 09 and 19
    if hr < 10:
        hr = f"0{hr}"

    files = tuple(file for file in os.listdir() if file.endswith(f"{hr} (Float).DAT"))
    num_files = len(files)


    # Create a list of command line commands to convert the relevant files
    # into CSV using FTViewFileViewer
    def interpolate_args(filename):
        """Interpolates given filename into list of command line arguments for
        subprocess.run
        "FTViewFileViewer.exe" /sd FILE ../CSV DIRNAME/FILENAME.csv
        """
        ftview = os.path.normpath("../FTViewFileViewer.exe")
        dest = os.path.normpath(f"../{csv_dir}/{filename.rstrip('.DAT')}.csv")

        return [ftview, "/sd", filename, dest]


    cmds = map(interpolate_args, files)

    print(f"\n🌱 Converting {num_files} files to CSV... (This may take a minute.)")

    # Run the commands concurrently
    start_time = time.time()

    with ThreadPoolExecutor() as executor:
        executor.map(run, cmds)

    print(f"🌼 Done! ({time.time() - start_time} seconds)")


def main():
    """Main entry point"""
    
    # Configure app
    target_dir, target_hr = configure(True)

    # Convert specified files to CSV
    # to_csv(target_dir, target_hr)

    # TODO - Calculate average of each CSV
    

    # TODO - Plot averages


if __name__ == "__main__":
    main()
