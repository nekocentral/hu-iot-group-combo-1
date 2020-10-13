'''Bestand waar module in staat van parkeren

Auteur: Ralph van Leeuwen'''

import sqlite3

class Parkeren:
    '''Hierin staat alles voor het in en uit gaan van de parkeerplaats
    '''

    def __init__(self):
        '''Zet globale variable waardes'''

        # Globale vars
        self.totaal_parkeerplaatsen = 4
        self.totaal_voorangparkeerplaatsen = 3
        self.database_name = 'toegangssysteem.db'

    def tel_parkeerplaatsen(self):
        '''Telt het aantal in beslag genomen parkeerplaatsen.
        
        Args:
        None
        
        Returns:
        count(int) -- Aantal in beslag genomen parkeerplaatsen.'''

        # Haalt benodigde waardes op vanuit database
        connection = sqlite3.connect(self.database_name)
        counts = connection.execute('''SELECT COUNT (*) FROM parkeerplaatsen''')

        # Haalt gewenste data uit waardes
        for count in (counts.fetchall()):
            connection.close()
            return count[0]


    def tel_voorangparkeerplaatsen(self):
        '''Telt het aantal in beslag genomen voorang parkeerplaatsen.

        Args:
        None
        
        Returns:
        count(int) -- Aantal in beslag genomen parkeerplaatsen met voorang.'''

        connection = sqlite3.connect(self.database_name)
        counts = connection.execute('''SELECT COUNT (*) FROM parkeerplaatsen WHERE voorang == 1''')

        for count in (counts.fetchall()):
            connection.close()
            return count[0]

    def get_persoonid(self, tag):
        '''Haalt persoon_id op vanuit de database die weer met andere
        functies gebruikt gaan worden

        Args:
        tag(int) -- Tag van de QR of RFID

        Returns:
        Persoons_id(int) -- ID van het persoon uit de database.
        '''

        # Haalt benodigde waardes op vanuit database
        connection = sqlite3.connect(self.database_name)
        persoons_ids = connection.execute('''SELECT * FROM tags WHERE tag_id == {0}'''.format(str(tag)))
        
        # Haalt gewenste data uit waardes
        for persoons_id in (persoons_ids.fetchall()):
            connection.close()
            return persoons_id[3]
        
    def check_parkeer(self, persoons_id):
        '''Haalt op basis van informatie van tag van QR code of RFID
        de juiste parkeer rechten op
        
        Args:
        persoons_id(int) -- ID van het persoon
        
        Returns:
        parkeren(bool) -- True of False of deze persoon in het systeem gevonden is voor parkeren'''

        # Haalt waardes op op basis van persoons_id in database
        connection = sqlite3.connect(self.database_name)
        results = connection.execute('''SELECT * FROM personen WHERE persoons_id == {0}'''.format(str(persoons_id)))

        # Verwerkt query en returned op basis van of hij mag parkeren of niet.
        for result in (results.fetchall()):
            connection.close()
            if (result[3] == 1):
                return True
            return False
      

    def check_voorang(self, persoons_id):
        '''Haalt op basis van informatie van tag van QR code of RFID
        code de rechten op of deze persoon voorang heeft.
        
        Args:
        persoons_id(int) -- ID van het persoon
        
        Returns:
        voorang(bool) -- True of False of dit persoon voorang heeft'''

        # Zet database connectie op
        connection = sqlite3.connect(self.database_name)
        results = connection.execute('''SELECT * FROM personen WHERE persoons_id == {0}'''.format(str(persoons_id)))

        # Verwerkt query en returned op basis van of hij mag parkeren of niet.
        for result in (results.fetchall()):
            connection.close()
            if (result[4] == 1):
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

        # Genereerd ID
        parkeer_id = id('random')

        # Voert query uit en commit deze
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

        # Genereerd ID
        parkeer_id = id('random')

        # Voert query uit en commit deze
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

        # Voert query uit voor het verwijderen van waarde
        connection = sqlite3.connect(self.database_name)
        connection.execute('''DELETE FROM parkeerplaatsen WHERE tag_id == {0}'''.format(str(tag)))
        connection.commit()
        connection.close()

    def is_geparkeerd(self, tag):
        '''Aangezien een tag maar een keer mag parkeren controleerd
        deze functie of de tag al geparkeerd staat

        Args:
        tag(int) -- Tag van de QR of RFID

        Returns:
        al_geparkeerd(bool) -- True is wel geparkeerd False is niet geparkeerd
        result(string) -- Onder welk ID je al geparkeerd bent'''

        # Zet database connectie op
        connection = sqlite3.connect(self.database_name)
        results = connection.execute('''SELECT * FROM parkeerplaatsen WHERE tag_id == {0}'''.format(str(tag)))

        # Verwerkt query en returned op basis van of hij mag parkeren of niet.
        for result in (results.fetchall()):
            connection.close()
            return True, str(result[0])
        connection.close()
        return False, ''
    
    def check_bestaat(self, tag):
        '''Aangezien het geen zin heeft verwerkingen te gaan doen van
        een tag die niet bekend is in het systeem doet deze functie
        hier een controle op.

        Args:
        tag(int) -- Tag van de QR of RFID

        Returns:
        bestaat(bool) -- True of False indien deze wel of niet gevonden is.
        '''

        connection = sqlite3.connect(self.database_name)
        results = connection.execute('''SELECT * FROM tags WHERE tag_id == {0}'''.format(str(tag)))

        # Verwerkt query en returned op basis van of hij mag parkeren of niet.
        for result in (results.fetchall()):
            connection.close()
            return True, result
        connection.close()
        return False, ''      


    def parkeer(self, tag, optie):
        '''Hierin wordt besloten of je mag parkeren

        Args:
        tag(int) -- Tag van de QR of RFID.
        optie(bool) -- Of je in of uit wilt, True is in False is uit.

        Returns:
        result(bool) -- Resultaat of het parkeren gelukt is.
        message(string) -- Bericht van eventuele foutmelding of speciale opmerkingen.
        '''

        # Vooraf een check of de tag wel bestaat
        if not (self.check_bestaat(tag))[0]:
            return False, 'Deze tag staat niet in ons systeem.'

        # Waardes nodig binnen deze functie
        parkeerplaatsen = self.tel_parkeerplaatsen()
        voorangparkeerplaatsen = self.tel_voorangparkeerplaatsen()
        persoons_id = self.get_persoonid(tag)
        parkeer = self.check_parkeer(persoons_id)
        voorang = self.check_voorang(persoons_id)

        # Controleren of deze persoon al geparkeerd staat
        is_geparkeerd = self.is_geparkeerd(tag)
        if (is_geparkeerd[0]) and optie:
            return False, 'U heeft al een parkeerplek onder het ID {0}'.format(is_geparkeerd[1])

        # Uitrekenen van andere waardes op basis van vooraf opgehaalde waardes
        normaal_beschikbaar = (self.totaal_parkeerplaatsen - self.totaal_voorangparkeerplaatsen) - parkeerplaatsen
        voorang_beschikbaar = self.totaal_voorangparkeerplaatsen - voorangparkeerplaatsen
        if not optie:
            if parkeer or voorang:
                self.out_parkeerplaats(tag)
                return True, 'U heeft de parkeergarage verlaten.'
            return False, 'U mag niet parkeren, dus u kan de parkeergarage ook niet verlaten.'
            
        if not parkeer:
            return False, 'U bent niet toegestaan om te parkeren.'
        if parkeer and not voorang and normaal_beschikbaar <= 0:
            return False, 'Er zijn geen normale parkeerplekken meer over.'
        if parkeer and voorang and voorang_beschikbaar <= 0 and normaal_beschikbaar <=0:
            return False, 'Er zijn geen normale parkeerplekken of voorangsparkeerplekken meer over'
        if parkeer and normaal_beschikbaar >= 1:
            self.in_parkeerplaats(tag, persoons_id)
            return True, 'U bent geparkeerd op een reguliere parkeerplaats.'
        if parkeer and voorang and voorang_beschikbaar >= 1:
            self.in_voorang_parkeerplaats(tag, persoons_id)
            return True, 'U bent geparkeerd op een voorangsparkeerplaats.'
        return False, 'Er is iets mis gegaan aan de technische kant, heb je de database gesloopt?'
