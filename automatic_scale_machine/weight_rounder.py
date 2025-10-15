# PRODUCT WEIGHT ROUNDER LIBRARY

# Author    : Alfonsus Giovanni
# Version   : 0.1
# Date      : 14 Oktober 2025  

import json
import os

file_dir = "data/rounded_set.json" # Directory file JSON

class Weight_Rounder:
    def __init__(self, file):
        self.setting_file = file
        self.setting_value = self.load_setting()

    def load_setting(self):
        if not os.path.exists(self.setting_file):
            self.setting_err = 0x01 # product file load error
            return []
        
        try:
            with open(self.setting_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            self.setting_err = 0x02 # return file decode error
            return []
        
    def save_setting(self):
        with open(self.setting_file, "w") as f:
            json.dump(self.setting_value, f, indent=4)

    def change_setting(self, set_value):        
        self.setting_value = self.load_setting()

        for variable in self.setting_value:
            variable["value"] = set_value
            self.save_setting()
            break

    def process_value(self, weight_input):
        round_value = int(weight_input)
        comma_value = weight_input - round_value
        rounded_value = 0

        get_value = [p["value"] for p in self.setting_value]
        value = get_value[0]

        if comma_value < value:
            rounded_value = int(weight_input) - 1
        else:
            rounded_value = round_value

        return rounded_value

Mysetting = Weight_Rounder(file_dir)