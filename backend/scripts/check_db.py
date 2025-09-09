import sqlite3
import os
import json

# Path to the database file, located in the 'backend' directory
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'database.db')

if not os.path.exists(DATABASE_PATH):
    print("Database file not found. Please run init_db.py first.")
else:
    try:
        # Connect to the database
        db = sqlite3.connect(DATABASE_PATH)
        # Use a row factory to access columns by name
        db.row_factory = sqlite3.Row
        cursor = db.cursor()

        # Select all rooms
        print("Fetching all rooms from the database...\n")
        cursor.execute("SELECT * FROM rooms")
        rows = cursor.fetchall()

        if not rows:
            print("The 'rooms' table is empty.")
        else:
            # Print each row in a readable format
            for i, row in enumerate(rows):
                print(f"--- Room {i+1} ---")
                for key in row.keys():
                    value = row[key]
                    # Try to pretty-print JSON strings
                    if isinstance(value, str) and (value.startswith('[') or value.startswith('{')):
                        try:
                            parsed_json = json.loads(value)
                            print(f"{key}:")
                            print(json.dumps(parsed_json, indent=2, ensure_ascii=False))
                        except json.JSONDecodeError:
                            print(f"{key}: {value}")
                    else:
                        print(f"{key}: {value}")
                print("-" * (len(f"--- Room {i+1} ---")) + "\n")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'db' in locals() and db:
            db.close()