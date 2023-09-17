import sqlite3
import re



class Auth:
    def __init__(self):
        self.connection = sqlite3.connect("student_class.sqlite")
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

        username_pattern = re.compile(r"^[a-zA-Z0-9]{5,20}$")
        if not username_pattern.match(username): # add validation on insert
            print("username has invalid regex pattern, inserting rejected.")
        else:
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


    def get_id(self, username: str) -> str:
        sql_query = f"""
                     SELECT student_id
                     FROM student_auth
                     WHERE student_username='{username}';
                     """
        result = self.cursor.execute(sql_query).fetchone()
        return None if result == None else result[0]



class SchoolClass:
    def __init__(self):
        self.connection = sqlite3.connect("student_class.sqlite")
        self.cursor = self.connection.cursor()
        self.create_table()


    def create_table(self):
        sql_query = ("CREATE TABLE IF NOT EXISTS school_class("
                     "class_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "class_name VARCHAR(200) NOT NULL)")
        self.cursor.execute(sql_query)
    

    def get_classes(self):
        sql_query = '''
                    SELECT * FROM school_class
                    '''
        result = self.cursor.execute(sql_query).fetchall()
        return result



class StudentClass:
    def __init__(self):
        self.connection = sqlite3.connect('student_class.sqlite')
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")
        self.create_table()


    def create_table(self):
        sql_query = f'''
                    CREATE TABLE IF NOT EXISTS student_class(
                        student_id INTEGER NOT NULL,
                        class_id INTEGER NOT NULL,
                        FOREIGN KEY(student_id) REFERENCES student_auth(student_id),
                        FOREIGN KEY(class_id) REFERENCES school_class(class_id)
                    )
                    '''
        self.cursor.execute(sql_query)


    def create_row(self, student_id: int, class_id: int) -> None:
        sql_query = f'''
                    INSERT INTO student_class(student_id, class_id)
                    VALUES({student_id}, {class_id})
                    '''
        self.cursor.execute(sql_query)
        self.connection.commit()


    def clear(self) -> None:
        sql_query = f'''
                    DELETE FROM student_class
                    '''
        self.cursor.execute(sql_query)
        self.connection.commit()


    def get_by_class_id(self, class_id: int) -> list[tuple]:
        sql_query = f'''
                    SELECT * FROM student_class
                    WHERE class_id = {class_id}
                    '''
        result = self.cursor.execute(sql_query).fetchall()
        return result


    def get_by_student_id(self, student_id: int) -> list[tuple]:
        sql_query = f'''
                    SELECT * FROM student_class
                    WHERE student_id = {student_id}
                    '''
        result = self.cursor.execute(sql_query).fetchall()
        return result


