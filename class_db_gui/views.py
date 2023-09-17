# modules built in
from typing import Protocol
import tkinter as tk
from tkinter import ttk, messagebox


# modules wrote by self
from . import widgets



class Presenter(Protocol):
    def handle_login(self):
        ...
    def handle_signup(self):
        ...
    def handle_create_user(self):
        ...
    def handle_add_class(self):
        ...
    def handle_drop_class(self):
        ...


class WindowLogin(tk.Tk):
    def __init__(self, presenter):
        super().__init__()

        self.presenter = presenter
        self.variables = {
            'username': tk.StringVar(),
            'password': tk.StringVar()
        }

        self.title("Log In")
        self.eval('tk::PlaceWindow . center') # use tcl to center window
        self.resizable(False, False)


    def init_widget(self):
        # widgets creation
        self.frame_login = ttk.LabelFrame(self, text='login')
        self.named_entry_username = widgets.NamedEntry(self.frame_login, 
                                                 label_text='username',
                                                 entry_textvariable=self.variables['username'])
        self.named_entry_password = widgets.NamedEntry(self.frame_login,
                                                 label_text='password',
                                                 entry_textvariable=self.variables['password'],
                                                 show='*')
        self.frame_btns = ttk.Frame(self)
        self.btn_login = ttk.Button(self.frame_btns, text='log in')
        self.btn_signup = ttk.Button(self.frame_btns, text='sign up')

        # widgets grid layout
        self.frame_login.grid(row=0)
        self.named_entry_username.grid(row=0, padx=5, pady=10)
        self.named_entry_password.grid(row=1, padx=5, pady=10)
        self.frame_btns.grid(row=1)
        self.btn_login.grid(row=0, column=0, padx=5, pady=3)
        self.btn_signup.grid(row=0, column=1, padx=5, pady=3)

        # widgets bindings
        self.btn_login.bind('<ButtonRelease-1>', self.presenter.handle_login)
        self.btn_signup.bind('<ButtonRelease-1>', self.presenter.handle_signup)


    def msgbox_success(self, title: str, content: str) -> None:
        messagebox.showinfo(title, content)


    def msgbox_warning(self, title: str, content: str) -> None:
        messagebox.showinfo(title, content)


    def run(self):
        self.init_widget()
        self.mainloop()



class WindowSignup(tk.Tk):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter
        self.variables = {
            'username': tk.StringVar(),
            'password': tk.StringVar()
        }

        self.title('Sign Up')
        self.eval('tk::PlaceWindow . center') # use tcl to center window
        self.resizable(False, False)


    def init_widget(self):
        # widgets creation
        self.frame_signup = ttk.LabelFrame(self, text='sign up')
        self.entry_username = widgets.NamedEntry(self.frame_signup, 
                                                 label_text='username',
                                                 entry_textvariable=self.variables['username'])
        self.entry_password = widgets.NamedEntry(self.frame_signup,
                                                 label_text='password',
                                                 entry_textvariable=self.variables['password'],
                                                 show='*')
        self.btn_create_user = ttk.Button(self, text='confirm info')

        # widgets grid layout
        self.frame_signup.grid()
        self.entry_username.grid(row=0, pady=10)
        self.entry_password.grid(row=1, pady=10)
        self.btn_create_user.grid(row=1, pady=5)

        # widgets bindings
        self.btn_create_user.bind('<ButtonRelease-1>', self.presenter.handle_create_user)


    def msgbox_success(self, title: str, content: str) -> None:
        messagebox.showinfo(title, content)


    def msgbox_warning(self, title: str, content: str) -> None:
        messagebox.showwarning(title, content)


    def run(self):
        self.init_widget()
        self.mainloop()



class WindowMain(tk.Tk):
    def __init__(self, presenter: Presenter):
        super().__init__()
        self.presenter = presenter
    
        self.title('Home')
        self.eval('tk::PlaceWindow . center') # use tcl to center window
    
        self.variables = {
            'user_id': tk.StringVar(),
            'username': tk.StringVar(),
            'date': tk.StringVar(),
        }
        self.mapping_available_class_to_classid = {}

        self.mapping_selected_class_to_classid = {}


        self.init_widget()

        
    def init_widget(self):
        # widgets creation
        self.frame_info = ttk.LabelFrame(self, text="Info")
        self.named_label_name = widgets.NamedLabel(self.frame_info, label_text='Name: ', label_textvariable=self.variables['username'])
        self.named_label_id = widgets.NamedLabel(self.frame_info, label_text='ID: ', label_textvariable=self.variables['user_id'])

        self.frame_classes = ttk.LabelFrame(self, text="Available Classes")
        self.listbox_classes = tk.Listbox(self.frame_classes)

        self.frame_btns = ttk.Frame(self)
        self.btn_add_class = ttk.Button(self.frame_btns, text='>>')
        self.btn_drop_class = ttk.Button(self.frame_btns, text='<<')

        self.frame_classes_selected = ttk.LabelFrame(self, text="Selected Classes")
        self.listbox_classes_selected = tk.Listbox(self.frame_classes_selected)

        # widgets grid layout
        self.frame_info.grid(row=0)
        self.named_label_name.grid()
        self.named_label_id.grid()

        self.frame_classes.grid(row=1, column=0)
        self.listbox_classes.grid()

        self.frame_btns.grid(row=1, column=1)
        self.btn_add_class.grid(row=0)
        self.btn_drop_class.grid(row=1)

        self.frame_classes_selected.grid(row=1, column=2)
        self.listbox_classes_selected.grid()

        # event handler
        self.listbox_classes.bind('<<ListboxSelect>>', self.presenter.handle_listbox_available_class_select)
        self.listbox_classes_selected.bind('<<ListboxSelect>>', self.presenter.handle_listbox_selected_class_select)
        self.btn_add_class.bind('<ButtonRelease-1>', self.presenter.handle_add_class)
        self.btn_drop_class.bind('<ButtonRelease-1>', self.presenter.handle_drop_class)


    def update_listbox_available_classes(self, class_list: list[tuple]) -> None:
        self.listbox_classes.delete(0, tk.END)
        listbox_index = 0
        for c in class_list:
            self.listbox_classes.insert(tk.END, f'{c[0], c[1]}')
            self.mapping_available_class_to_classid[listbox_index] = c[0]
            listbox_index += 1
        self.update()


    def update_listbox_selected_classes(self, class_list: list[tuple]) -> None:
        self.listbox_classes_selected.delete(0, tk.END)
        listbox_index = 0
        for c in class_list:
            self.listbox_classes_selected.insert(tk.END, f'{c[1]}')
            self.mapping_selected_class_to_classid[listbox_index] = c[1]
            listbox_index += 1
        self.update()


    def msgbox_warning(self, title: str, content: str) -> None:
        messagebox.showwarning(title, content)


    def msgbox_info(self, title: str, content: str) -> None:
        messagebox.showinfo(title, content)


    def run(self):
        self.mainloop()


