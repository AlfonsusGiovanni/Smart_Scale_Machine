import customtkinter as ctk
import tkinter as tk
import time
import datetime
import random
from tkinter import messagebox
from automatic_scale_machine import printer_handler as prhd
from automatic_scale_machine import serial_handler as sr
from automatic_scale_machine import system_control as sc
from automatic_scale_machine import rupiah as rp
from automatic_scale_machine import file_export as fe
from automatic_scale_machine import file_upload as fu

# Set Appearance Mode
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Menu Bar Frame Class -------------------------------------------------------------------------------------------------------------------------
class Menu_Bar_Frame(ctk.CTkFrame):
    def __init__(self, parent, left_frame):
        super().__init__(parent)

        self.left_frame = left_frame    # Left frame class control

        self.current_time = 0       # Current time
        self.current_date = 0       # Current date
        self.file_window = None     # File window top level
        self.setting_window = None  # Setting window top level

        # File Button
        self.file_menu_btn = ctk.CTkButton(
            self, 
            text="File", 
            text_color="white",
            font=("Arial", 14, "bold"),
            width=40, height=20,
            fg_color="gray15", hover_color="gray",
            command=self.show_file_widget
        )
        self.file_menu_btn.pack(side="left", padx=10)

        # Setting button
        self.setting_menu_btn = ctk.CTkButton(
            self, 
            text="Setting", 
            text_color="white",
            font=("Arial", 14, "bold"),
            width=60, height=20,
            fg_color="gray15", hover_color="gray",
            command=self.show_setting_widget
        )
        self.setting_menu_btn.pack(side="left", padx=(0,10))

        # Product info Button
        self.productinfo_menu_btn = ctk.CTkButton(
            self,
            text="Product Info", 
            text_color="white",
            font=("Arial", 14, "bold"),
            width=100, height=20,
            fg_color="gray15", hover_color="gray",
            command=self.show_productinfo_widget
        )
        self.productinfo_menu_btn.pack(side="left")

        # Time info label
        self.time_label = ctk.CTkLabel(
            self,
            height=25,
            fg_color="gray20",
            font=("Arial", 14, "bold"),
            text_color="white",
            corner_radius=10,
        )
        self.time_label.pack(side="right", padx=(0,10))

        # Date info label
        self.date_label = ctk.CTkLabel(
            self,
            height=25,
            fg_color="gray20",
            font=("Arial", 14, "bold"),
            text_color="white",
            corner_radius=10,
        )
        self.date_label.pack(side="right", padx=(0,10))

        # Update date and time
        self.update_date()
        self.update_time()

    # Clock time update funciton
    def update_time(self):
        self.current_time = time.strftime("%H:%M:%S")
        self.time_label.configure(text=(f"{self.current_time}"))
        self.after(1000, self.update_time)

    # Date time update function
    def update_date(self):
        self.current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        self.date_label.configure(text=(f"{self.current_date}"))
        self.date_label.after(6000, self.update_date)
    
    # File widget control function
    def show_file_widget(self):
        self.file_window = File_Window(self, self.left_frame)
        self.file_window.configure(fg_color="gray10")
        self.file_window.update_print_info()

    # Setting widget control function
    def show_setting_widget(self):
        self.setting_window = Setting_Window(self)
        self.setting_window.configure(fg_color="gray10")

    # Info widget control function
    def show_productinfo_widget(self):
        self.product_window = Product_Window(self)
        self.product_window.configure(fg_color="gray10")

