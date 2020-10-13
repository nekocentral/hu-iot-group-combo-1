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
            return True, persoons_id
        return False, 0

    def authorize(self, persoons_id, ruimte_id):
        '''Nadat je geauthenticeerd ben kan je geautorizeerd worden
        op basis van de ruimte waar de aanvraag vandaan komt en op
        basis van het persoonsid

