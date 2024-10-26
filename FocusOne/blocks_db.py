import sqlite3


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


def get_act_block():
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
    cur.execute("SELECT id, name, time FROM blocks WHERE active=1")
    result = cur.fetchone()
    con.close()
    act_block = {"id": result[0], "name": result[1], "duration": result[2]}
    return act_block


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


init_db()
