#!/usr/bin/env python3
"""
Automates organizing and synthesizing data into meaningful graphs.
"""
import os


def configure(dev=False):
    """Configures application to user's needs."""
    if dev:
        os.chdir("data")

    def valid_input(user_input, upper_bound):
        """Validates the users input."""

        # Must be an integer
        try:
            user_input = int(user_input)
        except ValueError:
            print("🚨 Please enter an integer.")
            return None

        # Must be a positive
        if user_input < 0:
            print("🚨 Please enter a positive integer.")
            return None

        # Below upper bound
        if user_input > upper_bound:
            print("🚨 Please enter a positive integer within the given contraints.")
            return None

        return user_input

    # Configure target directory
    dirs = tuple(filter(os.path.isdir, os.listdir()))
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

    print("\n🕑 Enter hour to isolate: (24-hour format, ex: 2:00 PM --> 14)")

    while target_hr is None:
        ans = input("> ")
        target_hr = valid_input(ans, 24)

    return target_dir, target_hr


def main():
    """Main entry point"""
    target_dir, target_hr = configure(True)


if __name__ == "__main__":
    main()
