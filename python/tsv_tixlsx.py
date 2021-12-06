import csv
from xlsxwriter.workbook import Workbook
import sys
# Add some command-line logic to read the file names.
tsv_file = sys.argv[1]
xlsx_file = sys.argv[2]

# Create an XlsxWriter workbook object and add a worksheet.
workbook = Workbook(xlsx_file)
worksheet = workbook.add_worksheet()

# Create a TSV file reader.
tsv_reader = csv.reader(open(tsv_file), delimiter='\t')

# Read the row data from the TSV file and write it to the XLSX file.
for row, data in enumerate(tsv_reader):
    worksheet.write_row(row, 0, data)

# Close the XLSX file.
workbook.close()