import customtkinter as ctk
import tkinter as tk
import time
import datetime
import random
from tkinter import messagebox
from automatic_scale_machine import printer_handler as prhd
from automatic_scale_machine import product_control as pctl
from automatic_scale_machine import serial_handler as sr
from automatic_scale_machine import weight_rounder as wr

# Set Appearance Mode
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Menu Bar Frame Class -------------------------------------------------------------------------------------------------------------------------
class Menu_Bar_Frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.file_btn_counter = 0
        self.setting_btn_counter = 0
        self.current_time = 0
        self.current_date = 0

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
        self.setting_menu_btn.pack(side="left",)

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
        self.file_btn_counter += 1

        if(self.file_btn_counter<2):
            print("File Widget Open")
        else:
            self.file_btn_counter = 0
            print("File Widget Closed")

    # File widget control function
    def show_setting_widget(self):
        self.setting_btn_counter += 1
        
        if(self.setting_btn_counter<2):
            print("Setting Widget Open")
        else:
            self.setting_btn_counter = 0
            print("Setting Widget Closed")

# Sheet Frame ----------------------------------------------------------------------------------------------------------------------------------
class Sheet_Frame(ctk.CTkFrame):
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
            text="+",
            font=("Arial", 14, "bold"),
            width=30, height=30,
            fg_color="steel blue",
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
    def __init__(self, parent, menu_frame):
        super().__init__(parent)

        # Left frame variable
        self.menu_frame = menu_frame
        self.max_sheet = 4
        self.max_row = 500
        self.max_column = 5

        self.current_sheet = ""
        self.sheet_num = 0
        self.current_sheet_num = 0
        self.deleted_sheet = ""

        self.sheet_table = {}
        self.sheet_info_frame = {}
        self.info_frame1 = {}
        self.info_frame2 = {}
        self.info_frame3 = {}
        self.sheet_cust_name = {}
        self.sheet_cell = [[[0]*self.max_column for r in range(self.max_row)] for s in range(self.max_sheet)]

        self.column_width = [50, 125, 100, 100, 125]

        self.starting_row = 10
        self.current_row = 0
        self.row_counter = 0
        self.total_column = 5

        # Sheet Tab View
        self.sheet_tab = ctk.CTkTabview(
            self,
            fg_color="gray15",
            bg_color="gray10",
            segmented_button_fg_color="gray10",
            segmented_button_unselected_color="gray10",
            corner_radius=10,
            command=self.update_sheet
        )
        self.sheet_tab.pack(side="top", fill="both", expand=True, padx=(20,0), pady=(3,20))

    # Create new sheet function
    def create_new_sheet(self):
        self.sheet_num += 1
        sheet_name = f"Sheet{self.sheet_num}"
    
        if self.sheet_num <= 4:
            tab = self.sheet_tab.add(sheet_name)
            self.sheet_tab.move(self.sheet_num-1, sheet_name)

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
                fg_color="white",
                corner_radius=10
            )
            self.sheet_info_frame[self.sheet_num].pack(side="top", fill="both", expand=True, padx=(5,5), pady=(15,5))

            # Add data frame 1
            self.info_frame1[self.sheet_num] = ctk.CTkFrame(
                self.sheet_info_frame[self.sheet_num],
                width=150, height=30,
                fg_color="red",
                corner_radius=0
            )
            self.info_frame1[self.sheet_num].pack(side="left", padx=(10,20))
            self.info_frame1[self.sheet_num].pack_propagate(False)

            # Add data frame 2
            self.info_frame2[self.sheet_num] = ctk.CTkFrame(
                self.sheet_info_frame[self.sheet_num],
                width=150, height=30,
                fg_color="green",
                corner_radius=0
            )
            self.info_frame2[self.sheet_num].pack(side="left", padx=(0,20))
            self.info_frame2[self.sheet_num].pack_propagate(False)

            # Add data frame 3
            self.info_frame3[self.sheet_num] = ctk.CTkFrame(
                self.sheet_info_frame[self.sheet_num],
                width=150, height=30,
                fg_color="blue",
                corner_radius=0
            )
            self.info_frame3[self.sheet_num].pack(side="left", padx=(0,0))
            self.info_frame3[self.sheet_num].pack_propagate(False)

            # Add product quantity information label
            self.product_qty = ctk.CTkLabel(
                self.info_frame1[self.sheet_num],
                font=("Arial", 16, "bold"),
                text="Qty:",
                text_color="black"
            )
            self.product_qty.pack(side="left")

            # Product total weight information label
            self.total_weight = ctk.CTkLabel(
                self.info_frame2[self.sheet_num],
                font=("Arial", 16, "bold"),
                text="Total Weight:",
                text_color="black"
            )
            self.total_weight.pack(side="left")

            # Product total price information label
            self.total_price = ctk.CTkLabel(
                self.info_frame3[self.sheet_num],
                font=("Arial", 16, "bold"),
                text="Total Price:",
                text_color="black"
            )
            self.total_price.pack(side="left")

        else:
            messagebox.showinfo("Info", "Sheet Limit!")
        
        self.update_sheet()

    # Delete sheet function
    def delete_sheet(self):
        if not self.current_sheet:
            messagebox.showinfo("Info", "No sheet selected!")
            return
        
        sheet_to_delete = int(self.current_sheet[5])

        # Remove current sheet
        if sheet_to_delete > 1:
            self.sheet_tab.delete(self.current_sheet)
            self.sheet_num = sheet_to_delete-1
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
        self.current_sheet_num = int(self.current_sheet[5])

    # Create new column
    def add_column(self):
        for i in range(0,self.total_column):
            self.sheet_cell[self.current_sheet_num][self.current_row][i] = ctk.CTkLabel(
                self.sheet_table[self.sheet_num],
                height=25, width=self.column_width[i],
                fg_color="gray90",
                font=("Arial", 14),
                text="",
                text_color="black"
            )
            self.sheet_cell[self.current_sheet_num][self.current_row][i].grid(row=self.current_row+1, column=i, padx=(0,5), pady=(5,0))
        self.sheet_cell[self.current_sheet_num][self.current_row][0].configure(text=f"{self.current_row+1}")

    # Add data to the sheet table
    def add_data(self, product_name, product_price, weight, cust_name):
        if self.current_row >= self.starting_row:
            self.add_column()

        self.sheet_cell[self.current_sheet_num][self.current_row][1].configure(text=f"{product_name}")
        self.sheet_cell[self.current_sheet_num][self.current_row][2].configure(text=f"{product_price}")

        self.processed_weight = wr.Mysetting.process_value(weight)
        self.sheet_cell[self.current_sheet_num][self.current_row][3].configure(text=f"{self.processed_weight}")

        self.total_price = product_price * self.processed_weight
        self.sheet_cell[self.current_sheet_num][self.current_row][4].configure(text=f"{self.total_price}")

        self.current_row+=1

    # Delete last row table data
    def delete_data(self):
        if self.current_row > 0:
            self.sheet_cell[self.current_sheet_num][self.current_row-1][1].configure(text="")
            self.sheet_cell[self.current_sheet_num][self.current_row-1][2].configure(text="")
            self.sheet_cell[self.current_sheet_num][self.current_row-1][3].configure(text="")
            self.sheet_cell[self.current_sheet_num][self.current_row-1][4].configure(text="")

        else:
            self.current_row = 0
            messagebox.showinfo("Info", "Can't Delete Row")
            return
        
        self.current_row-=1
        messagebox.showinfo("Info", f"Row{self.current_row+1} Deleted")

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

        self.product_name_info =    f"Product Name      = \n\n"
        self.product_price_info =   f"Product Price       = \n\n"
        self.customer_name_info =   f"Customer Name   ="

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
            text_color="gray50",
            font=("Arial", 14, "bold"),
            dropdown_font=("Arial", 14, "bold"),
            corner_radius=10,
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
            height=14,
            font=("Arial", 14),
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
            text=f"{self.selected_product}\n\nRp. {self.selected_product_price}\n\n{self.customer_name}",
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
        self.product_list = pctl.Myproduct.load_products()
        return [p["name"] for p in self.product_list]
    
    # Update selected product function
    def update_product(self, choice):
        self.selected_product = choice # Get product choice

        self.get_products()
        
        for product in self.product_list:
            if product["name"] == self.selected_product:
                self.selected_product_price = product["price"]
        self.info_data_label.configure(text=f"{self.selected_product}\n\nRp. {self.selected_product_price}\n\n{self.customer_name}")

    # Update customer name
    def update_cust_name(self):
        self.customer_name = self.cust_name_entry.get()

        if self.customer_name != "":
            self.info_data_label.configure(text=f"{self.selected_product}\n\nRp. {self.selected_product_price}\n\n{self.customer_name}")

    # Send confirmed data
    def confirm_data(self):
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
        self.title("Smart Weighting System")
        self.resizable(width=False, height=False)

        # Top Frame
        self.top_frame = ctk.CTkFrame(self, corner_radius=0)
        self.top_frame.pack(side="top")

        # Menu Bar Frame
        self.menu_bar = Menu_Bar_Frame(self.top_frame)
        self.menu_bar.configure(width=1024, height=40, corner_radius=0, fg_color="gray15")
        self.menu_bar.pack(side="left")
        self.menu_bar.pack_propagate(False)

        # Middle Frame
        self.middle_frame = ctk.CTkFrame(self, corner_radius=0)
        self.middle_frame.pack(side="top")

        # Left Main Frame
        self.left_frame = Left_Frame(self.middle_frame, self.menu_bar)
        self.left_frame.configure(width=604, height=520, corner_radius=0, fg_color="gray10")
        self.left_frame.pack(side="left")
        self.left_frame.pack_propagate(False)

        # Right Main Frame
        self.right_frame = Right_Frame(self.middle_frame, self.left_frame)
        self.right_frame.configure(width=604, height=520, corner_radius=0, fg_color="gray10")
        self.right_frame.pack(side="right")
        self.right_frame.pack_propagate(False)

        # Bottom Frame
        self.bottom_frame = ctk.CTkFrame(self, height=40, corner_radius=0)
        self.bottom_frame.pack(side="top", fill="x")
        self.bottom_frame.pack_propagate(False)

        # Sheet Frame
        self.sheet_frame = Sheet_Frame(self.bottom_frame, self.left_frame)
        self.sheet_frame.pack(side="bottom", fill="x")
        self.sheet_frame.pack_propagate(False)
        self.sheet_frame.add_sheet()

app = App()
app.mainloop()