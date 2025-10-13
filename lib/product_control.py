# PRODUCT CONTROL LIBRARY

# Author    : Alfonsus Giovanni
# Version   : 0.1
# Date      : 10 Oktober 2025  

import json
import os

file_dir = "dir/products.json" # Directory file JSON

class product:
    def __init__(self, file):
        self.product_ctrl_return = 0
        self.product_file = file # Saved file directory
        self.product_list = self.load_products() # Save JSON format to string array variable

    def load_products(self):
        if not os.path.exists(self.product_file):
            self.product_ctrl_return = 0x01 # product file load error
            return []
        
        try:
            with open(self.product_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            self.product_ctrl_return = 0x02 # return file decode error
            return []
        
    def save_product(self):
        with open(self.product_file, "w") as f:
            json.dump(self.product_list, f, indent=4)

    def add_product(self, input_name, input_price):
        name = input_name
        
        if not name:
            self.product_ctrl_return = 0x03 # return name empty error
            return
        
        try:
            price = input_price
        except ValueError:
            self.product_ctrl_return = 0x04 # return invalid input value error
            return
        
        self.product_list.append({"name": name, "price": price})
        self.save_product()
        self.product_ctrl_return = 0x05 # return save success

    def delete_product(self, product_num):
        if not self.product_list:
            return

        target = product_num
        index = int(target) - 1
        
        if 0 <= index < len(self.product_list):
            self.product_list.pop(index)
            self.save_product()
            self.product_ctrl_return = 0x06 # return product delete success
        else:
            self.product_ctrl_return = 0x07 # return product number error
    
    def update_price(self, update_name, new_price):
        self.product_list = self.load_products()
        for product in self.product_list:
            if product["name"] == update_name:
                product["price"] = new_price
                break

            else:
                self.product_ctrl_return = 0x08 # return update product not found

Myproduct = product(file_dir)