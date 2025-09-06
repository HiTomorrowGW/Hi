import os
import sqlite3
from flask import g

# Path to the database file, located in the 'backend' directory
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')

def get_db():
    print(f"Database path: {DATABASE_PATH}") # for debugging
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
    db = get_db()
    cursor = db.cursor()
    # The schema.sql file is in the same directory as this file
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.sql')
    with open(schema_path, 'r') as f:
        cursor.executescript(f.read())
    db.commit()
    cursor.close()

def init_app(app):
    app.teardown_appcontext(close_db)