import sqlite3 

def init_db():
    con = sqlite3.connect("tasks.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS tasks(name,time,description,date)")
    return con, cur

def add_task(name,time,description="",date=""):
    con, cur = init_db()
    cur.execute(f"INSERT INTO tasks values ('{name}','{time}','{description}','{date}')")
    con.commit()
    con.close()

