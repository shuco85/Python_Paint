from tkinter import ttk
import tkinter as tk

root = tk.Tk()
root.title('Paint FLX')
root.geometry('800x800')
root.resizable(False, False)

my_canvas = tk.Canvas(root,
                      width=600,
                      height=400,
                      bg='black')
my_canvas.pack(pady=20)

root.mainloop()
