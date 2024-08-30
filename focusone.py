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

def parse_time(time_input: str) -> int:
    """Convert natural language time input into seconds. Example: '1h 30m 45s' to 5445 seconds."""
    
    if not time_input.strip():
        raise ValueError("Input string is empty or invalid")
    
    time_units = {
        'h': 3600,
        'm': 60,
        's': 1
    }

    time_input = time_input.split()
    time_parsed = 0

    if len(time_input) > 3:
        raise ValueError("More than 3 time units are not allowed")

    for time in time_input:
        time_tail = time[-1]
        try:
            n = int(time[:-1])
        except ValueError:
            raise ValueError(f"Invalid time value: '{time[:-1]}' cannot be converted to an integer")

        if time_tail in time_units:
            time_parsed += n * time_units[time_tail]
        else:
            raise ValueError(f"Invalid time unit: '{time_tail}'")

    return time_parsed


