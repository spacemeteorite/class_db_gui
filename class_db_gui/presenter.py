from views import WindowLogin, WindowMain, WindowSignup
from models import Auth
from encryption import EncryptMethods


class Presenter:
    def __init__(self):
        # initiate gui
        self.window_login = WindowLogin(self)
        print('login window initiated')

        # initiate database
        self.auth = Auth()
        print('db initiated')

        # run app
        self.run()


    def handle_login(self, event=None) -> None:
        username_entry = self.window_login.variables['username'].get()
        password_entry = self.window_login.variables['password'].get()
        encrypted_password = EncryptMethods.encrypt_pwd(password_entry)


        if username_entry == '' or password_entry == '':
            self.window_login.msgbox_warning('Empty Entry', 'username or password cannot be empty!')
        else:
            username_db = self.auth.get_usr(username_entry)
            if username_db == None:
                self.window_login.msgbox_warning('No such user', f'no such user: {username_entry}')
            else:
                password_db = self.auth.get_pwd(username_db)
                if encrypted_password != password_db:
                    self.window_login.msgbox_warning('password error', 'wrong password, please try again')
                    print(encrypted_password)
                    print(password_db)
                else:
                    self.open_main_window()


    def handle_signup(self, event=None) -> None:
        self.window_login.destroy()
        self.window_signup = WindowSignup(self)
        self.window_signup.run()


    def handle_create_user(self, event=None) -> None:
        username_entry = self.window_signup.variables['username'].get()
        password_entry = self.window_signup.variables['password'].get()
        encrypted_password = EncryptMethods.encrypt_pwd(password_entry)
        print(encrypted_password)

        if username_entry == '' or password_entry == '':
            self.window_signup.msgbox_warning('Empty Entry', 'username or password cannot be empty!')
        else:
            username_db = self.auth.get_usr(username_entry)
            if username_db == username_entry:
                self.window_signup.msgbox_warning('user existed', f'user existed in database! <{username_entry}>')
            else:
                self.auth.create_usr(username_entry, encrypted_password)
                print('create successfully!')
                self.window_signup.destroy()
                self.window_login = WindowLogin(self)
                self.window_login.run() 


    def open_main_window(self):
        self.window_login.destroy()
        self.window_main = WindowMain(self)
        self.window_main.run()


    def run(self):
        self.window_login.run()


if __name__ == '__main__':
    presenter = Presenter()