#!/usr/bin/env python3
"""
Automates organizing and synthesizing data into meaningful graphs.
"""
import os

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from subprocess import run
from time import time

from helpers import calc_avg, configure, convert_setup, plot_averages


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
    with ThreadPoolExecutor() as executor:
        executor.map(run, cmds)

    print(f"🌼 Done! ({int(time() - start_time)} seconds)")

    # CALCULATE average of each CSV
    os.chdir(os.path.normpath(f"../{csvs}"))
    csvs = os.listdir()

    print("\n🧮 Calculating averages... ")

    start_time = time()

    # -- Calculate concurrently
    with ProcessPoolExecutor() as executor:
        avgs = executor.map(calc_avg, csvs)
        data = {_date: _avg for _date, _avg in avgs if _avg is not None}

    print(f"📋 Done! ({int(time() - start_time)} seconds)")

    # PLOT averages
    plot_averages(data, root, target_dir, target_hr)


if __name__ == "__main__":
    os.chdir("data")  # DEV
    main()
