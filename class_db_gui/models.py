import sqlite3
import mysql.connector
from encryption import EncryptMethods



class SchoolClass:
    '''
    accessing school_class database in mysql
    used for choosing classes
    '''

    def __init__(self):
        self.connection =  mysql.connector.connect(user='user_1',
                                                   password='123456',
                                                   host='127.0.0.1',
                                                   database='school_class')
        self.cursor = self.connection.cursor()
        self.init_tables()


    def init_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS student(
            student_id INTEGER PRIMARY KEY AUTO_INCREMENT,
            student_name VARCHAR(50) NOT NULL
        );
                    
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS class(
            class_id INTEGER PRIMARY KEY AUTO_INCREMENT,
            class_name VARCHAR(100) NOT NULL             
        );
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_class(
            student_id INTEGER NOT NULL,
            class_id INTEGER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES student(student_id),
            FOREIGN KEY (class_id) REFERENCES class(class_id)
        );               
        ''')
    
    
    def show_tables(self):
        self.cursor.execute("SHOW TABLES;")

        for result in self.cursor:
            print(result)



class Auth:
    def __init__(self):
        self.connection = sqlite3.connect("auth.sqlite")
        self.cursor = self.connection.cursor()
        self.create_table()


    def create_table(self) -> None:
        sql_query = '''
                    CREATE TABLE IF NOT EXISTS student_auth(
                    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_username VARCHAR(20) UNIQUE NOT NULL,
                    student_password VARCHAR(20) NOT NULL
                    )'''
        self.cursor.execute(sql_query)


    def create_usr(self, username:str, encrypted_password:str) -> None:
        '''
        please use encrypted password(sha256) at GUI 
        level to avoid password been handled as plain-text
        '''
        try:
            sql_query = f'''
                        INSERT INTO student_auth(student_username, student_password)
                        VALUES("{username}", "{encrypted_password}")
                        '''
            self.cursor.execute(sql_query)
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                print(e)


    def get_usr(self, username: str) -> str:
        sql_query = f'''
                     SELECT student_username
                     FROM student_auth
                     WHERE student_username="{username}"
                     '''
        result = self.cursor.execute(sql_query).fetchone() 
        # because result of query is always a table not a single value, so we need to process it to get the value
        return None if result == None else result[0]


    def get_pwd(self, username: str) -> str:
        sql_query = f'''
                     SELECT student_password
                     FROM student_auth
                     WHERE student_username="{username}"
                     '''
        result = self.cursor.execute(sql_query).fetchone()

        return None if result == None else result[0]

