import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk

def get_button(window, text, color, command, fg='white'):
    return tk.Button(window, text=text, bg=color, fg=fg, command=command, font=('Arial', 14), width=20)

def get_img_label(window):
    return tk.Label(window)

def get_entry_text(window):
    return tk.Text(window, height=1, width=20, font=('Arial', 14))

def get_text_label(window, text):
    return tk.Label(window, text=text, font=('Arial', 14))

def msg_box(title, description):
    messagebox.showinfo(title, description)
