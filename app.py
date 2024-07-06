import sqlite3 

def init_db():
    con = sqlite3.connect("tasks.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS 
    blocks(id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    time TEXT NOT NULL,
    description TEXT,
    date TEXT)
    """)

    return con, cur

def add_task(name,time,description="",date=""):
    con, cur = init_db()
    cur.execute(f"INSERT INTO blocks(name, time, description, date) VALUES ('{name}','{time}','{description}','{date}')")
    con.commit()
    con.close()


def get_tasks():
    con, cur = init_db()
    res=cur.execute("SELECT name FROM blocks")
    tasks=res.fetchall()
    con.close()
    return tasks


def parse_time(time_input):
    """"natural like time input into seconds ex: 1m to 60"""
    time_tail = [-1]
    time_parsed = 0
    n = int(time_input[:-1])
    if time_tail == "m":
        time_parsed = n*60
    
    if time_tail == "h":
        n = int(time_input[:-1])
        time_parsed = n*3600
    
        return time_parsed 
        

    
