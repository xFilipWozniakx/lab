import sys
import sqlite3
import os
import bcrypt

# ---------------------------------- default vars -------------------------------------------
DB_PATH = "./photo_sync/database/data.db"

# ----------------------------------classes-----------------------------------------------------------


class DB_CREDS_EMPTY(Exception):
    pass


# ----------------------------------functions-----------------------------------------------------------


def create_db(login="admin", password="password"):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)

    password_hash = hash_pass(password)

    cur.execute(
        "INSERT INTO users (login, password_hash) VALUES (?, ?)",
        (login, password_hash),
    )

    con.commit()
    return con, cur


def connect_db(db_path=DB_PATH):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    return con, cur


def insert_into_users(cursor, connect, login="user", password="password"):
    try:
        password = hash_pass(password)
        cursor.execute(
            "INSERT INTO users( login, password_hash) VALUES (?, ?)", (login, password)
        )
        connect.commit()
        return True
    except sqlite3.Error as exc:
        print(f"Failed to insert user: {exc}", file=sys.stderr)
        return False


def hash_pass(password):
    password = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    if bcrypt.checkpw(password, hashed_password):
        return hashed_password.decode("utf-8")
    else:
        print("passwords doesnt match")


def check_if_exists(cur, login, password) -> bool:

    result = cur.execute(
        "SELECT password_hash FROM USERS where login = ?", (login,)
    ).fetchone()
    if result is None:
        return False
    passw = result[0]
    result = bcrypt.checkpw(password.encode("utf-8"), passw.encode("utf-8"))
    return result


def retrieve_all(cursor):
    for row in cursor.execute("SELECT * FROM USERS;"):
        print(row)


# ----------------------------------------program starts ----------------------------------------


# ------ db creation & checks -------

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

db_specs = connect_db()

db_specs[1].execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL
    )
""")
db_specs[0].commit()

if not check_if_exists(db_specs[1], "admin", "password"):
    if not insert_into_users(
        db_specs[1],
        db_specs[0],
        login="admin",
        password="password",
    ):
        raise RuntimeError("Failed to initialize admin account")

# ------ daemon functions --------
while True:
    request = sys.stdin.readline().strip()
    if request != "":
        _, login, password = request.split("|")
        # print(f'pro: {_} log: {login} pass: {password}')
        # sys.stdout.write(f"{_}, {login}, {password}\n")
        # sys.stdout.flush()

        result = check_if_exists(db_specs[1], login, password)

        if _ == "AUTH":
            if result == True:
                sys.stdout.buffer.write(b"\xdc")
                sys.stdout.flush()
            elif result == False:
                sys.stdout.buffer.write(b"\xdd")
                sys.stdout.flush()
        else:
            print("did see auth")
