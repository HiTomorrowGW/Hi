import sqlite3
import pandas as pd
import os
import json

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'database.db')
EXCEL_PATH = os.path.join(BASE_DIR, '..', 'rooms.xlsx')

def import_excel_to_db():
    """
    Reads data from an Excel file and imports/updates the 'rooms' table in the SQLite database.
    """
    if not os.path.exists(EXCEL_PATH):
        print(f"Excel file not found at {EXCEL_PATH}. Please export data first.")
        return

    if not os.path.exists(DB_PATH):
        print(f"Database file not found at {DB_PATH}. Please run init_db.py first.")
        return

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Read the Excel file into a DataFrame
        print(f"Reading data from {EXCEL_PATH}...")
        df = pd.read_excel(EXCEL_PATH, engine='openpyxl')

        print("Processing data for import/update...")
        for index, row in df.iterrows():
            room_id = row.get('id')
            name = row.get('name')
            description = row.get('description')
            price = row.get('price')
            image_url = row.get('image_url')
            amenities = json.dumps(row.get('amenities', [])) if isinstance(row.get('amenities'), list) else json.dumps([])
            additional_images = json.dumps(row.get('additional_images', [])) if isinstance(row.get('additional_images'), list) else json.dumps([])
            tags = json.dumps(row.get('tags', [])) if isinstance(row.get('tags'), list) else json.dumps([])

            # Check if room_id exists for update, otherwise insert
            if room_id is not None and pd.notna(room_id): # Check for NaN from Excel
                cursor.execute("SELECT id FROM rooms WHERE id = ?", (int(room_id),))
                existing_room = cursor.fetchone()

                if existing_room:
                    # Update existing room
                    cursor.execute(
                        """
                        UPDATE rooms SET name=?, description=?, price=?, image_url=?, amenities=?, additional_images=?, tags=?
                        WHERE id=?
                        """,
                        (name, description, price, image_url, amenities, additional_images, tags, int(room_id))
                    )
                    print(f"Updated room with ID: {int(room_id)}")
                else:
                    # Insert new room if ID is provided but doesn't exist (this might be an error case or intended for new records with specific IDs)
                    # For simplicity, if ID is provided but doesn't exist, we'll insert it.
                    # In a real app, you might want to handle this differently (e.g., only insert if ID is None/empty)
                    cursor.execute(
                        """
                        INSERT INTO rooms (id, name, description, price, image_url, amenities, additional_images, tags)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (int(room_id), name, description, price, image_url, amenities, additional_images, tags)
                    )
                    print(f"Inserted new room with provided ID: {int(room_id)}")
            else:
                # Insert new room (ID will be auto-incremented)
                cursor.execute(
                    """
                    INSERT INTO rooms (name, description, price, image_url, amenities, additional_images, tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (name, description, price, image_url, amenities, additional_images, tags)
                )
                print(f"Inserted new room (auto-ID)")

        # Commit the changes
        conn.commit()
        print("Import/Update successful!")

    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback() # Rollback changes on error
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    import_excel_to_db()