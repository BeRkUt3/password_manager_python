from class_Generator import Generator
from database import *
from tkinter import messagebox as mbox
import tkinter as tk


win = tk.Tk()
win.title("Password Manager")
win.geometry("700x500+800+300")
win.resizable(True, True)

def password_checker_page():
    def check():
        row = 3
        clear_window(row)

        input = password.get()
        if not input:
            mbox.showerror('Error', 'You must enter a password!')
            return
        if not (1 <= len(input) <= 30):
            mbox.showerror('Error', 'Length must be between 1 and 30!')
            return
        if len(input) < 9:
            tk.Label(win, text="[!] The length should be a least 9 symbols").grid(row=row, column=0)
            row += 1
        is_AZ = False
        is_az = False
        is_num = False
        is_symbol = False
        for i in input:
            if 'A' <= i <= 'Z':
                is_AZ = True
            elif 'a' <= i <= 'z':
                is_az = True
            elif '0' <= i <= '9':
                is_num = True
            else:
                is_symbol = True
        if not is_AZ:
            tk.Label(win, text="[!] There is no uppercase charakter").grid(row=row, column=0)
            row += 1
        if not is_az:
            tk.Label(win, text="[!] There is no lowercase charakter").grid(row=row, column=0)
            row += 1
        if not is_num:
            tk.Label(win, text="[!] There is no number").grid(row=row, column=0)
            row += 1
        if not is_symbol:
            tk.Label(win, text="[!] There is no special symbol").grid(row=row, column=0)
            row += 1

    menu()
    tk.Label(win, text="Your password (1 to 30 symbols):").grid(row=1, column=0)
    password = tk.Entry(win, justify="right")
    password.grid(row=1, column=1)
    tk.Button(win, text="Check", command=check).grid(row=2, column=0)

def check_root(func):
    def is_root():
        if check_root_password(password.get()):
            func()
        else:
            mbox.showerror('Error', 'Invalid password!')

    menu()
    clear_window(1)
    tk.Label(win, text="Root Password:").grid(row=1, column=0)
    password = tk.Entry(win, justify='right')
    password.grid(row=1, column=1)
    tk.Button(win, text="Apply", command=is_root).grid(row=2, column=0)

def clear_window(i):
    while win.grid_slaves(row=i):
        for el in win.grid_slaves(row=i):
            el.destroy()
        i += 1

def generator_page():
    generator = Generator(win, 1)
    menu()
    generator.generate_page()

def generator_window():
    result = ''
    def use_pwd():
        nonlocal result
        result = generator.pwd
        gen_win.destroy()

    gen_win = tk.Toplevel()
    gen_win.title("Generator")
    gen_win.geometry("400x200+600+200")
    gen_win.resizable(False, False)

    tk.Button(gen_win, text="Use", command=use_pwd).grid(row=0, column=0)

    generator = Generator(gen_win, 1)
    generator.generate_page()
    gen_win.wait_window()
    return result

def root_password_changing():
    def change():
        clear_window(5)
        if new_password.get() == repeat_new_password.get():
            ans = change_root_password(old_password.get(), new_password.get())
            tk.Label(win, text=ans).grid(row=5, column=0)
        else:
            mbox.showerror('Error', 'Password in "Repeat New Password" field doesn\'t match to password in "New Password" field')

    menu()
    clear_window(1)
    tk.Label(win, text="Current Password (Default: \"0000\"):").grid(row=1, column=0)
    tk.Label(win, text="New Password:").grid(row=2, column=0)
    tk.Label(win, text="Repeat New Password:").grid(row=3, column=0)

    old_password = tk.Entry(win, justify="right")
    old_password.grid(row=1, column=1)

    new_password = tk.Entry(win, justify="right")
    new_password.grid(row=2, column=1)

    repeat_new_password = tk.Entry(win, justify="right")
    repeat_new_password.grid(row=3, column=1)

    tk.Button(win, text="Apply", command=change).grid(row=4, column=0)



