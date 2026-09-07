import sqlite3

def create_database():
    conn = sqlite3.connect("tickets.db")

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
            status TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_ticket(data):
    conn = sqlite3.connect("tickets.db")

    conn.execute("""
        INSERT INTO tickets
        (employee_name, email, title, description, department,
         category, severity, priority, confidence, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["employee_name"],
        data["email"],
        data["title"],
        data["description"],
        data["department"],
        data["category"],
        data["severity"],
        data["priority"],
        data["confidence"],
        data["status"]
    ))

    conn.commit()
    conn.close()


def get_tickets():
    conn = sqlite3.connect("tickets.db")
    conn.row_factory = sqlite3.Row

    tickets = conn.execute(
        "SELECT * FROM tickets ORDER BY ticket_id DESC"
    ).fetchall()

    conn.close()

    return tickets