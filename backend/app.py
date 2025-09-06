import os
import json
import sqlite3
from flask import Flask, jsonify, g, send_from_directory, request
from database import init_app, get_db

app = Flask(__name__, static_folder='../', static_url_path='/')
init_app(app) # Register teardown function

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if path.startswith('backend/'):
        return "", 404
    return send_from_directory(app.static_folder, path)

@app.route('/api/rooms', methods=['POST'])
def create_room():
    db = get_db()
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    image_url = data.get('image_url')
    amenities = data.get('amenities', [])
    additional_images = data.get('additional_images', [])
    tags = data.get('tags', [])

    if not all([name, description, price, image_url]):
        return jsonify({"error": "Missing data"}), 400

    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO rooms (name, description, price, image_url, amenities, additional_images, tags) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, description, price, image_url, json.dumps(amenities), json.dumps(additional_images), json.dumps(tags))
        )
        new_room_id = cursor.lastrowid

        room_image_folder = os.path.join(app.static_folder, 'images', str(new_room_id))
        os.makedirs(room_image_folder, exist_ok=True)

        final_image_url = f'/images/{new_room_id}/{os.path.basename(image_url)}'
        
        cursor.execute(
            "UPDATE rooms SET image_url = ? WHERE id = ?",
            (final_image_url, new_room_id)
        )

        cursor.execute('SELECT * FROM rooms WHERE id = ?', (new_room_id,))
        new_room = cursor.fetchone()
        
        db.commit()
        return jsonify(dict(new_room)), 201

    except Exception as error:
        print("Error while creating room", error)
        db.rollback()
        return jsonify({"error": "Database error"}), 500

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM rooms')
    rooms = cursor.fetchall()
    
    rooms_list = []
    for room in rooms:
        room_dict = dict(room)
        for field in ['amenities', 'additional_images', 'tags']:
            if room_dict.get(field) and isinstance(room_dict[field], str):
                try:
                    room_dict[field] = json.loads(room_dict[field])
                except json.JSONDecodeError:
                    room_dict[field] = []
            elif not room_dict.get(field):
                 room_dict[field] = []
        rooms_list.append(room_dict)
        
    return jsonify(rooms_list)

@app.route('/api/rooms/<int:room_id>')
def get_room(room_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM rooms WHERE id = ?', (room_id,))
    room = cursor.fetchone()
        
    if room is None:
        return jsonify({"error": "Room not found"}), 404
    
    room_dict = dict(room)
    for field in ['amenities', 'additional_images', 'tags']:
        if room_dict.get(field) and isinstance(room_dict[field], str):
            try:
                room_dict[field] = json.loads(room_dict[field])
            except json.JSONDecodeError:
                room_dict[field] = []
        elif not room_dict.get(field):
            room_dict[field] = []
            
    return jsonify(room_dict)

if __name__ == '__main__':
    app.run(debug=True, port=5000)