import sqlite3 

def init_db():
    con = sqlite3.connect("tasks.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS 
    tasks(id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    time TEXT NOT NULL,
    description TEXT,
    date TEXT)
    """)

    return con, cur

def add_task(name,time,description="",date=""):
    con, cur = init_db()
    cur.execute(f"INSERT INTO tasks (name, time, description, date) VALUES ('{name}','{time}','{description}','{date}')")
    con.commit()
    con.close()


def get_tasks():
    con, cur = init_db()
    res=cur.execute("SELECT * FROM TASKS")
    tasks=res.fetchall()
    con.close()
    return tasks
def parse_time(time):
    return time

