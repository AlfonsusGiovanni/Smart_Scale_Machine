import customtkinter as ctk
from tkinter import messagebox


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class SheetManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CustomTkinter Sheet Manager")
        self.geometry("900x600")

        # Data structures
        self.sheets = {}
        self.current_sheet = None
        self.sheet_count = 0

        # Layout configuration
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Toolbar (top)
        self.toolbar_frame = ctk.CTkFrame(self, height=50)
        self.toolbar_frame.grid(row=0, column=0, sticky="ew")
        self.toolbar_frame.grid_columnconfigure((0, 1), weight=0)
        self.toolbar_frame.grid_columnconfigure(2, weight=1)

        # Add and Delete Buttons
        self.add_btn = ctk.CTkButton(self.toolbar_frame, text="Add Sheet", command=self.add_sheet)
        self.add_btn.grid(row=0, column=0, padx=10, pady=10)

        self.del_btn = ctk.CTkButton(self.toolbar_frame, text="Delete Sheet", command=self.delete_sheet)
        self.del_btn.grid(row=0, column=1, padx=10, pady=10)

        # Sheet content frame (center)
        self.sheet_frame = ctk.CTkFrame(self)
        self.sheet_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Bottom tab bar (sheet selector)
        self.tab_bar_frame = ctk.CTkFrame(self, height=40)
        self.tab_bar_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.tab_bar_frame.grid_columnconfigure(0, weight=1)

        # Initialize with first sheet
        self.add_sheet()

    # -------------------------------
    # Create a new sheet
    # -------------------------------
    def add_sheet(self):
        self.sheet_count += 1
        sheet_name = f"Sheet{self.sheet_count}"

        # Create new Text area (sheet content)
        text_widget = ctk.CTkTextbox(self.sheet_frame, width=800, height=400)
        text_widget.insert("1.0", f"This is {sheet_name}")
        self.sheets[sheet_name] = text_widget

        # Create a tab button for this sheet
        btn = ctk.CTkButton(
            self.tab_bar_frame, text=sheet_name,
            width=100, height=30,
            command=lambda name=sheet_name: self.show_sheet(name)
        )
        btn.pack(side="left", padx=5, pady=5)
        self.sheets[sheet_name].tab_button = btn  # store reference to delete later

        # Show the newly added sheet
        self.show_sheet(sheet_name)

    # -------------------------------
    # Show selected sheet
    # -------------------------------
    def show_sheet(self, sheet_name):
        # Hide current sheet
        if self.current_sheet:
            self.sheets[self.current_sheet].pack_forget()

        # Show new sheet
        self.current_sheet = sheet_name
        self.sheets[sheet_name].pack(expand=True, fill="both", padx=10, pady=10)

    # -------------------------------
    # Delete current sheet
    # -------------------------------
    def delete_sheet(self):
        if not self.current_sheet:
            messagebox.showinfo("Info", "No sheet selected.")
            return

        # Don't allow deleting the last sheet
        if len(self.sheets) == 1:
            messagebox.showwarning("Warning", "Cannot delete the last sheet.")
            return

        sheet_to_delete = self.current_sheet
        # Remove from GUI
        self.sheets[sheet_to_delete].pack_forget()
        self.sheets[sheet_to_delete].tab_button.destroy()

        # Delete from dictionary
        del self.sheets[sheet_to_delete]

        # Switch to another remaining sheet
        next_sheet = list(self.sheets.keys())[0]
        self.show_sheet(next_sheet)


if __name__ == "__main__":
    app = SheetManagerApp()
    app.mainloop()
