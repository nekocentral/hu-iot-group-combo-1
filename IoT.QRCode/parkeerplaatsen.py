'''Bestand waar module in staat van parkeren

Auteur: Ralph van Leeuwen'''

import sqlite3

class Parkeren:
    '''Hierin staat alles voor het in en uit gaan van de parkeerplaats
    '''

    def __init__(self):
        '''Zet globale variable waardes'''
        
        self.totaal_parkeerplaatsen = 20
        self.totaal_voorangparkeerplaatsen = 3
        self.database_name = 'toegangssysteem.db'

    def tel_parkeerplaatsen(self):
        '''Telt het aantal in beslag genomen parkeerplaatsen.
        
        Args:
        None
        
        Returns:
        count(int) -- Aantal in beslag genomen parkeerplaatsen.'''

        connection = sqlite3.connect(self.database_name)
        count = connection.execute('''SELECT COUNT (*) FROM parkeerplaatsen''')
        connection.close()

        return count


    def tel_voorangparkeerplaatsen(self):
        '''Telt het aantal in beslag genomen voorang parkeerplaatsen.

        Args:
        None
        
        Returns:
        count(int) -- Aantal in beslag genomen parkeerplaatsen met voorang.'''

        connection = sqlite3.connect(self.database_name)
        count = connection.execute('''SELECT COUNT (*) FROM parkeerplaatsen WHERE voorang == 1''')
        connection.close()

        return count


    def get_persoonid(self, tag):
        '''Haalt persoon_id op vanuit de database die weer met andere
        functies gebruikt gaan worden

        Args:
        tag(int) -- Tag van de QR of RFID

        Returns:
        Persoons_id(int) -- ID van het persoon uit de database.
        '''

        connection = sqlite3.connect(self.database_name)
        persoons_id = connection.execute('''SELECT * FROM tags WHERE tag_id == {0}'''.format(str(tag)))

        return persoons_id

    def check_parkeer(self, persoons_id):
        '''Haalt op basis van informatie van tag van QR code of RFID
        de juiste parkeer rechten op
        
        Args:
        persoons_id(int) -- ID van het persoon
        
        Returns:
        parkeren(bool) -- True of False of deze persoon in het systeem gevonden is voor parkeren'''

        connection = sqlite3.connect(self.database_name)
        result = connection.execute('''SELECT * FROM personen WHERE persoons_id == {0}'''.format(str(persoons_id)))
        connection.close()

        if (result[4] == 1):
            return True
        return False

    def check_voorang(self, persoons_id):
        '''Haalt op basis van informatie van tag van QR code of RFID
        code de rechten op of deze persoon voorang heeft.
        
        Args:
        persoons_id(int) -- ID van het persoon
        
        Returns:
        voorang(bool) -- True of False of dit persoon voorang heeft'''

        connection = sqlite3.connect(self.database_name)
        result = connection.execute('''SELECT * FROM personen WHERE persoons_id == {0}'''.format(str(persoons_id)))

        if (result[5] == 1):
            return True
        return False
        
    def in_parkeerplaats(self, tag, persoons_id):
        '''Laat je in de parkeerplaats gaan en logt
        dit ook in de database
        
        Args:
        tag(int) -- Tag van de QR of RFID
        persoons_id(int) -- ID van het persoon

        Returns:
        None'''

        parkeer_id = id('random')

        connection = sqlite3.connect(self.database_name)
        connection.execute('''INSERT INTO parkeerplaatsen (parkeer_id,voorang,tag_id,persoons_id)
        VALUES({0}, {1}, {2}, {3});'''.format(parkeer_id, 0, tag, persoons_id))
        connection.commit()
        connection.close()

    def in_voorang_parkeerplaats(self, tag, persoons_id):
        '''Laat je in de parkeerplaats gaan en logt
        dit ook in de database. Geeft ook een voorang waarde mee.
        
        Args:
        tag(int) -- Tag van de QR of RFID
        persoons_id(int) -- ID van het persoon

        Returns:
        None'''

        parkeer_id = id('random')

        connection = sqlite3.connect(self.database_name)
        connection.execute('''INSERT INTO parkeerplaatsen (parkeer_id,voorang,tag_id,persoons_id)
        VALUES({0}, {1}, {2}, {3});'''.format(parkeer_id, 1, tag, persoons_id))
        connection.commit()
        connection.close()

    def out_parkeerplaats(self, tag):
        '''Laat je de parkeerplaats uit gaan, haalt de waarde
        dat je geparkeerd bent ook uit de database.

        Args:
        tag(int) -- Tag van de QR of RFID

        Returns:
        None'''

        connection = sqlite3.connect(self.database_name)
        connection.execute('''DELETE FROM parkeerplaatsen WHERE tag_id == {0}'''.format(str(tag)))
        connection.commit()
        connection.close()






