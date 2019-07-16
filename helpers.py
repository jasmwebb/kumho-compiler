from os import listdir, walk, makedirs, chdir
from os.path import join, basename, dirname, isfile
from subprocess import run
from csv import DictReader
from statistics import mean
from xlsxwriter import Workbook


# Compile list of all directories with relevant data
def compile_dirs(parent_dir, relevant_grandchild):
    compiled_dirs = {"parent": parent_dir, "children": {}}
    relevant_child = listdir(parent_dir)
    for child in relevant_child:
        compiled_dirs["children"][child] = []
        for grandchild in relevant_grandchild:
            compiled_dirs["children"][child].append(grandchild)
    return compiled_dirs


# Convert files fitting specified criteria and save to different location
def convert_data(orig_dirs, time, converter):
    print("Converting .DAT files to .CSV. "
          f"This may take a few minutes...\n{'='*80}")
    converted_dir = orig_dirs["parent"] + " CSV"
    for child, grandchildren in orig_dirs["children"].items():
        print(f"Inside {child} directory...")
        for grandchild in grandchildren:
            print(f"\t> Inside {grandchild} directory...")
            for root, _, files in walk(join(orig_dirs["parent"],
                                            child,
                                            grandchild)):
                # Create directories for converted files
                if files:
                    new_dir = join(converted_dir,
                                   child,
                                   grandchild,
                                   basename(root))
                    makedirs(new_dir, exist_ok=True)
                    chdir(root)
                    # Only convert files for specified time
                    for file in files:
                        if file.endswith(time):
                            new_file = join(new_dir, file.rstrip('.DAT'))
                            run([converter, file, new_file])
    print(f"{'='*80}\nConversion complete.")
    return converted_dir


# Create Excel workbooks from averages of all converted data
def averages(data_dirs, strip_time):
    print("Averaging data and creating Excel workbooks. "
          f"This may take a few minutes...\n{'='*80}")
    strip_time = strip_time.rstrip(".DAT") + ".csv"
    # Walk through directory of converted CSVs
    for root, subs, files in walk(data_dirs):
        # Where there are files, create new Excel workbook
        if files:
            # Disregard dirs containing previously compiled Excel workbooks
            try:
                if files[0].rstrip(".xlsx") == subs[0]:
                    continue
            except IndexError:
                pass
            # File naming
            sheet_name = basename(root)
            print(f"Creating workbook for {sheet_name}...")
            workbook_path = join(dirname(root), sheet_name + ".xlsx")
            # Skip dir if Excel workbook already exists
            if isfile(workbook_path):
                continue
            # Workbook config and formatting
            workbook = Workbook(workbook_path)
            worksheet = workbook.add_worksheet(sheet_name)
            worksheet.write_row("A1", ["Date", "Values"])
            date_format = workbook.add_format()
            date_format.set_num_format("yyyy mm dd")
            # Iterate through .CSV files in dir
            for row_num, file in enumerate(files, start=1):
                # Add date to worksheet
                worksheet.write(row_num, 0, file.rstrip(strip_time),
                                date_format)
                # Average first 10 values in file
                values = []
                with open(join(root, file), 'r') as data:
                    reader = DictReader(data)
                    for row in reader:
                        values.append(float(row["Value"].strip(' ')))
                # Add average to worksheet
                worksheet.write(row_num, 1, mean(values[:10]))
            # Create chart from data
            chart = workbook.add_chart({"type": "line"})
            chart.add_series({
                "values": [sheet_name, 1, 1, row_num, 1],
                "categories": [sheet_name, 1, 0, row_num, 0],
                "name": sheet_name,
                "marker": {"type": "square"}
            })
            chart.set_x_axis({
              "name": "Date",
              "date_axis": True
            })
            chart.set_y_axis({"name": "Value"})
            chart.set_legend({"none": True})
            worksheet.insert_chart("D2", chart)
            workbook.close()
    print(f"{'='*80}\nWorkbooks created.")