def my_pwds_page():
    def show_user_logins():
        nonlocal row
        clear_window(row)
        rows = get_all_logins()
        tk.Label(win, text='№').grid(row=row, column=0)
        tk.Label(win, text='Login').grid(row=row, column=1)
        tk.Label(win, text='Password').grid(row=row, column=2)
        for i, line in enumerate(rows, start=1):
            tk.Label(win, text=str(i+1)).grid(row=row+i, column=0)
            tk.Label(win, text=line['Login']).grid(row=row+i, column=1)
            tk.Label(win, text=line['Password']).grid(row=row+i, column=2)

    def add_login():
        nonlocal row
        def add():
            clear_window(row+3)
            if not login.get() or not password.get():
                mbox.showerror('Error', 'Please fill all fields')
                return
            ans = add_new_line(login.get(), password.get())
            tk.Label(win, text=ans).grid(row=6, column=0)
        def generate():
            pwd = generator_window()
            password.delete(0, tk.END)
            password.insert(tk.END, pwd)
        clear_window(row)
        tk.Label(win, text="Login:").grid(row=row, column=0)
        login = tk.Entry(win, justify="right")
        login.grid(row=row, column=1)
        tk.Label(win, text="Password:").grid(row=row+1, column=0)
        password = tk.Entry(win, justify="right")
        password.grid(row=row+1, column=1)
        tk.Button(win, text="Generate", command=generate).grid(row=row+1, column=2)
        tk.Button(win, text="Add", command=add).grid(row=row+2, column=0)
    def edit_login():
        nonlocal row
        def delete_log():
            cur = get_cur()
            if not cur:
                return
            delete_line(int(cur['ID']))
            clear_window(row+2)
            rows = get_all_logins()
            for i, line in enumerate(rows, start=3):
                tk.Label(win, text=line['ID']).grid(row=row + i, column=0)
                tk.Label(win, text=line['Login']).grid(row=row + i, column=1)
                tk.Label(win, text=line['Password']).grid(row=row + i, column=2)
        def edit_log():
            def edit_log_query():
                edit_line_login(int(cur['ID']), new_login.get())
                tk.Label(win, text="Completed").grid(row=row+4, column=0)

            cur = get_cur()
            if not cur:
                return
            clear_window(row+2)
            tk.Label(win, text=cur['ID']).grid(row=row+2, column=0)
            tk.Label(win, text=cur['Login']).grid(row=row+2, column=1)
            tk.Label(win, text=cur['Password']).grid(row=row+2, column=2)

            tk.Label(win, text="New login:").grid(row=row+3, column=0)
            new_login = tk.Entry(win, justify="right")
            new_login.grid(row=row+3, column=1)
            tk.Button(win, text="Edit", command=edit_log_query).grid(row=row+3, column=2)
        def edit_pwd():
            def edit_pwd_query():
                edit_line_password(int(cur['ID']), new_password.get())
                tk.Label(win, text="Completed").grid(row=row+5, column=0)
            def generate():
                pwd = generator_window()
                new_password.delete(0, tk.END)
                new_password.insert(tk.END, pwd)

            cur = get_cur()
            if not cur:
                return
            clear_window(row+2)
            tk.Label(win, text=cur['ID']).grid(row=row+2, column=0)
            tk.Label(win, text=cur['Login']).grid(row=row+2, column=1)
            tk.Label(win, text=cur['Password']).grid(row=row+2, column=2)

            tk.Label(win, text="New password:").grid(row=row+3, column=0)
            new_password = tk.Entry(win, justify="right")
            new_password.grid(row=row+3, column=1)
            tk.Button(win, text="Generate", command=generate).grid(row=row+3, column=2)

            tk.Button(win, text="Edit", command=edit_pwd_query).grid(row=row+4, column=0)
        def get_cur():
            if not id.get().isdigit():
                mbox.showerror('Error', 'Please enter an ID')
                return None
            for r in rows:
                if r['ID'] == int(id.get()):
                    return r
            mbox.showerror('Error', 'ID not found')
            return None



        clear_window(row)
        tk.Label(win, text="Enter ID:").grid(row=row, column=0)
        id = tk.Entry(win, justify="right")
        id.grid(row=row, column=1)
        tk.Button(win, text="Edit login", command=edit_log).grid(row=row, column=2, sticky="ew")
        tk.Button(win, text="Edit password", command=edit_pwd).grid(row=row, column=3, sticky="ew")
        tk.Button(win, text="Delete", command=delete_log).grid(row=row, column=4, sticky="ew")
        rows = get_all_logins()
        tk.Label(win, text='ID').grid(row=row+1, column=0)
        tk.Label(win, text='Login').grid(row=row+1, column=1)
        tk.Label(win, text='Password').grid(row=row+1, column=2)
        for i, line in enumerate(rows, start=2):
            tk.Label(win, text=line['ID']).grid(row=row + i, column=0)
            tk.Label(win, text=line['Login']).grid(row=row + i, column=1)
            tk.Label(win, text=line['Password']).grid(row=row + i, column=2)

    menu()
    clear_window(1)
    row = 1
    tk.Label(win, text="Select an option:").grid(row=row, column=0)
    row += 1
    tk.Button(win, text="Show my logins", command=show_user_logins).grid(row=row, column=0, sticky="ew")
    tk.Button(win, text="Add login", command=add_login).grid(row=row, column=1, sticky="ew")
    tk.Button(win, text="Edit login", command=edit_login).grid(row=row, column=2, sticky="ew")
    row += 1



def menu():
    tk.Button(win, text="Generator", command=start_generator_page).grid(row=0, column=0, sticky="ew")
    tk.Button(win, text="Password Checker", command=start_password_checker_page).grid(row=0, column=1, sticky="ew")
    tk.Button(win, text="My passwords", command=start_my_pwds_page).grid(row=0, column=2, sticky="ew")
    tk.Button(win, text="Change root password", command=root_password_changing).grid(row=0, column=3, sticky="ew")


def start_generator_page():
    clear_window(0)
    generator_page()
def start_password_checker_page():
    clear_window(0)
    password_checker_page()
def start_my_pwds_page():
    clear_window(0)
    check_root(my_pwds_page)



def main():
    menu()
    win.mainloop()

if __name__ == '__main__':
    main()
