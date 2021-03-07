#!/usr/bin/env python3
"""
Automates organizing and synthesizing data into meaningful graphs.
"""
import os

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from csv import DictReader
from datetime import date
from matplotlib import pyplot as plt
from statistics import mean, StatisticsError
from subprocess import run
from time import time


def configure():
    """Configures application to user's needs."""
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

    print("📁 Select directory to analyze:")

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

    # CONFIGURE app
    root = os.getcwd()
    target_dir, target_hr = configure()

    # CONVERT specified files to CSV
    cmds, csvs, num_files = convert_setup(target_dir, target_hr)

    print(f"\n🌱 Converting {num_files} files to CSV... "
          "(This may take a minute.)")

    start_time = time()

    # -- Run the commands concurrently
    # with ThreadPoolExecutor() as executor:
    #     executor.map(run, cmds)

    print(f"🌼 Done! ({int(time() - start_time)} seconds)")

    # CALCULATE average of each CSV
    os.chdir(os.path.normpath(f"../{csvs}"))
    csvs = os.listdir()

    print("\n🧮 Calculating averages... ")

    start_time = time()

    # -- Calculate concurrently
    with ProcessPoolExecutor() as executor:
        avgs = executor.map(calc_avg, csvs)
        data = {_date: _avg for _date, _avg in avgs}

    print(f"📋 Done! ({int(time() - start_time)} seconds)")

    # PLOT averages
    print("\n📏 Plotting data... ")

    # -- x-axis is the dates (keys), y-axis is the average (values)
    x, y = zip(*sorted(data.items()))

    # -- Format hour for title
    hour = target_hr if target_hr <= 12 else target_hr - 12
    am_pm = "AM" if target_hr < 12 else "PM"

    # -- Style, plot, add information
    plt.style.use("seaborn-pastel")
    plt.plot_date(x, y, linestyle="solid")
    plt.gcf().autofmt_xdate()
    plt.title(f"{target_dir} - {hour} {am_pm} Averages")
    plt.xlabel("Date")
    plt.ylabel("Value")

    # -- Save plot
    data_items = tuple(data.items())
    fig_name = f"{target_dir} ({data_items[0][0]} {data_items[-1][0]}).png"

    os.chdir(os.path.normpath(root))
    plt.savefig(fig_name)

    print(f"📈 Done!\n💾 {fig_name} saved to {root}")


if __name__ == "__main__":
    os.chdir("data")  # DEV
    main()
