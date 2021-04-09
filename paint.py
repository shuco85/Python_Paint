from tkinter import ttk
import tkinter as tk
from canvas import MyCanvas

root = tk.Tk()
root.title('Paint FLX')
root.geometry('800x800')
root.resizable(False, False)


my_canvas = MyCanvas(root)
my_canvas.pack(pady=20)

my_line = my_canvas.create_line(2, 2, 100, 100, fill='red')
my_line2 = my_canvas.create_line(0, 300, 100, 100, fill='blue')
my_canvas.delete(my_line2)

my_line3 = my_canvas.create_line(0, 300, 100, 100, fill='blue')


root.mainloop()