# File Window Top Level ------------------------------------------------------------------------------------------------------------------------
class File_Window(ctk.CTkToplevel):
    def __init__(self, parent, left_frame):
        super().__init__(parent)

        self.geometry("300x200")
        self.title("File Window")
        self.resizable(width=False, height=False)

        # Window variable
        self.left_frame = left_frame
        self.tab_count = 3

        self.file_tab_menu = {}
        self.tab_label_frame = {}
        self.tab_btn_frame = {}

        self.tab_info_label = {}
        self.tab_infodata_label = {}

        self.tab_label1 = ["Customer Name\n\n", "File Name", "Select File"]
        self.tab_label2 = ["Total Price\n\n", "Export To"]
        self.tab_label3 = ["Manpower Cost"]

        self.cust_name = "No Name"
        self.total_price = "0,00"
        self.manpower_cost = "0,00"

        # Create file tab menu
        self.file_tab = ctk.CTkTabview(
            self,
            fg_color="gray10",
            bg_color="gray10",
            segmented_button_selected_color="steel blue",
            segmented_button_fg_color="gray15",
            segmented_button_unselected_color="gray15",
            corner_radius=10,
            command=self.update_print_info
        )
        self.file_tab.pack(side="top")

        self.file_tab_menu[0]= self.file_tab.add("Print")
        self.file_tab_menu[1]= self.file_tab.add("Export")
        self.file_tab_menu[2] = self.file_tab.add("Upload")

        # Create all file tab menu
        for i in range(self.tab_count):
            self.tab_label_frame[i] = ctk.CTkFrame(self.file_tab_menu[i], fg_color="gray15", corner_radius=10)
            self.tab_label_frame[i].pack(side="top", fill="x", pady=(0,12))

            self.tab_btn_frame[i] = ctk.CTkFrame(self.file_tab_menu[i], fg_color="gray10", corner_radius=10)
            self.tab_btn_frame[i].pack(side="top", fill="x")

        # Print tab information label
        self.tab_info_label[0] = ctk.CTkLabel(
            self.tab_label_frame[0],
            width=125,
            anchor="w",
            justify="left",
            font=("Arial", 14, "bold"),
            text_color="white",
            text=self.tab_label1[0] + self.tab_label2[0] + self.tab_label3[0]
        )
        self.tab_info_label[0].grid(row=0, column=0, padx=(10,0), pady=10)

        # Print data label
        self.print_data_label = ctk.CTkLabel(
            self.tab_label_frame[0],
            justify="left",
            font=("Arial", 14),
            text_color="white",
            text=f": {self.cust_name}\n\n: Rp. {self.total_price}\n\n: Rp. {self.manpower_cost}"
        )
        self.print_data_label.grid(row=0, column=1, pady=10)

        # Print button
        self.print_btn = ctk.CTkButton(
            self.tab_btn_frame[0],
            width=60,
            fg_color="steel blue",
            font=("Arial", 14, "bold"),
            text="PRINT",
            corner_radius=5,
            command=self.check_before_print
        )
        self.print_btn.pack(side="right")

        # Export tab information 1 frame
        self.export_label1_frame = ctk.CTkFrame(
            self.tab_label_frame[1],
            fg_color="gray15"
        )
        self.export_label1_frame.pack(side="top", fill="x", expand=True, pady=10)

        # Export filename label
        self.export_filename_label = ctk.CTkLabel(
            self.export_label1_frame,
            width=80,
            anchor="w",
            justify="left",
            font=("Arial", 14, "bold"),
            text_color="white",
            text=self.tab_label1[1]
        )
        self.export_filename_label.grid(row=0, column=0, padx=(10,0))

        # Export filename entry
        self.export_filename_entry = ctk.CTkEntry(
            self.export_label1_frame,
            width=180,
            placeholder_text=fe.MyExporter.default_filename
        )
        self.export_filename_entry.grid(row=0, column=1)

        # Export tab information 2 frame
        self.export_label2_frame = ctk.CTkFrame(
            self.tab_label_frame[1],
            fg_color="gray15"
        )
        self.export_label2_frame.pack(side="top", fill="x", expand=True, pady=(0,10))

        # Export directory info label
        self.export_dir_label = ctk.CTkLabel(
            self.export_label2_frame,
            width=80,
            anchor="w",
            justify="left",
            font=("Arial", 14, "bold"),
            text_color="white",
            text=self.tab_label2[1]
        )
        self.export_dir_label.grid(row=0, column=0, padx=(10,0))

        # Export dir entry
        self.export_dir_entry = ctk.CTkEntry(
            self.export_label2_frame,
            width=180,
            placeholder_text=fe.MyExporter.default_dir
        )
        self.export_dir_entry.grid(row=0, column=1)

        # Export button
        self.export_btn = ctk.CTkButton(
            self.tab_btn_frame[1],
            width=75,
            fg_color="steel blue",
            font=("Arial", 14, "bold"),
            text="EXPORT",
            corner_radius=5,
            command=self.check_before_export
        )
        self.export_btn.pack(side="right")

        # Browse export file folder
        self.browse_dir_btn = ctk.CTkButton(
            self.tab_btn_frame[1],
            width=75,
            fg_color="steel blue",
            font=("Arial", 14, "bold"),
            text="BROWSE",
            corner_radius=5,
            command=lambda: self.browse_dir(self.export_dir_entry)
        )
        self.browse_dir_btn.pack(side="right", padx=(10))

        # Upload tab information
        self.upload_file_label = ctk.CTkLabel(
            self.tab_label_frame[2],
            width=80,
            anchor="w",
            justify="left",
            font=("Arial", 14, "bold"),
            text_color="white",
            text=self.tab_label1[2]
        )
        self.upload_file_label.grid(row=0, column=0, padx=(10,0), pady=10)

        # Upload file entry
        self.upload_file_entry = ctk.CTkEntry(
            self.tab_label_frame[2],
            width=180,
        )
        self.upload_file_entry.grid(row=0, column=1)

        # Upload button
        self.upload_btn = ctk.CTkButton(
            self.tab_btn_frame[2],
            width=75,
            fg_color="steel blue",
            font=("Arial", 14, "bold"),
            text="UPLOAD",
            corner_radius=5,
        )
        self.upload_btn.pack(side="right")

    # Update Print Information Function
    def update_print_info(self):
        if self.file_tab.get() == "Print":
            self.cust_name = self.left_frame.sheet_cust_name[self.left_frame.current_sheet_num]
            self.total_price = self.left_frame.total_price_val[self.left_frame.current_sheet_num]

            unformatted_manpower_cost = sc.Mysystem.calc_manpower(self.left_frame.total_weight_val[self.left_frame.current_sheet_num])
            self.manpower_cost = rp.rupiah_format(unformatted_manpower_cost, with_prefix=False)

            if len(self.cust_name) > 0:
                self.print_data_label.configure(text=f": {self.cust_name}\n\n: Rp. {self.total_price}\n\n: Rp. {self.manpower_cost}")

            else:
                self.cust_name = "No Name"

        elif self.file_tab.get() == "Export":
            pass

        elif self.file_tab.get() == "Upload":
            pass

    # Check current sheet data before printing
    def check_before_print(self):
        if self.cust_name != "No Name":
            self.left_frame.print_sheet()
        
        else:
            self.destroy()
            messagebox.showinfo("Info", "Sheet Data Invalid!")

    # Check current sheet data before export
    def check_before_export(self):
        filename = self.export_filename_entry.get()
        if filename == "":
            filename = fe.MyExporter.default_filename + fe.MyExporter.file_format

        else:
            filename = filename + fe.MyExporter.file_format
        
        filedir = self.export_dir_entry.get()
        if filedir == "":
            filedir = fe.MyExporter.default_dir
        
        if self.cust_name != "No Name":
            self.left_frame.export_sheet(filename, filedir)
        
        else:
            self.destroy()
            messagebox.showinfo("Info", "Sheet Data Invalid!")

    # Browse file export directory
    def browse_dir(self, entry_widget):
        folder_path = tk.filedialog.askdirectory()
        if folder_path:
            entry_widget.delete(0, ctk.END)
            entry_widget.insert(0, folder_path)

