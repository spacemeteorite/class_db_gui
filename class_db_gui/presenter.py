# modules built-in
import re

# modules from third party

# modules wrote by self
from .views import WindowLogin, WindowMain, WindowSignup
from .models import Auth, SchoolClass, StudentClass
from .encryption import EncryptMethods



class Presenter:
    def __init__(self):
        # initiate gui
        self.window_login = WindowLogin(self)
        print('login window initiated')

        # initiate database
        self.db_auth = Auth()
        self.db_school_class = SchoolClass()
        self.db_student_class = StudentClass()

        # run app
        self.run()

        # metadata
        self.current_user_id = None # auto assign after logged in
        self.current_waiting_to_add_class_id = None # auto assign after class selected
        self.current_waiting_to_drop_class_id = None # auto assign


    def handle_login(self, event=None) -> None:
        username_entry = self.window_login.variables['username'].get()
        password_entry = self.window_login.variables['password'].get()
        self.validation_login(username_entry, password_entry)


    def handle_signup(self, event=None) -> None:
        self.window_login.destroy()
        self.window_signup = WindowSignup(self)
        self.window_signup.run()


    def handle_create_user(self, event=None) -> None:
        username_entry = self.window_signup.variables['username'].get()
        password_entry = self.window_signup.variables['password'].get()

        self.validation_create_user(username_entry, password_entry)


    def handle_listbox_available_class_select(self, event=None) -> None:
        current_selected_class_listbox_index = event.widget.curselection()[0]
        self.current_waiting_to_add_class_id = self.window_main.mapping_available_class_to_classid[current_selected_class_listbox_index]


    def handle_listbox_selected_class_select(self, event=None) -> None:
        current_selected_class_listbox_index = event.widget.curselection()[0]
        self.current_waiting_to_drop_class_id = self.window_main.mapping_selected_class_to_classid[current_selected_class_listbox_index]


    def handle_add_class(self, event=None) -> None:
        print(f'try add class {self.current_waiting_to_add_class_id}')

        # check if student has selected this class already
        student_id = self.current_user_id
        class_id = self.current_waiting_to_add_class_id
        sql_query = f'''
                    SELECT * 
                    FROM student_class
                    WHERE student_id = {student_id} AND class_id = {class_id}
                    '''
        result = self.db_student_class.cursor.execute(sql_query).fetchall()
        print('result:', result)
        if result == []:
            self.db_student_class.create_row(student_id, class_id)
            self.window_main.msgbox_info('success', f'add class{class_id} successfully!')
        else:
            self.window_main.msgbox_warning('duplicated record', 'you already selected this class, try another one')

        selected_class_list = self.db_student_class.get_by_student_id(self.current_user_id)
        self.window_main.update_listbox_selected_classes(selected_class_list)


    def handle_drop_class(self, event=None) -> None:
        print('handle drop class')
        student_id = self.current_user_id
        class_id = self.current_waiting_to_drop_class_id
        self.db_student_class.delete_row(student_id, class_id)

        selected_class_list = self.db_student_class.get_by_student_id(self.current_user_id)
        self.window_main.update_listbox_selected_classes(selected_class_list)

        self.window_main.msgbox_info('success', f'successfully dropped class{class_id}')


    def validation_login(self, username, password):
        '''validate user pwd input with record in db'''
        encrypted_password = EncryptMethods.encrypt_pwd(password)

        if username == '' or password == '':
            self.window_login.msgbox_warning('Empty Entry', 'username or password cannot be empty!')
        else:
            username_db = self.db_auth.get_usr(username)
            if username_db == None:
                self.window_login.msgbox_warning('No such user', f'no such user: {username}')
            else:
                password_db = self.db_auth.get_pwd(username_db)
                if encrypted_password != password_db:
                    self.window_login.msgbox_warning('password error', 'wrong password, please try again')
                else:
                    self.success_login(username)


    def validation_create_user(self, username, password):
        # first we need to validate username and password to preferred format
        # with the help of regex(regular expression)
        username_pattern = re.compile(r"^[a-zA-Z0-9]{5,20}$")
        password_pattern = re.compile(r"^[a-zA-Z0-9]{10,30}+$")
        encrypted_password = EncryptMethods.encrypt_pwd(password)

        if username == '' or password == '':
            self.window_signup.msgbox_warning('Empty Entry', 'username or password cannot be empty!')
        else:
            hasUsername = username == self.db_auth.get_usr(username)
            if hasUsername:
                self.window_signup.msgbox_warning('user existed', f'user existed in database! <{username}>')
            else:
                if username_pattern.match(username) and password_pattern.match(password):
                    self.db_auth.create_usr(username, encrypted_password)
                    self.window_signup.msgbox_success('user created!', f"""user created successfully\n username:{username}\n password:{password}""")
                    self.success_signup()
                else:
                    self.window_signup.msgbox_warning('invalid value', """please try valid username(5-20 length contains letters or numbers) or password(10-30 length contains letters or numbers)""")


    def success_login(self, username):
        self.window_login.msgbox_success(f'Successfully Logged In', f'Welcome {username}!')
        self.window_login.destroy()

        self.current_user_id = self.db_auth.get_id(username)
        self.window_main = WindowMain(self)
        self.window_main.variables['username'].set(username)
        self.window_main.variables['user_id'].set(self.current_user_id)


        class_list = self.db_school_class.get_classes()
        self.window_main.update_listbox_available_classes(class_list)
        selected_class_list = self.db_student_class.get_by_student_id(self.current_user_id)
        self.window_main.update_listbox_selected_classes(selected_class_list)
        self.window_main.run()


    def success_signup(self):
        self.window_signup.destroy()
        self.window_login = WindowLogin(self)
        self.window_login.run() 


    def run(self):
        self.window_login.run()


if __name__ == '__main__':
    presenter = Presenter()