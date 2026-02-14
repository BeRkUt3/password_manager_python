from class_Password import Password
from tkinter import messagebox as mbox
from tkinter import ttk
import tkinter as tk

class Generator:
    def __init__(self, win, row):
        self._win = win
        self._row = row
        self.__pwd = ''
    def generate_page(self):
        def generate_password():
            if not any([is_AZ.get(), is_az.get(), is_num.get(), is_symbol.get()]):
                mbox.showerror('Error', 'You must select at least one option!')
                return
            try:
                l = int(length.get())
            except:
                mbox.showerror('Error', 'Length must be an integer!')
            if not (1 <= int(length.get()) <= 30):
                mbox.showerror('Error', 'Length must be between 1 and 30!')
            try:
                pwd = Password(int(length.get()), is_AZ.get(), is_az.get(), is_num.get(), is_symbol.get())
                pwd.generate()
                self.__pwd = pwd.password
                output.delete(0, 'end')
                output.insert(0, pwd.password)
            except Exception as err:
                mbox.showerror('Error', str(err))

        tk.Label(self._win, text="A-Z:").grid(row=self._row + 0, column=0)
        tk.Label(self._win, text="a-z:").grid(row=self._row + 1, column=0)
        tk.Label(self._win, text="0-9:").grid(row=self._row + 2, column=0)
        tk.Label(self._win, text="Special symbols:").grid(row=self._row + 3, column=0)

        is_AZ = tk.BooleanVar()
        is_AZ.set(True)
        ttk.Radiobutton(self._win, text="Yes", variable=is_AZ, value=True).grid(row=self._row + 0, column=1)
        ttk.Radiobutton(self._win, text="No", variable=is_AZ, value=False).grid(row=self._row + 0, column=2)
        is_az = tk.BooleanVar()
        is_az.set(True)
        ttk.Radiobutton(self._win, text="Yes", variable=is_az, value=True).grid(row=self._row + 1, column=1)
        ttk.Radiobutton(self._win, text="No", variable=is_az, value=False).grid(row=self._row + 1, column=2)
        is_num = tk.BooleanVar()
        is_num.set(True)
        ttk.Radiobutton(self._win, text="Yes", variable=is_num, value=True).grid(row=self._row + 2, column=1)
        ttk.Radiobutton(self._win, text="No", variable=is_num, value=False).grid(row=self._row + 2, column=2)
        is_symbol = tk.BooleanVar()
        is_symbol.set(True)
        ttk.Radiobutton(self._win, text="Yes", variable=is_symbol, value=True).grid(row=self._row + 3, column=1)
        ttk.Radiobutton(self._win, text="No", variable=is_symbol, value=False).grid(row=self._row + 3, column=2)

        tk.Label(self._win, text="Length (1 to 30):").grid(row=self._row + 4, column=0)
        length = tk.Entry(self._win, justify="right")
        length.grid(row=self._row + 4, column=1)

        tk.Button(self._win, text="Generate Password", command=generate_password).grid(row=self._row + 5, column=0)

        tk.Label(self._win, text="Password").grid(row=self._row + 6, column=0)
        output = tk.Entry(self._win, justify="right")
        output.grid(row=self._row + 6, column=1, columnspan=3, sticky="ew")
    @property
    def pwd(self):
        return self.__pwd
    @pwd.setter
    def pwd(self, value):
        return
    @pwd.deleter
    def pwd(self):
        return