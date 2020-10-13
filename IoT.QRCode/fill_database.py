import sqlite3
from random import randint

def new_person(voornaam, achternaam, parkeren, prioriteit_parkeren):
    '''Maakt nieuw persoon aan in de database

    Args:
    voornaam(str) -- Voornaam van persoon
    achternaam(str) -- Achternaam van de persoon
    parkeren(int) -- 1 of 0 of hij mag parkeren
    prioriteit_parkeren(int) -- 1 of 0 of hij mag prioriteit parkeren

    Returns:
    persoons_id(int) -- Random int, ID van persoon
    '''

    connection = sqlite3.connect('toegangssysteem.db')
    persoons_id = randint(100000, 1000000)

    connection.execute('''INSERT INTO personen(persoons_id,voornaam,achternaam,parkeren,prioriteit_parkeren)
              VALUES({0}, '{1}', '{2}', {3}, {4})'''.format(str(persoons_id), voornaam, achternaam, str(parkeren), str(prioriteit_parkeren)))

    connection.commit()
    connection.close()

    return persoons_id

def new_tag(tag_id, is_qr, is_rfid, persoons_id):
    '''Maakt nieuw persoon aan in de database

    Args:
    tag_id(int) -- Meegegven waarde
    is_qr(int) -- 1 of 0 of het een qr is
    is_rfid(int) -- 1 of 0 of het een rfid is
    persoons_id(int) -- Random int, ID van persoon

    Returns:
    None
    '''

    connection = sqlite3.connect('toegangssysteem.db')
    connection.execute('''INSERT INTO tags(tag_id,is_qr,is_rfid,persoons_id)VALUES({0}, {1}, {2}, {3})'''.format(str(tag_id), str(is_qr), str(is_rfid), str(persoons_id)))
    connection.commit()
    connection.close()

def new_ruimte(ruimte_id, ruimte_naam):
    '''Maakt nieuwe ruimte aan en zet deze in database

    Args:
    ruimte_id(int) -- Nummerige int van ruimte
    ruimte_naam(str) -- Naam van ruimte

    Returns:
    None
    '''

    connection = sqlite3.connect('toegangssysteem.db')
    connection.execute('''INSERT INTO ruimtes(ruimte_id, ruimte_naam) VALUES({0}, '{1}')'''.format(str(ruimte_id), ruimte_naam))
    connection.commit()
    connection.close()

def new_toegang(persoons_id, ruimte_id, heeft_toegang):
    '''Voegt nieuwe toegang toe aan bestaande gebruiker

    Args:
    persoons_id(int) -- Random int, ID van persoon
    ruimte_id(int) -- Nummerige int van ruimte
    heeft_toegang(int) -- 1 of 0 of de gebruiker toegang heeft

    Returns:
    None
    '''

    toegang_id = randint(100000, 1000000)

    connection = sqlite3.connect('toegangssysteem.db')
    connection.execute('''INSERT INTO toegang(toegang_id, persoons_id, ruimte_id, heeft_toegang) VALUES ({0}, {1}, {2}, {3})'''.format(str(toegang_id), str(persoons_id), str(ruimte_id), str(heeft_toegang)))
    connection.commit()
    connection.close()
