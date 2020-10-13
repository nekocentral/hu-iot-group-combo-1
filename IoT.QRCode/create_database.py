import sqlite3

c = sqlite3.connect('toegangssysteem.db')
c.execute('''DROP TABLE IF EXISTS tags;''')
c.execute('''DROP TABLE IF EXISTS personen;''')
c.execute('''DROP TABLE IF EXISTS parkeerplaatsen;''')
c.execute('''DROP TABLE IF EXISTS ruimtes;''')
c.execute('''DROP TABLE IF EXISTS toegang;''')
c.execute('''DROP TABLE IF EXISTS log;''')

c.commit()

c.execute('''CREATE TABLE IF NOT EXISTS personen (
   persoons_id INTEGER PRIMARY KEY,
   voornaam TEXT,
   achternaam TEXT,
   parkeren INTEGER,
   prioriteit_parkeren INTEGER
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

c.execute('''CREATE TABLE IF NOT EXISTS ruimtes (
    ruimte_id INTEGER PRIMARY KEY,
    ruimte_naam TEXT
);''')

c.execute('''CREATE TABLE IF NOT EXISTS toegang (
    toegang_id INTEGER PRIMARY KEY,
    persoons_id INTEGER,
    ruimte_id INTEGER,
    heeft_toegang INTEGER,
    FOREIGN KEY (persoons_id)
        REFERENCES ruimtes (persoons_id),
    FOREIGN KEY (ruimte_id)
        REFERENCES personen (ruimte_id)
);''')

c.execute('''CREATE TABLE IF NOT EXISTS log (
    logline INTEGER PRIMARY KEY,
    tag_id INTEGER,
    persoons_id INTEGER,
    ruimte_id INTEGER,
    toegang_id INTEGER,
    logregel TEXT,
    FOREIGN KEY (tag_id)
        REFERENCES tags (tag_id),
    FOREIGN KEY (persoons_id)
        REFERENCES ruimtes (persoons_id),
    FOREIGN KEY (ruimte_id)
        REFERENCES personen (ruimte_id),
    FOREIGN KEY (toegang_id)
        REFERENCES toegang (toegang_id)
);''')

c.commit()
c.close()
