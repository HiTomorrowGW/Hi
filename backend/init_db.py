# backend/init_db.py
import sqlite3
import os
import json

# This script will initialize the database directly, without using the Flask app.

# Path to the database file, located in the 'backend' directory
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')

# Path to the schema.sql file
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.sql')

print("Initializing the database...")

if os.path.exists(DATABASE_PATH):
    os.remove(DATABASE_PATH)
    print(f"Removed old database at {DATABASE_PATH}")

try:
    # Connect to the database (this will create the file)
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.cursor()

    # Read and execute the schema.sql file
    print(f"Reading schema from {SCHEMA_PATH}")
    with open(SCHEMA_PATH, 'r') as f:
        cursor.executescript(f.read())
    
    print("Tables created. Inserting sample data...")

    # Insert sample room data
    rooms_to_add = [
        {
            "name": "스탠다드",
            "description": "혼자 여행객을 위한 완벽한 방입니다. 편안한 침대와 모든 필수 편의시설을 갖추고 있습니다.",
            "price": 75000,
            "image_url": "/images/1/main.jpg",
            "amenities": ["와이파이", "에어컨", "책상"],
            "additional_images": [],
            "tags": ["가성비", "1인실"]
        },
        {
            "name": "디럭스",
            "description": "커플이나 친구와 함께 사용하기 좋은 넓은 공간입니다. 퀸 사이즈 침대가 제공됩니다.",
            "price": 120000,
            "image_url": "/images/2/main.jpg",
            "amenities": ["와이파이", "TV", "미니바", "욕조"],
            "additional_images": [],
            "tags": ["커플 추천", "넓은 공간"]
        },
        {
            "name": "파노라마 뷰",
            "description": "가족 단위 여행객을 위한 최고의 선택. 별도의 거실 공간과 여러 개의 침대가 마련되어 있습니다.",
            "price": 200000,
            "image_url": "/images/1/main.jpg",
            "amenities": ["와이파이", "TV", "주방 시설", "세탁기"],
            "additional_images": [],
            "tags": ["가족 여행", "취사 가능"]
        },
        {
            "name": "트리플",
            "description": "아름다운 바다 전망을 자랑하는 방입니다. 발코니에서 멋진 일출을 감상하세요.",
            "price": 180000,
            "image_url": "/images/2/main.jpg",
            "amenities": ["와이파이", "TV", "발코니", "오션뷰"],
            "additional_images": [],
            "tags": ["오션뷰", "로맨틱"]
        },
        {
            "name": "패밀리",
            "description": "출장객을 위한 실용적인 공간. 두 개의 싱글 침대와 업무용 책상이 준비되어 있습니다.",
            "price": 110000,
            "image_url": "/images/1/main.jpg",
            "amenities": ["와이파이", "책상", "프린터 대여"],
            "additional_images": [],
            "tags": ["비즈니스", "출장"]
        }
    ]

    for room in rooms_to_add:
        cursor.execute(
            "INSERT INTO rooms (name, description, price, image_url, amenities, additional_images, tags) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                room["name"],
                room["description"],
                room["price"],
                room["image_url"],
                json.dumps(room["amenities"]),
                json.dumps(room["additional_images"]),
                json.dumps(room["tags"])
            )
        )

    # Commit the changes and close the connection
    db.commit()
    cursor.close()
    db.close()

    print("Database initialized successfully with 5 sample rooms.")

except Exception as e:
    print(f"An error occurred during database initialization: {e}")