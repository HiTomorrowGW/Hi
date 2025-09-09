import sqlite3
import pandas as pd
import os

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'database.db')
EXCEL_PATH = os.path.join(BASE_DIR, '..', 'rooms.xlsx')

def export_db_to_excel():
    """
    Connects to the SQLite database, reads the 'rooms' table,
    and exports it to an Excel file.
    """
    if not os.path.exists(DB_PATH):
        print(f"Database file not found at {DB_PATH}. Please run init_db.py first.")
        return

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(DB_PATH)

        # Use pandas to read the entire 'rooms' table into a DataFrame
        print("Reading data from 'rooms' table...")
        df = pd.read_sql_query("SELECT * FROM rooms", conn)

        # Close the connection
        conn.close()

        # Export the DataFrame to an Excel file
        print(f"Exporting data to {EXCEL_PATH}...")
        df.to_excel(EXCEL_PATH, index=False, engine='openpyxl')

        print("Export successful!")
        print(f"File saved at: {EXCEL_PATH}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    export_db_to_excel()