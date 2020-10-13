'''Bestand waar module in staat van parkeren

Auteur: Ralph van Leeuwen'''

import sqlite3

class Parkeren:
    '''Hierin staat alles voor het in en uit gaan van de parkeerplaats
    '''

    def __init__(self):
        '''Zet globale variable waardes'''

        # Globale vars
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

    def parkeer(self, tag, optie):
        '''Hierin wordt besloten of je mag parkeren

        Args:
        tag(int) -- Tag van de QR of RFID.
        optie(bool) -- Of je in of uit wilt, True is in False is uit.

        Returns:
        result(bool) -- Resultaat of het parkeren gelukt is.
        message(string) -- Bericht van eventuele foutmelding of speciale opmerkingen.
        '''

        # Waardes nodig binnen deze functie
        parkeerplaatsen = self.tel_parkeerplaatsen()
        voorangparkeerplaatsen = self.tel_voorangparkeerplaatsen()
        persoons_id = self.get_persoonid(tag)
        parkeer = self.check_parkeer(persoons_id)
        voorang = self.check_voorang(persoons_id)

        # Uitrekenen van andere waardes op basis van vooraf opgehaalde waardes
        normaal_beschikbaar = (self.totaal_parkeerplaatsen - self.totaal_voorangparkeerplaatsen) - parkeerplaatsen
        voorang_beschikbaar = self.totaal_voorangparkeerplaatsen - voorangparkeerplaatsen
        if not optie:
            if parkeer or voorang:
                out_parkeerplaats(tag)
                return True, 'U heeft de parkeergarage verlaten.'
            return False, 'U mag niet parkeren, dus u kant de parkeergarage ook niet verlaten.'
            
        if not parkeer:
            return False, 'U bent niet toegestaan om te parkeren.'
        elif parkeer and not voorang and normaal_beschikbaar <= 0:
            return False, 'Er zijn geen normale parkeerplekken meer over.'
        elif parkeer and voorang and voorang_beschikbaar <= 0 and normaal_beschikbaar <=0:
            return False, 'Er zijn geen normale parkeerplekken of voorangsparkeerplekken meer over'
        elif parkeer and normaal_beschikbaar >= 1:
            self.in_parkeerplaats(tag, persoons_id)
            return True, 'U bent geparkeerd op een reguliere parkeerplaats.'
        elif not parkeer and voorang and voorang_beschikbaar >= 1:
            self.in_voorang_parkeerplaats(tag, persoons_id)
            return True, 'U bent geparkeerd op een voorangsparkeerplaats.'
        return False, 'Er is iets mis gegaan aan de technische kant, heb je de database gesloopt?'



