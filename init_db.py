import sqlite3

def execute_sql_script(filename):
    with open(filename, 'r') as f:
        sql_script = f.read()
    conn = sqlite3.connect('allocateit.db')
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    execute_sql_script('setup.sql')
    print("✅ Database initialized successfully.")
