'''Hier staat de classe in waar de RFID sensor
acties in staan'''

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

class rfid:
    '''Hierin staan de functies rondom
    de RFID scanners.'''

    def __init__(self):
        '''Intiteerd eigen object

        Args:
        None

        Returns:
        None'''

        self.database_name = 'toegangssysteem.db'

    def read_card(self, ret_value, found_event):
        '''Leest de RFID kaart uit en geeft de input terug.

        Args:
        None

        Returns:
        Data .. dit nog ff afmaken
        '''

        reader = SimpleMFRC522()
        tag, text = reader.read()

        ret_value.value = int(text)
        found_event.set()
        return ret_value
