'''Dit bestand bevat de classe van de QR code
acties en dingen'''

import qrcode
import cv2
import pyzbar.pyzbar as pyzbar
from random import randint
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from PIL import Image


class qr:
    '''Classe die alle functies voor QR code acties bevat.
    '''
    def __init__(self):
        '''Intiteerd eigen object

        Args:
        None

        Returns:
        None'''

        # Variablen voor de camera configuratie
        self.database_name = 'toegangssysteem.db'
        self.cameraindex = 3

        # Variablen voor de mail configuratie
        self.smtp_server = ''
        self.smtp_port = 0
        self.mail_sender = ''
        self.mail_username = ''
        self.mail_password = ''

    def generate_qrcode(self, data):
        '''Genereerd QR code op basis van meegegeven data
        en slaat deze op als een bestand.
        
        data(str) -- Data to give to the QR code.
        
        Returns:
        file--name -- Naam waar het bestand als opgeslagen wordt.
        '''
        
        # Formaat van de QR code.
        qr = qrcode.QRCode(
            version=5,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=1,
        )

        # Toevoegen van data aan de geformateerde QR code.
        qr.add_data(data)
        qr.make(fit=True)

        # QR code omzetten naar een image.
        file_name = str(data) + '.png'
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(file_name)

        return file_name

    def scan_qrcode(self):
        '''Scans QR code based on index of video. Let op
        deze functie blijft door draaien tot er een QR-code
        is gevonden.

        Args:
        None
        
        Returns:
        None'''

        cap = cv2.VideoCapture(self.cameraindex)
        font = cv2.FONT_HERSHEY_PLAIN

        while True:
            _, frame = cap.read()

            decodedObjects = pyzbar.decode(frame)
            for obj in decodedObjects:
                return obj.data


    def register_qrcode(self, data, voornaam, achternaam):
        '''Registeert de standaard van een gast gebruiker
        op de database zodat deze toegang kan krijgen

        data(int) -- Nummer van de QR Code dat gegenereerd is.
        voornaam(str) -- Voornaam die in de database onder persoon komt te staan.
        achternaam(str) -- Achternaam die in de database onder persoon komt te staan.

        Returns:
        persoons_id(int) -- Random gegenereerde ID van persoon'''

        # Maakt verbinding met de SQL database
        connection = sqlite3.connect('toegangssysteem.db')

        # Genereerd een persoon ID random
        persoons_id = randint(100000, 1000000)

        # Voeg persoon toe aan database
        connection.execute('''INSERT INTO personen(persoons_id,voornaam,achternaam,parkeren,prioriteit_parkeren)
              VALUES({0}, '{1}', '{2}', {3}, {4})'''.format(str(persoons_id), voornaam, achternaam, str(1), str(0)))
        connection.commit()

        # Voeg tag toe aan database
        connection.execute('''INSERT INTO tags(tag_id,is_qr,is_rfid,persoons_id)VALUES({0}, {1}, {2}, {3})'''.format(str(data), str(1), str(0), str(persoons_id)))
        connection.commit()
        connection.close()
        # Voeg toegangscontrole toe aan database
        
        return persoons_id

    def qr_access(self, persoons_id):
        '''Deze functie is apart zodat je niet gelijk alles sloopt
        wanneer je alleen de permissies aanpast. Dit zijn trouwens default
        0 waardes omdat de gast geen toegang hoort te hebben tot ruimtes

        Args:
        persoons_id(int) -- id van systeem

        Returns:
        None'''

        connection = sqlite3.connect('toegangssysteem.db')
        connection.execute('''INSERT INTO toegang(toegang_id, persoons_id, ruimte_id, heeft_toegang) VALUES ({0}, {1}, {2}, {3})'''.format(str(randint(100000, 1000000)), str(persoons_id), str(1), str(0)))
        connection.execute('''INSERT INTO toegang(toegang_id, persoons_id, ruimte_id, heeft_toegang) VALUES ({0}, {1}, {2}, {3})'''.format(str(randint(100000, 1000000)), str(persoons_id), str(2), str(0)))
        connection.execute('''INSERT INTO toegang(toegang_id, persoons_id, ruimte_id, heeft_toegang) VALUES ({0}, {1}, {2}, {3})'''.format(str(randint(100000, 1000000)), str(persoons_id), str(3), str(0)))
        connection.execute('''INSERT INTO toegang(toegang_id, persoons_id, ruimte_id, heeft_toegang) VALUES ({0}, {1}, {2}, {3})'''.format(str(randint(100000, 1000000)), str(persoons_id), str(4), str(0)))
        connection.execute('''INSERT INTO toegang(toegang_id, persoons_id, ruimte_id, heeft_toegang) VALUES ({0}, {1}, {2}, {3})'''.format(str(randint(100000, 1000000)), str(persoons_id), str(5), str(0)))
        connection.commit()
        connection.close()

    def send_qrcode(self, file_name, recipient):
        '''Stuurt een mail met een QR code hierin
        deze QR code kan gebruikt worden om toegang
        te krijgen tot een de parkeerruimte'''

        # Initial message setup
        message = MIMEMultipart("alternative")
        message["Subject"] = 'Uw QR code staat klaar.'
        message["From"] = self.mail_sender
        message["To"] = recipient

        # Afbeelding deel in html verwerkt.
        html = """\
        <html>
            <body>
                <img src="cid:Mailtrapimage">
            </body>
        </html>
        """

        # Het html deel attachen aan het mailbericht
        part = MIMEText(html, "html")
        message.attach(part)

        # Bestand binnen halen van de schrijf af van de daadwerkelijke afbeelding.
        content = open(file_name, 'rb')
        image = MIMEImage(content.read())
        content.close()

        # Referentie van image linken.
        image.add_header('Content-ID', '<Mailtrapimage>')
        message.attach(image)

        # Het daadwerkelijk versturen van het mail bericht.
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.login(self.mail_username, self.mail_password)
            server.sendmail(self.mail_sender, recipient, message.as_string())