# Setting Window Top Level ---------------------------------------------------------------------------------------------------------------------
class Setting_Window(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("300x200")
        self.title("Setting Window")
        self.resizable(width=False, height=False)

        # Setting window variable
        self.setting_tab_menu = {}
        self.tab_label_frame = {}
        self.tab_btn_frame = {}

        self.tab_count = 3

        # Create setting tab menu
        self.setting_tab = ctk.CTkTabview(
            self,
            fg_color="gray10",
            bg_color="gray10",
            segmented_button_fg_color="gray15",
            segmented_button_unselected_color="gray15",
            corner_radius=10,
            command=self.update_setting_info
        )
        self.setting_tab.pack(side="top")

        self.setting_tab_menu[0] = self.setting_tab.add("Product")
        self.setting_tab_menu[1] = self.setting_tab.add("Scale")
        self.setting_tab_menu[2] = self.setting_tab.add("Manpower")

        # Create all file tab menu
        for i in range(self.tab_count):
            self.tab_label_frame[i] = ctk.CTkFrame(self.setting_tab_menu[i], fg_color="gray15", corner_radius=10)
            self.tab_label_frame[i].pack(side="top", fill="x", pady=(0,12))

            self.tab_btn_frame[i] = ctk.CTkFrame(self.setting_tab_menu[i], fg_color="gray10", corner_radius=10)
            self.tab_btn_frame[i].pack(side="top", fill="x")

        # Product tab information 1 frame
        self.product_label1_frame = ctk.CTkFrame(
            self.tab_label_frame[0],
            fg_color="gray15"
        )
        self.product_label1_frame.pack(side="top", fill="x", expand=True, pady=10)

        # Product name info label
        self.product_name_label = ctk.CTkLabel(
            self.product_label1_frame,
            width=110,
            anchor="w",
            justify="left",
            font=("Arial", 14, "bold"),
            text_color="white",
            text="Product Name"
        )
        self.product_name_label.grid(row=0, column=0, padx=(10,0))

        # Product name entry
        self.product_name_entry = ctk.CTkEntry(
            self.product_label1_frame,
            width=150,
            placeholder_text="Input Name"
        )
        self.product_name_entry.grid(row=0, column=1)

        # Product tab information 2 frame
        self.product_label2_frame = ctk.CTkFrame(
            self.tab_label_frame[0],
            fg_color="gray15"
        )
        self.product_label2_frame.pack(side="top", fill="x", expand=True, pady=(0,10))

        # Product price info label
        self.product_price_label = ctk.CTkLabel(
            self.product_label2_frame,
            width=110,
            anchor="w",
            justify="left",
            font=("Arial", 14, "bold"),
            text_color="white",
            text="Product Price"
        )
        self.product_price_label.grid(row=0, column=0, padx=(10,0))

        # Product price entry
        self.product_price_entry = ctk.CTkEntry(
            self.product_label2_frame,
            width=150,
            placeholder_text="Input Price"
        )
        self.product_price_entry.grid(row=0, column=1)

        # Delete product button
        self.delete_product_btn = ctk.CTkButton(
            self.tab_btn_frame[0],
            width=75,
            fg_color="steel blue",
            font=("Arial", 14, "bold"),
            text="DELETE",
            corner_radius=5,
            command=self.delete_product
        )
        self.delete_product_btn.pack(side="right")

        # Add product button
        self.add_product_btn = ctk.CTkButton(
            self.tab_btn_frame[0],
            width=75,
            fg_color="steel blue",
            font=("Arial", 14, "bold"),
            text="ADD",
            corner_radius=5,
            command=self.add_product
        )
        self.add_product_btn.pack(side="right", padx=10)

        # Scale tab information 1 frame
        self.scale_info1_frame = ctk.CTkFrame(
            self.tab_label_frame[1],
            fg_color="gray15",
        )
        self.scale_info1_frame.pack(side="top", fill="x", expand=True, pady=10)

        # Scale setting value info
        self.scale_value_info = ctk.CTkLabel(
            self.scale_info1_frame,
            width=150,
            anchor="w",
            justify="left",
            font=("Arial", 14, "bold"),
            text_color="white",
            text="Rounded Weight",
        )
        self.scale_value_info.grid(row=0, column=0, padx=(10,0))

        # Scale setting value data
        self.scale_value_data = ctk.CTkLabel(
            self.scale_info1_frame,
            anchor="w",
            justify="left",
            font=("Arial", 14, "bold"),
            text_color="white",
            text=": 0.0Kg",
        )
        self.scale_value_data.grid(row=0, column=1)

        # Scale tab information 2 frame
        self.scale_info2_frame = ctk.CTkFrame(
            self.tab_label_frame[1],
            fg_color="gray15",
        )
        self.scale_info2_frame.pack(side="top", fill="x", expand=True, pady=(0,10))

        # Change scale setting info
        self.change_set_label = ctk.CTkLabel(
            self.scale_info2_frame,
            width=150,
            anchor="w",
            justify="left",
            font=("Arial", 14, "bold"),
            text_color="white",
            text="Set Rounded Weight",
        )
        self.change_set_label.grid(row=0, column=0, padx=(10,0))

        # Change scale setting entry
        self.change_weight_entry = ctk.CTkEntry(
            self.scale_info2_frame,
            width=110,
            placeholder_text="Input Value"
        )
        self.change_weight_entry.grid(row=0, column=1)

        # Confirm scale setting btn
        self.confirm_scale_btn = ctk.CTkButton(
            self.tab_btn_frame[1],
            width=80,
            fg_color="steel blue",
            font=("Arial", 14, "bold"),
            text="CONFIRM",
            corner_radius=5,
            command=self.change_rounded_weight
        )
        self.confirm_scale_btn.pack(side="right")

        # Manpower tab label 1 frame
        self.manpower_labe1_frame = ctk.CTkFrame(
            self.tab_label_frame[2],
            fg_color="gray15",
        )
        self.manpower_labe1_frame.pack(side="top", fill="x", expand=True, pady=10)

        # Manpower cost label
        self.manpower_cost_label = ctk.CTkLabel(
            self.manpower_labe1_frame,
            width=150,
            anchor="w",
            justify="left",
            font=("Arial", 14, "bold"),
            text_color="white",
            text="Manpower Cost",
        )
        self.manpower_cost_label.grid(row=0, column=0, padx=(10,0))

        # Manpower cost data
        self.manpower_cost_data = ctk.CTkLabel(
            self.manpower_labe1_frame,
            anchor="w",
            justify="left",
            font=("Arial", 14, "bold"),
            text_color="white",
            text=": Rp 0.0/Kg",
        )
        self.manpower_cost_data.grid(row=0, column=1)

        # Manpower tab label 2 frame
        self.manpower_label2_frame = ctk.CTkFrame(
            self.tab_label_frame[2],
            fg_color="gray15",
        )
        self.manpower_label2_frame.pack(side="top", fill="x", expand=True, pady=(0,10))

        # Change manpower cost label
        self.change_cost_label = ctk.CTkLabel(
            self.manpower_label2_frame,
            width=150,
            anchor="w",
            justify="left",
            font=("Arial", 14, "bold"),
            text_color="white",
            text="Set Manpower Cost",
        )
        self.change_cost_label.grid(row=0, column=0, padx=(10,0))

        # Change manpower cost entry
        self.change_cost_entry = ctk.CTkEntry(
            self.manpower_label2_frame,
            width=110,
            placeholder_text="Set Cost"
        )
        self.change_cost_entry.grid(row=0, column=1)

        # Confirm cost setting btn
        self.confirm_cost_btn = ctk.CTkButton(
            self.tab_btn_frame[2],
            width=80,
            fg_color="steel blue",
            font=("Arial", 14, "bold"),
            text="CONFIRM",
            corner_radius=5,
            command=self.change_manpower_cost
        )
        self.confirm_cost_btn.pack(side="right")
    
    # Add product function
    def add_product(self):
        input_name = self.product_name_entry.get()
        input_price = self.product_price_entry.get()
        product_name = {}
        product_price = {}
        
        # Check if name input is empty
        if input_name == "":
            messagebox.showinfo("Info", "Product Name Can't Empty!")
            return
        
        # Check if price input is empty
        if input_price == "":
            messagebox.showinfo("Info", "Product Price Can't Empty!")
            return
        
        # Load product
        product_list = sc.Mysystem.load_products()
        product_count = 0
        product_num = 0
        product_exist = False

        for product in product_list:
            product_name[product_count] = product["name"]
            product_price[product_count] = product["price"]
            product_count+=1
        
        # Check if product name is exist
        for i in range(product_count):
            if product_name[i] == input_name:
                product_exist = True
                break
            product_num+=1
        
        # Check if price is updated
        if product_exist and product_price[product_num] != float(input_price):
            sc.Mysystem.update_price(input_name, float(input_price))
            return

        # Check if price is not updated or get same product data
        elif product_exist and product_price[product_num] == float(input_price):
            messagebox.showinfo("Info", "Product Already Exist!")
            return
        
        # Check if new data added
        elif not product_exist:
           sc.Mysystem.add_product(input_name, float(input_price))

    # Update setting value function
    def update_setting_info(self):
        if self.setting_tab.get() == "Scale":
            setting_list = sc.Mysystem.load_setting()
            rounded_val = 0

            for setting_val in setting_list:
                rounded_val = setting_val["weight_val"]
            
            self.scale_value_data.configure(text=f": {rounded_val}Kg")

        elif self.setting_tab.get() == "Manpower":
            setting_list = sc.Mysystem.load_setting()
            cost_val = 0

            for setting_val in setting_list:
               cost_val = setting_val["manpower_val"]
               
            self.manpower_cost_data.configure(text=f": Rp. {cost_val}/Kg")

    # Delete product function
    def delete_product(self):
        input_name = self.product_name_entry.get()
        
        # Check if name input is empty
        if input_name == "":
            messagebox.showinfo("Info", "Product Name Can't Empty!")
            return
        
        sc.Mysystem.delete_product(input_name)

    # Change rounded weight value
    def change_rounded_weight(self):
        input_weight = self.change_weight_entry.get()

        if input_weight == "":
            messagebox.showinfo("Info", "Value Can't Empty!")
            return
        
        sc.Mysystem.change_weight_setting(float(input_weight))
        self.update_setting_info()
    
    # Change manpower cost value
    def change_manpower_cost(self):
        input_cost = self.change_cost_entry.get()

        if input_cost == "":
            messagebox.showinfo("Info", "Value Can't Empty!")
            return
        
        sc.Mysystem.change_manpower_setting(float(input_cost))
        self.update_setting_info()

# Product Info Window Top Level ----------------------------------------------------------------------------------------------------------------
class Product_Window(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("370x200")
        self.title("Product Window")
        self.resizable(width=False, height=False)

        # Product window variable
        self.row_num = sc.Mysystem.max_product
        self.column_num = 3

        self.column_width = [50, 125, 125]
        self.product_cell = [[0]*self.column_num for i in range(self.row_num)]

        # Product scroll frame
        self.product_scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="white",
            corner_radius=10,
        )
        self.product_scroll_frame.pack(side="top", fill="x", expand=True, padx=15, pady=15)

        # Product num title
        self.product_num_title = ctk.CTkLabel(
            self.product_scroll_frame,
            height=40, width=self.column_width[0],
            fg_color="gray75",
            font=("Arial", 14, "bold"),
            text="No",
            text_color="black",
        )
        self.product_num_title.grid(row=0, column=0, padx=(0,5), pady=(0,5))

        # Product name title
        self.product_name_title = ctk.CTkLabel(
            self.product_scroll_frame,
            height=40, width=self.column_width[1],
            fg_color="gray75",
            font=("Arial", 14, "bold"),
            text="Product Name",
            text_color="black",
        )
        self.product_name_title.grid(row=0, column=1, padx=(0,5), pady=(0,5))

        # Product price tittle
        self.product_price_title = ctk.CTkLabel(
            self.product_scroll_frame,
            height=40, width=self.column_width[2],
            fg_color="gray75",
            font=("Arial", 14, "bold"),
            text="Product Price\n(Rp)",
            text_color="black",
        )
        self.product_price_title.grid(row=0, column=2, pady=(0,5))

        self.show_product()

    # Show product function
    def show_product(self):
        # Load current saved product
        product_list = sc.Mysystem.load_products()
        product_data = [[0]*2 for i in range(self.row_num)]

        product_count = 0

        for product in product_list:
            product_data[product_count][0] = product["name"]
            product_data[product_count][1] = product["price"]
            product_count+=1

        # Create cell based on product count
        for i in range(product_count):
            # Product number
            self.product_cell[i][0] = ctk.CTkLabel(
                self.product_scroll_frame,
                height=25, width=self.column_width[0],
                fg_color="gray90",
                font=("Arial", 14),
                text=f"{i+1}",
                text_color="black"
            )
            self.product_cell[i][0].grid(row=i+1, column=0, padx=(0,5), pady=(0,5))

            # Product name & price
            for j in range(1, self.column_num):
                self.product_cell[i][j] = ctk.CTkLabel(
                    self.product_scroll_frame,
                    height=25, width=self.column_width[j],
                    fg_color="gray90",
                    font=("Arial", 14),
                    text=f"{product_data[i][j-1]}",
                    text_color="black"
                )
                self.product_cell[i][j].grid(row=i+1, column=j, padx=(0,5), pady=(0,5))
            
# Sheet Frame ----------------------------------------------------------------------------------------------------------------------------------
class Sheet_Ctrl_Frame(ctk.CTkFrame):
    def __init__(self, parent, left_frame):
        super().__init__(parent)
        self.configure(height=50, corner_radius=0, fg_color="gray15")

        # Sheet frame variables
        self.left_frame = left_frame

        # Sheet label
        self.sheet_label = ctk.CTkLabel(
            self,
            width=80, height=30,
            fg_color="gray20",
            font=("Arial", 14, "bold"),
            text="Sheet",
            text_color="white",
            corner_radius=5,
        )
        self.sheet_label.pack(side="left", padx=(10,0))

        # Delete sheet button
        self.delete_sheet_btn = ctk.CTkButton(
            self,
            width=30, height=30,
            fg_color="steel blue",
            font=("Arial", 14, "bold"),
            text="-",
            command=self.delete_sheet
        )
        self.delete_sheet_btn.pack(side="left", padx=(10,5))

        # Add sheet button
        self.add_sheet_btn = ctk.CTkButton(
            self,
            width=30, height=30,
            fg_color="steel blue",
            font=("Arial", 14, "bold"),
            text="+",
            command=self.add_sheet
        )
        self.add_sheet_btn.pack(side="left", padx=5)

    # Add sheet function handler
    def add_sheet(self):
        self.left_frame.create_new_sheet()

    # Delete sheet function handler
    def delete_sheet(self):
        self.left_frame.delete_sheet()

# Left Frame -----------------------------------------------------------------------------------------------------------------------------------
class Left_Frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Left frame variable
        self.max_sheet = 4
        self.max_row = 500
        self.max_column = 5

        self.current_sheet = ""         # Current opened sheet name
        self.current_sheet_num = 0      # Current opened sheet number
        self.sheet_num = 0              # Increment sheet number
        self.deleted_sheet = ""         # Deleted sheet name

        self.sheet_table = {}                           # Table for each sheet page
        self.sheet_info_frame = {}                      # Information frame for each sheet page
        self.info_frame1 = {}                           # Information frame 1 
        self.info_frame2 = {}                           # Information frame 2
        self.info_frame3 = {}                           # information frame 3
        self.sheet_cust_name = [""]*self.max_sheet      # Customer name for each sheet

        self.sheet_cell = [[[0]*self.max_column for r in range(self.max_row)] for s in range(self.max_sheet)]
        self.column_width = [50, 125, 100, 100, 125]    # Column 1-5 width

        self.starting_row = 10  # Starting row num
        self.total_column = 5   # Total column for sheet table
        self.current_row = [0]*self.max_sheet   # Current selected row for each sheet page
        self.row_counter = [0]*self.max_sheet   # Row counter for each sheet page

        self.product_qty_label = {}   # Total product quantity label for each sheet page
        self.total_weight_label = {}  # Total product total weight label for each sheet page
        self.total_price_label = {}   # Total product total price label for each sheet page

        self.product_qty_val = [0]*self.max_sheet
        self.total_weight_val = [0]*self.max_sheet
        self.total_price_val = [0]*self.max_sheet

        # Sheet Tab View
        self.sheet_tab = ctk.CTkTabview(
            self,
            fg_color="gray15",
            bg_color="gray10",
            segmented_button_selected_color="steel blue",
            segmented_button_fg_color="gray10",
            segmented_button_unselected_color="gray10",
            corner_radius=10,
            command=self.update_sheet
        )
        self.sheet_tab.pack(side="top", fill="both", expand=True, padx=(20,0), pady=(3,20))

    # Create new sheet function
    def create_new_sheet(self):
        sheet_name = f"Sheet{self.sheet_num+1}"
    
        if self.sheet_num < 4:
            tab = self.sheet_tab.add(sheet_name)

            # Add scrollable frame
            self.sheet_table[self.sheet_num] = ctk.CTkScrollableFrame(
                tab,
                height=350,
                fg_color="white",
                corner_radius=10
            )
            self.sheet_table[self.sheet_num].pack(side="top", fill="x", padx=(5,5), pady=(5,0))
            self.sheet_table[self.sheet_num].pack_propagate(False)

            # Add table tittle (num)
            self.column_num_title = ctk.CTkLabel(
                self.sheet_table[self.sheet_num],
                height=40, width=self.column_width[0],
                fg_color="gray75",
                font=("Arial", 14, "bold"),
                text="No",
                text_color="black"
            )
            self.column_num_title.grid(row=0, column=0, padx=(0,5))

            # Add table tittle (timestamp)
            self.column_time_title = ctk.CTkLabel(
                self.sheet_table[self.sheet_num],
                height=40, width=self.column_width[1],
                fg_color="gray75",
                font=("Arial", 14, "bold"),
                text="Product Name",
                text_color="black"
            )
            self.column_time_title.grid(row=0, column=1, padx=(0,5))

            # Add table tittle (product)
            self.column_product_title = ctk.CTkLabel(
                self.sheet_table[self.sheet_num],
                height=40, width=self.column_width[2],
                fg_color="gray75",
                font=("Arial", 14, "bold"),
                text="Price / Kg\n(Rp)",
                text_color="black"
            )
            self.column_product_title.grid(row=0, column=2, padx=(0,5))

            # Add table title (real weight)
            self.column_weight_title = ctk.CTkLabel(
                self.sheet_table[self.sheet_num],
                height=40, width=self.column_width[3],
                fg_color="gray75",
                font=("Arial", 14, "bold"),
                text="Weight\n(Kg)",
                text_color="black"
            )
            self.column_weight_title.grid(row=0, column=3, padx=(0,5))

            # Add table title (rounded weight)
            self.sheet_roundedweight_title = ctk.CTkLabel(
                self.sheet_table[self.sheet_num],
                height=40, width=self.column_width[4],
                fg_color="gray75",
                font=("Arial", 14, "bold"),
                text="Sub Price\n(Rp)",
                text_color="black"
            )
            self.sheet_roundedweight_title.grid(row=0, column=4, padx=(0,5))

            # Add starter sheet cell
            for i in range(0, self.starting_row):
                for j in range(0, self.total_column):
                    self.sheet_cell[self.sheet_num][i][j] = ctk.CTkLabel(
                        self.sheet_table[self.sheet_num],
                        height=25, width=self.column_width[j],
                        fg_color="gray90",
                        font=("Arial", 14),
                        text="",
                        text_color="black"
                    )
                    self.sheet_cell[self.sheet_num][i][j].grid(row=i+1, column=j, padx=(0,5), pady=(5,0))
                self.sheet_cell[self.sheet_num][i][0].configure(text=f"{i+1}")
            
            # Add sheet data information frame
            self.sheet_info_frame[self.sheet_num] = ctk.CTkFrame(
                tab,
                fg_color="gray20",
                corner_radius=10
            )
            self.sheet_info_frame[self.sheet_num].pack(side="top", fill="both", expand=True, padx=(5,5), pady=(20,5))

            # Add data frame 1
            self.info_frame1[self.sheet_num] = ctk.CTkFrame(
                self.sheet_info_frame[self.sheet_num],
                width=70, height=30,
                fg_color="gray20",
                corner_radius=0
            )
            self.info_frame1[self.sheet_num].pack(side="left", padx=(10,10))
            self.info_frame1[self.sheet_num].pack_propagate(False)

            # Add data frame 2
            self.info_frame2[self.sheet_num] = ctk.CTkFrame(
                self.sheet_info_frame[self.sheet_num],
                width=180, height=30,
                fg_color="gray20",
                corner_radius=0
            )
            self.info_frame2[self.sheet_num].pack(side="left", padx=(0,10))
            self.info_frame2[self.sheet_num].pack_propagate(False)

            # Add data frame 3
            self.info_frame3[self.sheet_num] = ctk.CTkFrame(
                self.sheet_info_frame[self.sheet_num],
                width=250, height=30,
                fg_color="gray20",
                corner_radius=0
            )
            self.info_frame3[self.sheet_num].pack(side="left", padx=(0,0))
            self.info_frame3[self.sheet_num].pack_propagate(False)

            # Add product quantity information label
            self.product_qty_label[self.sheet_num] = ctk.CTkLabel(
                self.info_frame1[self.sheet_num],
                font=("Arial", 16, "bold"),
                text="Qty: 0",
                text_color="white"
            )
            self.product_qty_label[self.sheet_num].pack(side="left")

            # Product total weight information label
            self.total_weight_label[self.sheet_num] = ctk.CTkLabel(
                self.info_frame2[self.sheet_num],
                font=("Arial", 16, "bold"),
                text="Total Weight: 0Kg",
                text_color="white"
            )
            self.total_weight_label[self.sheet_num].pack(side="left")

            # Product total price information label
            self.total_price_label[self.sheet_num] = ctk.CTkLabel(
                self.info_frame3[self.sheet_num],
                font=("Arial", 16, "bold"),
                text="Total Price: Rp. 0,00",
                text_color="white"
            )
            self.total_price_label[self.sheet_num].pack(side="left")

            self.sheet_tab.set(sheet_name)

        else:
            messagebox.showinfo("Info", "Sheet Limit!")

        self.update_sheet()
        self.sheet_num += 1

    # Delete sheet function
    def delete_sheet(self):
        if not self.current_sheet:
            messagebox.showinfo("Info", "No sheet selected!")
            return
        
        sheet_to_delete = int(self.current_sheet[5]) - 1 # Get number from "Sheet1", array[0] => array[1-1]

        # Remove current sheet
        if sheet_to_delete > 0:
            self.sheet_tab.delete(self.current_sheet)
            self.sheet_num = sheet_to_delete
            self.deleted_sheet = self.current_sheet

            self.current_sheet = "Sheet1"
            self.sheet_tab.set(self.current_sheet)

            messagebox.showinfo("Info", f"{self.deleted_sheet} Deleted!")
            return

        else:
            messagebox.showinfo("Info", "Can't Delete First Sheet!")
            return

    # Update current opened sheet
    def update_sheet(self):
        self.current_sheet = self.sheet_tab.get()
        self.current_sheet_num = int(self.current_sheet[5]) - 1 # Get number from "Sheet1", array[0] => array[1-1]

    # Create new column
    def add_row(self):
        for i in range(0,self.total_column):
            self.sheet_cell[self.current_sheet_num][self.current_row[self.current_sheet_num]][i] = ctk.CTkLabel(
                self.sheet_table[self.current_sheet_num],
                height=25, width=self.column_width[i],
                fg_color="gray90",
                font=("Arial", 14),
                text="",
                text_color="black"
            )
            self.sheet_cell[self.current_sheet_num][self.current_row[self.current_sheet_num]][i].grid(row=self.current_row[self.current_sheet_num]+1, column=i, padx=(0,5), pady=(5,0))
        self.sheet_cell[self.current_sheet_num][self.current_row[self.current_sheet_num]][0].configure(text=f"{self.current_row[self.current_sheet_num]+1}")

    # Add data to the sheet table
    def add_data(self, product_name, product_price, weight, cust_name):
        if len(self.sheet_cust_name[self.current_sheet_num]) == 0:
            self.sheet_cust_name[self.current_sheet_num] = cust_name
        
        else:
            if self.sheet_cust_name[self.current_sheet_num] != cust_name:
                messagebox.showinfo("Info", "Wrong customer data")
                return
            
        if self.current_row[self.current_sheet_num] >= self.starting_row:
            self.add_row()

        self.sheet_cell[self.current_sheet_num][self.current_row[self.current_sheet_num]][1].configure(text=f"{product_name}")
        self.sheet_cell[self.current_sheet_num][self.current_row[self.current_sheet_num]][2].configure(text=f"{product_price}")

        self.processed_weight = sc.Mysystem.process_weight(weight)
        self.sheet_cell[self.current_sheet_num][self.current_row[self.current_sheet_num]][3].configure(text=f"{self.processed_weight}")

        self.sub_price = rp.rupiah_format(product_price * self.processed_weight, with_prefix=False)
        self.sheet_cell[self.current_sheet_num][self.current_row[self.current_sheet_num]][4].configure(text=f"Rp. {self.sub_price}")

        self.current_row[self.current_sheet_num]+=1
        self.update_product_info()

    # Delete last row table data
    def delete_data(self):
        if self.current_row[self.current_sheet_num] > 0:
            self.sheet_cell[self.current_sheet_num][self.current_row[self.current_sheet_num]-1][1].configure(text="")
            self.sheet_cell[self.current_sheet_num][self.current_row[self.current_sheet_num]-1][2].configure(text="")
            self.sheet_cell[self.current_sheet_num][self.current_row[self.current_sheet_num]-1][3].configure(text="")
            self.sheet_cell[self.current_sheet_num][self.current_row[self.current_sheet_num]-1][4].configure(text="")

        else:
            self.current_row[self.current_sheet_num] = 0
            messagebox.showinfo("Info", "Can't Delete Row")
            return
        
        self.current_row[self.current_sheet_num]-=1
        self.update_product_info()
        messagebox.showinfo("Info", f"Row{self.current_row[self.current_sheet_num]+1} Deleted")
    
    # Update sheet product information
    def update_product_info(self):
        # Update product quantity
        self.product_qty_val[self.current_sheet_num] = self.current_row[self.current_sheet_num]
        self.product_qty_label[self.current_sheet_num].configure(text=f"Qty: {self.current_row[self.current_sheet_num]}")

        # Update product total weight and total price
        weight_sum = 0
        price_sum = 0
        for i in range(self.current_row[self.current_sheet_num]):
            weight_sum += int(self.sheet_cell[self.current_sheet_num][i][3].cget("text"))
            price_sum += int(rp.rupiah_deformat(self.sheet_cell[self.current_sheet_num][i][4].cget("text")))

        self.total_weight_val[self.current_sheet_num] = weight_sum
        self.total_price_val[self.current_sheet_num] = rp.rupiah_format(price_sum, with_prefix=True)

        self.total_weight_label[self.current_sheet_num].configure(text=f"Total Weight: {self.total_weight_val[self.current_sheet_num]}Kg")
        self.total_price_label[self.current_sheet_num].configure(text=f"Total Price: {self.total_price_val[self.current_sheet_num]}")

    # Print current sheet 
    def print_sheet(self):
        print("Printing Struct...")

    # Export current sheet to csv
    def export_sheet(self, file_name, file_dir):
        cell_data = [[0]*self.max_column for r in range(self.current_row[self.current_sheet_num])]

        for i in range(self.current_row[self.current_sheet_num]):
            for j in range(self.max_column):
                cell_data[i][j] = self.sheet_cell[self.current_sheet_num][i][j].cget("text")

        info = [
            self.sheet_cust_name[self.current_sheet_num], 
            self.current_row[self.current_sheet_num],
            self.total_weight_val[self.current_sheet_num],
            self.total_price_val[self.current_sheet_num],
        ]

        fe.MyExporter.export_file(file_name, cell_data, info, file_dir)

# Right Frame ----------------------------------------------------------------------------------------------------------------------------------
class Right_Frame(ctk.CTkFrame):
    def __init__(self, parent, left_frame):
        super().__init__(parent)

        # Right frame variable
        self.left_frame = left_frame
        self.weight = 0
        self.selected_product = "No Product"
        self.selected_product_price = "0"
        self.customer_name = "No Name"

        self.product_name_info =    f"Product Name\n\n"
        self.product_price_info =   f"Product Price\n\n"
        self.customer_name_info =   f"Customer Name"

        # Weight label
        self.weight_label = ctk.CTkLabel(
            self, 
            height=180,
            fg_color="gray15",
            font=("Arial", 80, "bold"),
            text="",
            text_color="white",
            corner_radius=10,
        )
        self.weight_label.pack(side="top", fill="x", padx=20, pady=20)

        # Information bar frame
        self.info_bar = ctk.CTkFrame(
            self,
            height=50,
            fg_color="gray10",
            corner_radius=0
        )
        self.info_bar.pack(side="top", fill="x")

        # Select product option menu
        self.product_box = ctk.CTkOptionMenu(
            self.info_bar,
            height=40, width=140,
            fg_color="white",
            button_color="gray75",
            button_hover_color="gray70",
            text_color="black",
            font=("Arial", 14, "bold"),
            dropdown_font=("Arial", 14, "bold"),
            corner_radius=10,
            dynamic_resizing=False,
            values=self.get_products(),
            command=self.update_product
        )
        self.product_box.grid(row=0, column=0, padx=(20,0))
        self.product_box.set("Product")

        # Customer name entry box
        self.cust_name_entry = ctk.CTkEntry(
            self.info_bar,
            height=40, width=150,
            font=("Arial", 14, "bold"),
            placeholder_text="Customer Name",
            placeholder_text_color="gray50",
            corner_radius=10,
        )
        self.cust_name_entry.grid(row=0, column=1, padx=(20,0))

        # Name confirm button
        self.name_confirm = ctk.CTkButton(
            self.info_bar,
            height=40, width=40,
            font=("Arial", 14, "bold"),
            text="Add",
            corner_radius=10,
            command=self.update_cust_name
        )
        self.name_confirm.grid(row=0, column=2, padx=(20,20))

        # Information title label
        self.info_label = ctk.CTkLabel(
            self,
            height=14, width=100,
            font=("Arial", 14, "bold"),
            text="INFORMATION",
            text_color="white",
        )
        self.info_label.pack(side="top", pady=(20,5))

        # Information frame
        self.info_frame = ctk.CTkFrame(
            self,
            width=380, height=116,
            fg_color="gray15",
            corner_radius=10,
        )
        self.info_frame.pack(side="top", padx=20, fill="x")

        # Product info label
        self.product_info_label = ctk.CTkLabel(
            self.info_frame,
            width=120, height=14,
            font=("Arial", 14, "bold"),
            anchor="w",
            justify="left",
            text=self.product_name_info+self.product_price_info+self.customer_name_info,
            text_color="white"
        )
        self.product_info_label.grid(row=0, column=0, padx=(20,0), pady=(10,10))

        # Product data label
        self.info_data_label = ctk.CTkLabel(
            self.info_frame,
            height=14,
            font=("Arial", 14),
            justify="left",
            text=f": {self.selected_product}\n\n: Rp. {self.selected_product_price}\n\n: {self.customer_name}",
            text_color="white"
        )
        self.info_data_label.grid(row=0, column=1, padx=(10,0), pady=(10,10))

        # Buttom button frame
        self.button_frame = ctk.CTkFrame(
            self,
            fg_color="gray10"
        )
        self.button_frame.pack(side="top", pady=(20,20), fill="x")

        # Confirm weight button
        self.confirm_button = ctk.CTkButton(
            self.button_frame,
            width=180, height=90,
            fg_color="mediumseagreen",
            hover_color="seagreen",
            font=("Arial", 20, "bold"),
            text="CONFIRM",
            corner_radius=10,
            command=self.confirm_data
        )
        self.confirm_button.pack(side="left", padx=(20,0))

        # Delete weight button
        self.delete_button = ctk.CTkButton(
            self.button_frame,
            width=180, height=90,
            fg_color="firebrick1",
            hover_color="firebrick3",
            font=("Arial", 20, "bold"),
            text="DELETE",
            corner_radius=10,
            command=self.delete_confirmed
        )
        self.delete_button.pack(side="right", padx=(0,20))

        self.update_weight()
 
    # Update weight function
    def update_weight(self):
        # Test only
        random_var = random.uniform(35.0, 60.0)
        self.weight = random_var
        self.weight_label.configure(text=f"{self.weight:.2f} Kg")

    # Get product list from stored product file
    def get_products(self):
        self.product_list = sc.Mysystem.load_products()
        return [p["name"] for p in self.product_list]
    
    # Update selected product function
    def update_product(self, choice):
        self.selected_product = choice # Get product choice

        self.get_products()
        
        for product in self.product_list:
            if product["name"] == self.selected_product:
                self.selected_product_price = product["price"]
        self.info_data_label.configure(text=f": {self.selected_product}\n\n: Rp. {self.selected_product_price}\n\n: {self.customer_name}")

    # Update customer name
    def update_cust_name(self):
        self.customer_name = self.cust_name_entry.get()

        if self.customer_name != "":
            self.info_data_label.configure(text=f": {self.selected_product}\n\n: Rp. {self.selected_product_price}\n\n: {self.customer_name}")

    # Send confirmed data
    def confirm_data(self):
        if self.selected_product == "No Product":
            messagebox.showinfo("Info", "Please Select Product!")
            return
        
        elif self.customer_name == "No Name":
            messagebox.showinfo("Info", "Please Add Customer Name!")
            return

        else:
            self.left_frame.add_data(self.selected_product,self.selected_product_price,self.weight,self.customer_name)

        # Test only
        self.update_weight()

    def delete_confirmed(self):
        self.left_frame.delete_data()

# App Class ------------------------------------------------------------------------------------------------------------------------------------
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # App Setting
        self.geometry("1024x600")
        self.title("Integrated Scale System - UD. Soenarto YS")
        self.resizable(width=False, height=False)

        # Top Frame
        self.top_frame = ctk.CTkFrame(self, corner_radius=0)
        self.top_frame.pack(side="top")

        # Middle Frame
        self.middle_frame = ctk.CTkFrame(self, corner_radius=0)
        self.middle_frame.pack(side="top")

        # Bottom Frame
        self.bottom_frame = ctk.CTkFrame(self, height=40, corner_radius=0)
        self.bottom_frame.pack(side="top", fill="x")
        self.bottom_frame.pack_propagate(False)

        # Left Main Frame
        self.left_frame = Left_Frame(self.middle_frame)
        self.left_frame.configure(width=604, height=520, corner_radius=0, fg_color="gray10")
        self.left_frame.pack(side="left")
        self.left_frame.pack_propagate(False)

        # Right Main Frame
        self.right_frame = Right_Frame(self.middle_frame, self.left_frame)
        self.right_frame.configure(width=604, height=520, corner_radius=0, fg_color="gray10")
        self.right_frame.pack(side="right")
        self.right_frame.pack_propagate(False)

        # Menu Bar Frame
        self.menu_bar = Menu_Bar_Frame(self.top_frame, self.left_frame)
        self.menu_bar.configure(width=1024, height=40, corner_radius=0, fg_color="gray15")
        self.menu_bar.pack(side="left")
        self.menu_bar.pack_propagate(False)

        # Sheet Control Frame
        self.sheet_frame = Sheet_Ctrl_Frame(self.bottom_frame, self.left_frame)
        self.sheet_frame.pack(side="bottom", fill="x")
        self.sheet_frame.pack_propagate(False)
        self.sheet_frame.add_sheet()

app = App()
app.mainloop()