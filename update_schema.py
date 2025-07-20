import sqlite3
import os

def add_column_if_not_exists(cursor, table, column, type):
    try:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {type};")
        print(f"Added column {column} to table {table}")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e):
            print(f"Column {column} already exists in table {table}")
        else:
            print(f"Error adding column {column} to table {table}: {str(e)}")

def execute_statements(cursor, statements):
    for statement in statements:
        try:
            cursor.execute(statement)
            print(f"Executed: {statement[:50]}...")
        except sqlite3.OperationalError as e:
            print(f"Error executing statement: {str(e)}")

def main():
    db_path = os.path.join('instance', 'tpl.db')
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create new tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS player (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        partner_name VARCHAR(100),
        game_type VARCHAR(20) NOT NULL,
        division FLOAT,
        "group" VARCHAR(1),
        is_active BOOLEAN NOT NULL DEFAULT 1,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """)
    print("Created player table")
    
    # Add columns to existing tables
    add_column_if_not_exists(cursor, 'appointable', 'game_type', 'VARCHAR(20)')
    add_column_if_not_exists(cursor, 'appointable', 'season_id', 'INTEGER')
    add_column_if_not_exists(cursor, 'schedule', 'game_type', 'VARCHAR(20)')
    add_column_if_not_exists(cursor, 'schedule', 'season_id', 'INTEGER')
    
    # Update appointable table with foreign key
    appointable_statements = [
        "CREATE TABLE IF NOT EXISTS temp_appointable AS SELECT * FROM appointable;",
        "DROP TABLE appointable;",
        """CREATE TABLE appointable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team VARCHAR(100) NOT NULL,
            matches INTEGER,
            won INTEGER,
            loss INTEGER,
            bonus INTEGER,
            points INTEGER,
            "group" INTEGER,
            games_total INTEGER,
            games_won INTEGER,
            games_percentage FLOAT,
            division FLOAT,
            game_type VARCHAR(20),
            season_id INTEGER,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (season_id) REFERENCES season(id)
        );""",
        "INSERT INTO appointable SELECT * FROM temp_appointable;",
        "DROP TABLE temp_appointable;"
    ]
    execute_statements(cursor, appointable_statements)
    
    # Update schedule table with foreign key
    schedule_statements = [
        "CREATE TABLE IF NOT EXISTS temp_schedule AS SELECT * FROM schedule;",
        "DROP TABLE schedule;",
        """CREATE TABLE schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team1 VARCHAR(100) NOT NULL,
            team2 VARCHAR(100) NOT NULL,
            score VARCHAR(50),
            deadline DATETIME,
            division FLOAT,
            game_type VARCHAR(20),
            season_id INTEGER,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (season_id) REFERENCES season(id)
        );""",
        "INSERT INTO schedule SELECT * FROM temp_schedule;",
        "DROP TABLE temp_schedule;"
    ]
    execute_statements(cursor, schedule_statements)
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("Schema update completed.")

if __name__ == '__main__':
    main() 