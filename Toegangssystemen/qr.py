'''Dit bestand bevat de classe van de QR code
acties en dingen'''

import qrcode
import cv2
import pyzbar.pyzbar as pyzbar
from random import randint
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import base64

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
        self.cameraindex = 0

        # Variablen voor de mail configuratie
        self.smtp_server = 'smtp.office365.com'
        self.smtp_port = 587
        self.mail_sender = 'ralph.vanleeuwen@student.hu.nl'
        self.mail_username = 'ralph.vanleeuwen@student.hu.nl'
        self.mail_password = ''

    def generate_qrcode(self):
        '''Genereerd QR code op basis van meegegeven data
        en slaat deze op als een bestand.
        
        Args:
        None
        
        Returns:
        tag_id(int) -- ID die gegenereerd is en op de QR-waarde staat.
        file_name(str) -- Naam van het bestand dat weggeschreven is.
        '''
        
        # Formaat van de QR code.
        qr = qrcode.QRCode(
            version=5,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=1,
        )

        tag_id = randint(100000, 100000000)

        # Toevoegen van data aan de geformateerde QR code.
        qr.add_data(tag_id)
        qr.make(fit=True)

        # QR code omzetten naar een image.
        file_name = str(tag_id) + '.png'
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(file_name)

        return tag_id, file_name

    def scan_qrcode(self, ret_value, found_event):
        '''Scans QR code based on index of video. Let op
        deze functie blijft door draaien tot er een QR-code
        is gevonden.

        Args:
        None
        
        Returns:
        data(str) -- The reciever data'''

        cap = cv2.VideoCapture(self.cameraindex, cv2.CAP_DSHOW)

        while True:
            _, frame = cap.read()

            decodedObjects = pyzbar.decode(frame)
            for obj in decodedObjects:
                ret_value.value = int(obj.data)
                found_event.set()
                return ret_value



    def register_qrcode(self, data, voornaam, achternaam):
        '''Registeert de standaard van een gast gebruiker
        op de database zodat deze toegang kan krijgen

        data(int) -- Nummer van de QR Code dat gegenereerd is.
        voornaam(str) -- Voornaam die in de database onder persoon komt te staan.
        achternaam(str) -- Achternaam die in de database onder persoon komt te staan.

        Returns:
        persoons_id(int) -- Random gegenereerde ID'''

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
        connection.execute('''INSERT INTO toegang(toegang_id, persoons_id, ruimte_id, heeft_toegang) VALUES ({0}, {1}, {2}, {3})'''.format(str(randint(100000, 1000000)), str(persoons_id), str(5), str(1)))
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

        encoded = base64.b64encode(open(file_name, "rb").read()).decode()

        # Afbeelding deel in html verwerkt.
        html = f"""\
            <html>
            <body>
            <p> Geachte Meneer / Mevrouw,</p>
            <p></p>
            <p> Uw QR code staat klaar voor uw gezoek aan BMC</p>
            <p> Hiermee heeft u toegang om te parkeren </p>
            <img src="data:image/jpg;base64,{encoded}">
            </body>
            </html>
            """

        # Het html deel attachen aan het mailbericht
        part = MIMEText(html, "html")
        message.attach(part)

        # Het daadwerkelijk versturen van het mail bericht.
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(self.mail_username, self.mail_password)
            server.sendmail(self.mail_sender, recipient, message.as_string())
            server.quit()
            os.remove(file_name)

    def new_qr_user(self, voornaam, achternaam, recipient):
        '''Spreekt omliggende functies aan voor een nieuwe gebruiker met QR
        code te generern via de volgende stappen:
        1. Genereren van QR code. generate_qrcode()
        2. Registreren van QR code waarbij de persoon
        wordt aangemaakt. register_qrcode()
        3. Toevoegen van standaard toegang voor qr_code. qr_access()
        4. Versturen van de QR code via de mail. send_qrcode()

        Args:
        voornaam(str) -- Voornaam van gebruiker.
        achternaam(str) -- Achternaam van gebruiker.
        recipient(str) -- e-mail adress van gebruiker waar de.
        QR code ook uiteindelijk naartoe wordt gestuurd.

        Returns:
        resultaat(bool) -- True of False, Of alles goed is gegaan.
        persoons_id(int) -- uniek ID van persoon
        '''

        # Main uitvoering
        
        tag_id, file_name = self.generate_qrcode()
        persoons_id = self.register_qrcode(tag_id, voornaam, achternaam)
        self.qr_access(persoons_id)
        self.send_qrcode(file_name, recipient)
        return True, persoons_id
        