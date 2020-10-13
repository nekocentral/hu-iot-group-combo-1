import sqlite3

c = sqlite3.connect('toegangssysteem.db')
c.execute('''DROP TABLE IF EXISTS tags;''')
c.execute('''DROP TABLE IF EXISTS personen;''')
c.execute('''DROP TABLE IF EXISTS parkeerplaatsen;''')
c.commit()

c.execute('''CREATE TABLE IF NOT EXISTS personen (
   persoons_id INTEGER PRIMARY KEY,
   voornaam TEXT,
   achternaam TEXT,
   parkeren TEXT,
   prioriteit_parkeren TEXT,
   fietsenstalling TEXT,
   ruimte1 TEXT,
   ruimte2 TEXT
);''')

c.execute('''CREATE TABLE IF NOT EXISTS tags (
    tag_id INTEGER PRIMARY KEY,
    is_qr INTEGER,
    is_rfid INTEGER,
    persoons_id INTEGER,
    FOREIGN KEY (persoons_id) REFERENCES personen(persoons_id)
);''')

c.execute('''CREATE TABLE IF NOT EXISTS parkeerplaatsen (
    parkeer_id INTEGER PRIMARY KEY,
    voorang INTEGER,
    tag_id INTEGER,
    persoons_id INTEGER,
    FOREIGN KEY (tag_id)
        REFERENCES tags (tag_id),
    FOREIGN KEY (persoons_id)
        REFERENCES personen (persoons_ID)
);''')
c.commit()
c.close()
