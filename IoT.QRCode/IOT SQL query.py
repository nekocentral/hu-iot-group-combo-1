import sqlite3

def create_persoon():
    """
    Create a new project into the projects table
    :param conn:
    :param persoon:
    :return: persoon_id:
    """

    conn = sqlite3.connect('toegangssysteem.db')

    sql1 = ''' INSERT INTO personen(persoons_id,voornaam,achternaam,parkeren,prioriteit_parkeren,fietsenstalling,ruimte1,ruimte2)
              VALUES(0096545,'Piet','Puk',1,0,1,1,0) '''
    sql2 = ''' INSERT INTO personen(persoons_id,voornaam,achternaam,parkeren,prioriteit_parkeren,fietsenstalling,ruimte1,ruimte2)
              VALUES(0065442,'Sven','Visser',1,1,1,1,1) '''
    sql3 = ''' INSERT INTO personen(persoons_id,voornaam,achternaam,parkeren,prioriteit_parkeren,fietsenstalling,ruimte1,ruimte2)
              VALUES(0084885,'Ralph','van Leeuwen',0,0,0,0,0) '''
    conn.execute(sql1)
    conn.execute(sql2)
    conn.execute(sql3)
    conn.commit()


def create_tag():
    """
    Create a new task
    :param conn:
    :param tags:
    :return:
    """
    conn = sqlite3.connect('toegangssysteem.db')

    sql1 = ''' INSERT INTO tags(tag_id,is_qr,is_rfid,persoons_id)
              VALUES(4444,0,1,0096545) '''
    sql2 = ''' INSERT INTO tags(tag_id,is_qr,is_rfid,persoons_id)
              VALUES(5555,1,0,0065442) '''
    sql3 = ''' INSERT INTO tags(tag_id,is_qr,is_rfid,persoons_id)
              VALUES(6666,1,1,0084885) '''
    conn.execute(sql1)
    conn.execute(sql2)
    conn.execute(sql3)
    conn.commit()

create_persoon()
create_tag()