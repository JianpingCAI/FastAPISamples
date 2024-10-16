import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)
folder_selected = filedialog.askdirectory()
if folder_selected:
    print(folder_selected)
else:
    print(None)
