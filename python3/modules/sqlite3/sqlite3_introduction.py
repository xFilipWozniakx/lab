# Date of creation: 07-10-2026 21:21
# how to handle sqlite3 connection table creation, and inserting positions
import sqlite3 

def po(item):
    print(f'{item}, {type(item)}')

def insert_into_users(cursor):
    login = input("Login?:\n")
    password = input("Password?:\n")
    cursor.execute(f"INSERT INTO users( login, password_hash) VALUES ('{login}', '{password}');")
    conn.commit()

def retrieve_all(cursor):
    for row in cursor.execute("SELECT * FROM USERS;"):
        print(row)

def create_tables(cursor):
    cursor.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL)");
    
def connect(name):
    con = sqlite3.connect(name)
    return con

def create(cursor):
    create_tables(cursor)
    insert_into_users(cursor)

conn = connect("db.db")
cur = conn.cursor()

# insert_into_users(cur)
# retrieve_all(cur)










"""
Connection	Database connection object.
Cursor	Database cursor object for executing SQL.
DatabaseError	Exception for database-related errors.
Error	Base exception class for sqlite3 errors.
IntegrityError	Exception for integrity constraint violations.
OperationalError	Exception for database operational errors.
ProgrammingError	Exception for programming errors.
Row	Row object representing a database row.
connect()	Open a connection to a SQLite database.
register_adapter()	Register a callable to convert custom Python types to SQLite types.
register_converter()	Register a callable to convert SQLite types to custom Python types.
"""

