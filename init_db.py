import sqlite3

def initialize_database():
    conn = sqlite3.connect("allocateit.db")
    cursor = conn.cursor()

    with open("setup.sql", "r") as f:
        sql = f.read()

    cursor.executescript(sql)
    conn.commit()
    conn.close()
    print("✅ Database created and initialized!")

if __name__ == "__main__":
    initialize_database()
