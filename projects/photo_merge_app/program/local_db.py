import sys
import sqlite3 
import os 
import bcrypt

# ----------------------------------classes-----------------------------------------------------------

class DB_CREDS_EMPTY(Exception):
    pass

# ----------------------------------functions-----------------------------------------------------------

def create_db(login="admin",password="password"):
    # make connection and pointers
    con = sqlite3.connect("data.db")
    cur= con.cursor()
    
    cur.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL)");
    password = hash_pass(password).decode('utf-8')
    cur.execute("INSERT INTO users( login, password_hash) VALUES (?, ?)", (login,password))
    con.commit()
    return con, cur

def connect_db(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    return con,cur

def insert_into_users(cursor,connect):
    login = input("Login?:\n")
    password = input("Password?:\n")
    password = hash_pass(password).decode('utf-8')
    cursor.execute("INSERT INTO users( login, password_hash) VALUES (?, ?)", (login,password))
    connect.commit()

def hash_pass(password):
        password = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        if bcrypt.checkpw(password, hashed_password):
            return hashed_password.decode('utf-8')
        else:
            print("passwords doesnt match")

def check_if_exists(cur,login,password) -> bool:

    passw = cur.execute("SELECT password FROM USERS where login = ?", (login,)).fetchone()
    if hash_pass(password) == passw:
        return True
    else:
        return False


def retrieve_all(cursor):
    for row in cursor.execute("SELECT * FROM USERS;"):
        print(row)


# ----------------------------------------program starts ----------------------------------------

# ------ db creation & checks -------

if 'database' not in os.listdir('.'):
    os.mkdir('database') 
    os.chdir('database')
    db_specs = create_db()
else:
    os.chdir("./database")
    if "data.db" not in os.listdir():
        db_specs = create_db()
    else:
        db_path = os.path.abspath('.')
        db_path += '/data.db'
        db_specs = connect_db(db_path)

# takes db_specs to perform opeartions or db 

if db_specs == False:
    raise DB_CREDS_EMPTY("Database connection and cursor are not assigned")

# ------ daemon functions --------

while True:
    request = sys.stdin.readline().strip()
    command, *args = request.split()
    
    if command == "EXIT":
        break 
    elif command == "AUTH":
        _, login, password = request.split()
        if check_if_exists(db_specs[1],login,password) == True:
            print("AUTH_OK",flush=True)
        else:
            print("AUTH_FAIL",flush=True)
