# FILE EXPORT LIBRARY

# Author    : Alfonsus Giovanni
# Version   : 0.1
# Date      : 18 Oktober 2025 

import csv
import os

# Default Exported File Dir
home_dir = os.path.expanduser("~")
docs_folder = os.path.join(home_dir, "Documents")

class Exporter:
    def __init__(self):
        self.default_filename = "Docs1.csv"
        self.default_dir = "/home/alfonsus-giovanni/Documents"

    def check_filename(self):
        pass

    def export_file(self, sheet_name, sheet_data, sheet_info, dir):
        file_path = os.path.join(self.default_dir, self.default_filename)
            

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

        except Exception as e:
            print(f"Error: {e}")

MyExporter = Exporter()
