# SYSTEM SETTING LIBRARY

# Author    : Alfonsus Giovanni
# Version   : 0.1
# Date      : 10 Oktober 2025  

import json
import os
from tkinter import messagebox

product_file_dir = "data/products.json"
setting_file_dir = "data/system_setting.json"

class Error_Code:
    NO_ERR = 0x00

    FILE_PATH_ERR = 0x01
    FILE_LOAD_ERR = 0x02
    FILE_RETURN_ERR = 0x03

    PRODUCT_NAME_INVALID = 0x04
    SET_VALUE_INVALID = 0x05
    PRODUCT_NOT_FOUND = 0x06

class App_System:
    def __init__(self, product_file, setting_file):
        self.product_file = product_file
        self.product_list = self.load_products()

        self.setting_file = setting_file
        self.setting_data = self.load_setting()

        self.system_code = Error_Code.NO_ERR
        self.max_product = 10

    # Load Saved Products Function
    def load_products(self):
        if not os.path.exists(self.product_file):
            self.system_code = Error_Code.FILE_PATH_ERR
            return []
        
        try:
            with open(self.product_file, "r") as f:
                return json.load(f)
            
        except json.JSONDecodeError:
            self.system_code = Error_Code.FILE_LOAD_ERR
            return []
        
    # Load Saved System Setting Function
    def load_setting(self):
        if not os.path.exists(self.setting_file):
            self.system_code = Error_Code.FILE_PATH_ERR
            return []
        
        try:
            with open(self.setting_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            self.system_code = Error_Code.FILE_LOAD_ERR
            return []

    # Change Weight Setting Value Function
    def change_weight_setting(self, set_value):        
        self.setting_data = self.load_setting()

        for variable in self.setting_data:
            variable["weight_val"] = set_value
            self.save_setting()
            messagebox.showinfo("Info", "Change Value Success!")
            break

    # Change Manpower Setting Value Function
    def change_manpower_setting(self, set_value):
        self.setting_data = self.load_setting()

        for variable in self.setting_data:
            variable["manpower_val"] = set_value
            self.save_setting()
            messagebox.showinfo("Info", "Change Value Success!")
            break

    # Process Weight Function
    def process_weight(self, weight_input):
        round_value = int(weight_input)
        comma_value = weight_input - round_value
        rounded_value = 0

        get_value = [p["weight_val"] for p in self.setting_data]
        value = get_value[0]

        if comma_value < value:
            rounded_value = int(weight_input) - 1
        else:
            rounded_value = round_value

        return rounded_value
    
    # Calculate Total Manpower Cost Function
    def calc_manpower(self, weight_sum):
        get_value = [p["manpower_val"] for p in self.setting_data]
        return weight_sum * get_value[0]
    
    # Save Product File Function
    def save_product(self):
        with open(self.product_file, "w") as f:
            json.dump(self.product_list, f, indent=4)

    # Save Setting File Function
    def save_setting(self):
        with open(self.setting_file, "w") as f:
            json.dump(self.setting_data, f, indent=4)

    # Add Product Function
    def add_product(self, input_name, input_price):
        name = input_name
        price = input_price
    
        self.product_list.append({"name": name, "price": price})
        self.save_product()
        messagebox.showinfo("Info", "Product Added!")

    # Delete Product Function
    def delete_product(self, product_name):
        target_num = 0

        for product in self.product_list:
            if product_name == product["name"]:
                break
            target_num+=1

        index = int(target_num)
        
        if 0 <= index < len(self.product_list):
            self.product_list.pop(index)
            self.save_product()
            messagebox.showinfo("Info", "Product Deleted!")

        else:
            messagebox.showinfo("Info", "Product Not Found!")
    
    # Update Product Price Function
    def update_price(self, update_name, new_price):
        self.product_list = self.load_products()
        for product in self.product_list:
            if product["name"] == update_name:
                product["price"] = new_price
                self.save_product()
                messagebox.showinfo("Info", "Price Updated!")
                break

            else:
                messagebox.showinfo("Info", "Product Not Found!")

Mysystem = App_System(product_file_dir, setting_file_dir)