import customtkinter as ctk
from tkinter import filedialog

def select_folder(entry_widget):
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_widget.delete(0, ctk.END)
        entry_widget.insert(0, folder_path)

app = ctk.CTk()
app.title("CustomTkinter Folder Browser")
app.geometry("400x150")

path_entry = ctk.CTkEntry(app, width=300)
path_entry.pack(pady=20)

browse_button = ctk.CTkButton(app, text="Browse Folder", command=lambda: select_folder(path_entry))
browse_button.pack()

app.mainloop()