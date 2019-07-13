from os import walk
from os.path import basename, dirname, join
from csv import DictReader
from statistics import mean
from xlsxwriter import Workbook


# Create Excel workbooks from averages of all converted data
def averages(data_dirs, strip_time):
    print("Averaging data and creating Excel workbooks. "
          f"This may take a few minutes...\n{'='*80}")
    strip_time = strip_time.rstrip(".DAT") + ".csv"
    # Walk through directory of converted CSVs
    for root, _, files in walk(data_dirs):
        # Where there are files, make a new Excel workbook
        if files:
            print(f"Creating workbook for {basename(root)}...")
            workbook = Workbook(join(dirname(root), basename(root) + ".xlsx"))
            worksheet = workbook.add_worksheet(basename(root))
            worksheet.write(0, 0, "Date")
            worksheet.write(0, 1, "Value")
            for row_num, file in enumerate(files):
                # Add date to worksheet
                worksheet.write(row_num + 1, 0, file.rstrip(strip_time))
                # Average first 10 values in file
                values = []
                with open(join(root, file), 'r') as data:
                    reader = DictReader(data)
                    for row in reader:
                        values.append(float(row["Value"].strip(' ')))
                # Add average to worksheet
                worksheet.write(row_num + 1, 1, mean(values[:10]))
            workbook.close()
    print(f"{'='*80}\nWorkbooks created.")
