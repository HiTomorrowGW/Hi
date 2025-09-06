DROP TABLE IF EXISTS rooms;

CREATE TABLE rooms (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT NOT NULL,
  price INTEGER NOT NULL,
  image_url TEXT,
  amenities TEXT, -- JSON list of amenities
  additional_images TEXT, -- JSON list of image URLs
  tags TEXT -- JSON list of tags
);