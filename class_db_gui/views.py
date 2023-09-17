from typing import Protocol

import tkinter as tk
from tkinter import ttk, messagebox

import widgets



class Presenter(Protocol):
    def handle_login(self):
        ...
    def handle_signup(self):
        ...

    def handle_create_user(self):
        ...



class WindowLogin(tk.Tk):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter
        self.variables = {
            'username': tk.StringVar(),
            'password': tk.StringVar()
        }

        self.init_screen()


    def init_screen(self):
        # widgets creation
        self.frame_login = ttk.LabelFrame(self, text='login')
        self.entry_username = widgets.LabelEntry(self.frame_login, 
                                                 label_text='username',
                                                 entry_textvariable=self.variables['username'])
        self.entry_password = widgets.LabelEntry(self.frame_login,
                                                 label_text='password',
                                                 entry_textvariable=self.variables['password'],
                                                 show='*')
        self.btn_login = ttk.Button(self.frame_login, text='log in')
        self.btn_signup = ttk.Button(self.frame_login, text='sign up')

        # widgets grid layout
        self.frame_login.grid()
        self.entry_username.grid()
        self.entry_password.grid()
        self.btn_login.grid()
        self.btn_signup.grid()

        # widgets bindings
        self.btn_login.bind('<ButtonRelease-1>', self.presenter.handle_login)
        self.btn_signup.bind('<ButtonRelease-1>', self.presenter.handle_signup)


    def msgbox_warning(self, title: str, content: str) -> None:
        messagebox.showinfo(title, content)


    def run(self):
        self.mainloop()



class WindowSignup(tk.Tk):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter
        self.variables = {
            'username': tk.StringVar(),
            'password': tk.StringVar()
        }

        self.init_screen()


    def init_screen(self):
        # widgets creation
        self.frame_signup = ttk.LabelFrame(self, text='sign up')
        self.entry_username = widgets.LabelEntry(self.frame_signup, 
                                                 label_text='username',
                                                 entry_textvariable=self.variables['username'])
        self.entry_password = widgets.LabelEntry(self.frame_signup,
                                                 label_text='password',
                                                 entry_textvariable=self.variables['password'],
                                                 show='*')
        self.btn_create_user = ttk.Button(self.frame_signup, text='confirm sign up')

        # widgets grid layout
        self.frame_signup.grid()
        self.entry_username.grid()
        self.entry_password.grid()
        self.btn_create_user.grid()

        # widgets bindings
        self.btn_create_user.bind('<ButtonRelease-1>', self.presenter.handle_create_user)


    def msgbox_warning(self, title: str, content: str) -> None:
        messagebox.showinfo(title, content)


    def run(self):
        self.mainloop()



class WindowMain(tk.Tk):
    def __init__(self, presenter: Presenter):
        super().__init__()
        self.presenter = presenter
    
    def run(self):
        self.mainloop()


