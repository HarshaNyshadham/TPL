import sqlite3
import os

def main():
    db_path = os.path.join('instance', 'tpl.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("Database Tables:")
    for table in tables:
        table_name = table[0]
        print(f"\n{table_name}:")
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
    
    conn.close()

if __name__ == '__main__':
    main() 