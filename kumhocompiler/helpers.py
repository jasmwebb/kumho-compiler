import os

from csv import DictReader
from datetime import date
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator
from statistics import mean, StatisticsError


def calc_avg(filename):
    """Calculates the average of all the values in a given CSV. Returns the
    CSV's date and the average.
    """
    _yyyy, _m, _d, *_ = filename.split()
    file_date = date(int(_yyyy), int(_m), int(_d))

    with open(filename, "r") as csv_file:
        reader = DictReader(csv_file)

        try:
            avg = abs(mean(float(row["Value"]) for row in reader))
            avg = avg if avg <= 300 else None
        except StatisticsError:
            # Empty CSV
            avg = None

    return file_date, avg


def configure():
    """Configures application to user's needs."""

    # Configure target directory
    dirs = tuple(_dir for _dir in os.listdir()
                 if os.path.isdir(_dir) and not _dir.endswith("CSV"))
    target_dir = None

    print("📁 Select directory to analyze:")

    for i, _dir in enumerate(dirs):
        print(f"\t{i} | {_dir}")

    # ----- LOCAL FUNCTION -----
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
    # ----- END LOCAL FUNCTION -----

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
    csv_dir = f"{dirname} CSV {hr if hr >= 10 else f'0{hr}'}00"

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

    # ----- LOCAL FUNCTION -----
    def interpolate_args(filename):
        """Interpolates given filename into list of command line arguments for
        subprocess.run
        ../FTViewFileViewer.exe /sd FILE ../CSV DIRNAME/FILENAME.csv
        """
        ftview = os.path.normpath("../FTViewFileViewer.exe")
        dest = os.path.normpath(f"../{csv_dir}/{filename.rstrip('.DAT')}.csv")

        return [ftview, "/sd", filename, dest]
    # ----- END LOCAL FUNCTION -----

    return map(interpolate_args, files), csv_dir, len(files)


def plot_averages(data, root_dir, dirname, hr):
    """Plots and saves a time series from given data."""
    print("\n📏 Plotting data... ")

    # x-axis is the dates (keys), y-axis is the average (values)
    x, y = zip(*sorted(data.items()))

    # Format hour for title
    hour = hr if hr <= 12 else hr - 12
    am_pm = "AM" if hr < 12 else "PM"

    # Style, plot, add information
    plt.style.use("seaborn-pastel")

    fig, ax = plt.subplots(1, 1, figsize=(12.8, 9.6))

    ax.plot_date(x, y, linestyle="solid", marker=None)

    plt.title(f"{dirname} - {hour} {am_pm}")
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Value")

    plt.xticks(rotation=45)
    months = MonthLocator()
    months_format = DateFormatter("%b %Y")
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(months_format)

    # Save plot
    fig_name = f"{dirname} {hr if hr >= 10 else f'0{hr}'}00.png"
    plt.savefig(os.path.normpath(f"{root_dir}/{fig_name}"))

    print(f"📈 Done!\n💾 {fig_name} saved to {root_dir}")
