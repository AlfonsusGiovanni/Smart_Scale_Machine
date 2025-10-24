# FILE EXPORT LIBRARY

# Author    : Alfonsus Giovanni
# Version   : 0.1
# Date      : 18 Oktober 2025 

import csv
import os
from tkinter import messagebox

# Default Exported File Dir
home_dir = os.path.expanduser("~")
docs_folder = os.path.join(home_dir, "Documents")

class Exporter:
    def __init__(self):
        self.file_format = ".csv"
        self.default_filename = "Docs1"
        self.default_dir = "/home/alfonsus-giovanni/Documents"

        self.double_filename = False

    def check_filename(self, filename, filedir):
        existing_files = os.listdir(filedir)

        if filename in existing_files:
            return True

        else:
            return False

    def export_file(self, filename, sheet_data, sheet_info, filedir):
        if self.check_filename(filename, filedir) == True:
            messagebox.showinfo("Info", "Filename Already Exist")
            return

        file_path = os.path.join(filedir, filename)

        cust_info = ['Customer', sheet_info[0]]
        qty_info = ['Quantity', sheet_info[1]]
        total_weight_info = ['Total Weight', sheet_info[2]]
        total_price_info = ['Total Price', sheet_info[3]]
        header_info = ['No', 'Product', 'Price', 'Weight', 'Sub Price']

        info_length = 5
        total_length = info_length + len(sheet_data)

        data = [0] * total_length

        data[0] = cust_info
        data[1] = qty_info
        data[2] = total_weight_info
        data[3] = total_price_info
        data[4] = header_info

        for i in range(info_length, total_length):
            data[i] = sheet_data[i-info_length]

        try:
            with open(file_path, 'w', newline='', encoding="utf-8") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerows(data)

            messagebox.showinfo("Info", "Export Success!")

        except Exception as e:
            messagebox.showinfo("Info", f"Export Error: {e}")

MyExporter = Exporter()
