import sqlite3
def create_database():
    conn = sqlite3.connect(
        "users.db"
    )
    cursor = conn.cursor()
    cursor.execute(
    """CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        bio TEXT DEFAULT '',
        profile_image TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        
    )
    """
    )
    conn.commit()
    conn.close()
create_database()
print(
    "Database Created Successfully"
)