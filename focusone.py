import json
import sqlite3
import struct
import sys
import threading
import time

from rich.progress import Progress

import x_utils

DATABASE = "blocks.db"


def init_db():
    """Initialize the database and create the blocks table if it doesn't exist."""
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS blocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                time INTEGER NOT NULL,
                description TEXT,
                date TEXT,
                active INTEGER
            )
        """
        )
        con.commit()


def add_block(name, time, description="", date="", active=0):
    """Add a new block to the database."""
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO blocks (name, time, description, date, active)
            VALUES (?, ?, ?, ?, ?)
        """,
            (name, time, description, date, active),
        )
        con.commit()


def get_blocks():
    """Retrieve all block names from the database."""
    with sqlite3.connect(DATABASE) as con:
        con.row_factory = sqlite3.Row  # This allows accessing fields by name
        cur = con.cursor()
        cur.execute("SELECT * FROM blocks")
        blocks = cur.fetchall()
    return blocks


def update_block(
    block_id, name=None, time=None, description=None, date=None, active=None
):
    """Update an existing block in the database."""
    update_fields = []
    parameters = []

    if name is not None:
        update_fields.append("name = ?")
        parameters.append(name)
    if time is not None:
        update_fields.append("time = ?")
        parameters.append(time)
    if description is not None:
        update_fields.append("description = ?")
        parameters.append(description)
    if date is not None:
        update_fields.append("date = ?")
        parameters.append(date)
    if active is not None:
        update_fields.append("active = ?")
        parameters.append(active)

    if not update_fields:
        raise ValueError("No fields to update")

    set_clause = ", ".join(update_fields)
    parameters.append(block_id)

    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(
            f"""
            UPDATE blocks
            SET {set_clause}
            WHERE id = ?
        """,
            tuple(parameters),
        )
        con.commit()


# Initialize the database (create the table if not exists)


def parse_time(time_input: str) -> int:
    """Convert natural language time input into seconds. Example: '1h 30m 45s' to 5445 seconds."""

    if not time_input.strip():
        raise ValueError("Input string is empty or invalid")

    time_units = {"h": 3600, "m": 60, "s": 1}

    time_input = time_input.split()
    time_parsed = 0

    if len(time_input) > 3:
        raise ValueError("More than 3 time units are not allowed")

    for time in time_input:
        time_tail = time[-1]
        try:
            n = int(time[:-1])
        except ValueError:
            raise ValueError(
                f"Invalid time value: '{time[:-1]}' cannot be converted to an integer"
            )

        if time_tail in time_units:
            time_parsed += n * time_units[time_tail]
        else:
            raise ValueError(f"Invalid time unit: '{time_tail}'")

    return time_parsed


def get_act_block():
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
    cur.execute("SELECT id, name, time FROM blocks WHERE active=1")
    act_block = cur.fetchone()
    con.close()
    return act_block


def show_act(bar_opt=False):

    if get_act_block() == None:
        print("no block active")
        return

    id = get_act_block()[0]
    name = get_act_block()[1]
    seconds = get_act_block()[2]

    while seconds > 0:
        hours, remainder = divmod(seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        timer = f"{name} {hours:02d}:{minutes:02d}:{secs:02d}"

        if bar_opt:
            print(timer, flush=True)

        else:
            print(timer, end="\r")

        seconds -= 1
        time.sleep(1)

    update_block(id, time=0, active=0)


def block_distractions(programs, websites, stop_event):
    while not stop_event.is_set():
        x_utils.close_programs(allowed_programs=programs)
        block_websites(websites)
        time.sleep(1)  # Check the stop_event every second


def send_to_browser_extension(allowed_websites):
    message = json.dumps({"allowed_websites": allowed_websites})
    # Write message size as 4 byte unsigned integer (native messaging protocol)
    sys.stdout.buffer.write(struct.pack("<I", len(message)))
    sys.stdout.buffer.write(message.encode("utf-8"))
    sys.stdout.flush()


def block_websites(allowed_websites):
    try:
        send_to_browser_extension(allowed_websites)
    except Exception as e:
        print(f"Error communicating with browser extension: {e}")


def show_progress(duration_seconds, title):

    while duration_seconds > 0:
        hours, remainder = divmod(duration_seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        timer = f"{title} {hours:02d}:{minutes:02d}:{secs:02d}"

        # if bar_opt:
        #     print(timer, flush=True)
        #
        # else:
        print(timer, end="\r")

        duration_seconds -= 1
        time.sleep(1)

    # with Progress() as progress:
    #     task = progress.add_task(f"[green]Focusing on {title}", total=duration_seconds)
    #     while not progress.finished:
    #         progress.update(task, advance=1)
    #         time.sleep(1)


def start_focus_session(duration, programs_allowed, websites_allowed, block_name):
    stop_event = threading.Event()
    timer_thread = threading.Thread(target=show_progress, args=(duration, block_name))
    blocker_thread = threading.Thread(
        target=block_distractions, args=(programs_allowed, websites_allowed, stop_event)
    )

    timer_thread.start()
    blocker_thread.start()

    timer_thread.join()
    stop_event.set()  # Signal the blocker to stop
    blocker_thread.join()  # Wait for the blocker to finish


init_db()
