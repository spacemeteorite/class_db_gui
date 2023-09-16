import sqlite3
import mysql.connector


class Model:


    def __init__(self):
        self.connection =  mysql.connector.connect(user='wang',
                                                   password='123456',
                                                   host='127.0.0.1',
                                                   database='school_class')
        self.cursor = self.connection.cursor()
        self.init_tables()


    def init_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS student(
            student_id INTEGER PRIMARY KEY AUTO_INCREMENT,
            student_name VARCHAR(50) NOT NULL
        );
                    
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS class(
            class_id INTEGER PRIMARY KEY AUTO_INCREMENT,
            class_name VARCHAR(100) NOT NULL             
        );
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_class(
            student_id INTEGER NOT NULL,
            class_id INTEGER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES student(student_id),
            FOREIGN KEY (class_id) REFERENCES class(class_id)
        );               
        """)
    
    
    def show_tables(self):
        self.cursor.execute("SHOW TABLES;")

        for result in self.cursor:
            print(result)


model = Model()
model.show_tables()