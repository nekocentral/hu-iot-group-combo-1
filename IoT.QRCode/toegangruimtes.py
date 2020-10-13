'''Bestand waar module in staat van toegang tot
allerlij ruimtes

Auteur: Ralph van Leeuwen'''

import sqlite3

class Toegang:
    '''Hierin staat alles voor het in en uit gaan van de ruimtes
    '''

    def __init__(self):
        '''Zet globale variable waardes'''

        # Standaard waardes zijn False
        self.authenticated = False
        self.authorized = False
        self.database_name = 'toegangssysteem.db'

    def authenticate(self, tag):
        '''Binnen deze functie wordt de authenticatie gedaan
        er wordt via de database een controlle gedaan of de tag
        bestaat in het systeem
        
        Args:
        tag(int) -- Tag van de QR of RFID

        Returns:
        None
        '''

        # Zet database connectie op
        connection = sqlite3.connect(self.database_name)

        # Haalt en verwerkt de waarde op van welk tag bij welke persoon hoort.
        persoons_ids = connection.execute('''SELECT * FROM tags WHERE tag_id == {0}'''.format(str(tag)))
        
        # Geeft True terug als er een waarde gevonden kan worden en geeft persoons_id gelijk mee.
        for persoons_id in (persoons_ids.fetchall()):
            connection.close()
            return True, persoons_id[3]
        return False, 0

    def authorize(self, persoons_id, ruimte_id):
        '''Nadat je geauthenticeerd ben kan je geautorizeerd worden
        op basis van de ruimte waar de aanvraag vandaan komt en op
        basis van het persoons_id

        Args:
        persoons_id(int) -- ID van Persoon
        ruimte_id(int) -- ID van ruimte waar persoon toegang tot wilt.

        Returns:
        authorized(bool) -- True of False of de gebruiker geauthoriseerd is tot de ruimte
        bericht(string) -- Bericht met speciale meldingen over de authorisatie.
        '''

        connection = sqlite3.connect(self.database_name)
        toegangs = connection.execute('''SELECT * FROM toegang WHERE persoons_id = {0} AND ruimte_id = {1};'''.format(str(persoons_id), str(ruimte_id)))

        toegang = None

        for toegang in (toegangs.fetchall()):
            connection.close()
            break
        
        if toegang is None:
            return False, 'Persoon_ID {0} heeft geen toegangswaarde staan voor ruimte_id {1}'.format(str(persoons_id), str(ruimte_id))
        if not toegang:
            return False, 'Persoon_ID {0} heeft een geen geldige toegang staan voor ruimte_id {1}'.format(str(persoons_id), str(ruimte_id))
        if toegang:
            return True, 'Persoon_ID {0} heeft correct toegang voor ruimte_id {1}'.format(str(persoons_id), str(ruimte_id))
        return False, 'Onbekende fout opgetreden.'

    def logging(self, resultaat, logtext, tag_id=0, persoons_id=0, ruimte_id=0):
        '''Logging richting de database, standaard zijn de waardes op 0

        Arguments:
        tag_id(int) -- ID van de tag van de gebruiker
        persoon_id(int) -- Persoon van de tag
        ruimte_id(int) -- Ruimte waar poging tot toegang in staat
        toegang_id(int) -- ID van toegangswaarde die gebruikt is
        resultaat(int) -- Resultaat of toegang geslaagd op gefaald is.
        logtext(str) -- Tekst van de logging

        Returns:
        None
        '''

        connection = sqlite3.connect(self.database_name)
        counts = connection.execute('''SELECT COUNT (*) FROM logging''')

        count = 0

        for count in (counts.fetchall()):
            break

        logline = int(count[0]) + 1

        connection.execute('''INSERT INTO logging(logline, tag_id, persoons_id, ruimte_id, resultaat, logtext)
        VALUES ({0}, {1}, {2}, {3}, {4}, '{5}')'''.format(str(logline), str(tag_id), str(persoons_id), str(ruimte_id), str(resultaat), logtext))
        connection.commit()
        connection.close()

    def vraag_toegang(self, tag_id, ruimte_id):
        '''Ruimte andere functies aan voor het
        aanvragen van de toegang tot een ruimte.

        Args:
        tag_id(int) -- ID van de tag van de gebruiker.
        ruimte_id -- ID van ruimte waar toegang tot gevraagt wordt.

        Returns:
        result(bool) -- Resultaat of toegang aanvraag gelukt is
        bericht(str) -- Bericht van wat er fout is gegaan.
        '''

        result_authenticate = self.authenticate(tag_id)
        if not result_authenticate[0]:
            self.logging(0, 'Tag is niet bekend in het systeem', tag_id, 0, ruimte_id)
            return False
        
        result_authorise = self.authorize(result_authenticate[1], ruimte_id)
        if not result_authorise[0]:
            self.logging(0, result_authorise[1], tag_id, result_authenticate[1], ruimte_id)
            return False

        self.logging(1, 'Toegang succesvol verleend', tag_id, result_authenticate[1], ruimte_id)
        return True

    def get_logging(self):
        '''Print alle logging op het scherm

        Args:
        None

        Returns:
        None
        '''

        connection = sqlite3.connect(self.database_name)
        results = connection.execute('''SELECT * FROM LOGGING''')
        for result in results.fetchall():
            print (result)
        