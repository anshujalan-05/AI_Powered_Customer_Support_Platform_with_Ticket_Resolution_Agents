import sqlite3

DATABASE_NAME = "tickets.db"


# =========================================================
# CREATE DATABASE
# =========================================================

def create_database():

    conn = sqlite3.connect(DATABASE_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tickets (

            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,

            employee_name TEXT,

            email TEXT,

            title TEXT,

            description TEXT,

            department TEXT,

            category TEXT,

            severity TEXT,

            priority TEXT,

            confidence REAL,

            status TEXT,

            resolution TEXT
        )
    """)

    # Check existing columns
    columns = conn.execute(
        "PRAGMA table_info(tickets)"
    ).fetchall()

    column_names = [
        column[1]
        for column in columns
    ]

    # Add resolution column if missing
    if "resolution" not in column_names:

        conn.execute("""
            ALTER TABLE tickets
            ADD COLUMN resolution TEXT
        """)

    conn.commit()
    conn.close()


# =========================================================
# SAVE TICKET
# =========================================================

def save_ticket(data):

    conn = sqlite3.connect(DATABASE_NAME)

    conn.execute("""
        INSERT INTO tickets
        (
            employee_name,
            email,
            title,
            description,
            department,
            category,
            severity,
            priority,
            confidence,
            status,
            resolution
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        data.get("employee_name", ""),
        data.get("email", ""),
        data.get("title", ""),
        data.get("description", ""),
        data.get("department", ""),
        data.get("category", ""),
        data.get("severity", ""),
        data.get("priority", ""),
        data.get("confidence", 0),
        data.get("status", "Open"),
        data.get("resolution", "")

    ))

    conn.commit()
    conn.close()


# =========================================================
# GET ALL TICKETS
# =========================================================

def get_tickets():

    conn = sqlite3.connect(DATABASE_NAME)

    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT *
        FROM tickets
        ORDER BY ticket_id DESC
    """).fetchall()

    tickets = [
        dict(row)
        for row in rows
    ]

    conn.close()

    return tickets


# =========================================================
# GET SINGLE TICKET
# =========================================================

def get_ticket(ticket_id):

    conn = sqlite3.connect(DATABASE_NAME)

    conn.row_factory = sqlite3.Row

    row = conn.execute("""
        SELECT *
        FROM tickets
        WHERE ticket_id = ?
    """, (ticket_id,)).fetchone()

    conn.close()

    if row is None:
        return None

    return dict(row)


# =========================================================
# UPDATE TICKET STATUS
# =========================================================

def update_ticket_status(ticket_id, new_status):

    conn = sqlite3.connect(DATABASE_NAME)

    conn.execute("""
        UPDATE tickets
        SET status = ?
        WHERE ticket_id = ?
    """, (
        new_status,
        ticket_id
    ))

    conn.commit()
    conn.close()