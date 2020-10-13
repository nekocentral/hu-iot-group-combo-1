'''Bestand waar module in staat van parkeren

Auteur: Ralph van Leeuwen'''

import sqlite3

class Parkeren:
    '''Hierin staat alles voor het in en uit gaan van de parkeerplaats
    '''

    def __init__(self):
        self.totaal_parkeerplaatsen = 20
        self.totaal_voorangparkeerplaatsen = 3
        self.database_name = 'toegangssysteem.db'

    def tel_parkeerplaatsen(self):
        '''Telt het aantal beschikbare parkeerplaatsen.
        
        Args:
        None
        
        Returns:
        count(int) -- Aantal beschikbare parkeerplaatsen.'''

        connection = sqlite3.connect(self.database_name)
        count = connection.execute('''SELECT COUNT (*) FROM parkeerplaatsen''')
        connection.close()

        return count


    def tel_voorangparkeerplaatsen(self):
        '''Telt het aantal beschikbare voorang parkeerplaatsen.

        Args:
        None
        
        Returns:
        count(int) -- Aantal beschikbare parkeerplaatsen met voorang.'''

        connection = sqlite3.connect(self.database_name)
        count = connection.execute('''SELECT COUNT (*) FROM parkeerplaatsen WHERE voorang == 1''')
        connection.close()

        return count

    def check_parkeer(self, tag):
        '''Haalt op basis van informatie van tag van QR code of RFID
        de juiste parkeer rechten op
        
        Args:
        tag(int) -- Tag van de QR of RFID
        
        Returns:
        parkeren(bool) -- True of False of deze persoon in het systeem gevonden is voor parkeren'''

        connection = sqlite3.connect(self.database_name)
        persoons_id = connection.execute('''SELECT * FROM tags WHERE tag_id == {0}'''.format(str(tag)))
        result = connection.execute('''SELECT * FROM personen WHERE persoons_id == {0}'''.format(str(persoons_id)))

    def check_voorang(self, tag):
        '''Haalt op basis van informatie van tag van QR code of RFID
        code de rechten op of deze persoon voorang heeft.
        
        Args:
        tag(int) -- Tag van de QR of RFID
        
        Returns:
        voorang(bool) -- True of False of dit persoon voorang heeft'''

        connection = sqlite3.connect(self.database_name)
        persoons_id = connection.execute('''SELECT * FROM tags WHERE tag_id == {0}'''.format(str(tag)))
        result = connection.execute('''SELECT * FROM personen WHERE persoons_id == {0}'''.format(str(persoons_id)))
        


