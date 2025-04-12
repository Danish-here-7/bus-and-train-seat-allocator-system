import sqlite3

def execute_sql_script(file_path):
    try:
        # Connect to SQLite database (it will create the file if it doesn't exist)
        conn = sqlite3.connect('ALLOCATEIT.db')
        cursor = conn.cursor()

        # Open the SQL script file
        with open(file_path, 'r') as file:
            sql_script = file.read()
            cursor.executescript(sql_script)  # Execute the SQL script

        conn.commit()  # Commit the changes to the database
        print("✅ Database initialized successfully.")
        conn.close()
    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
