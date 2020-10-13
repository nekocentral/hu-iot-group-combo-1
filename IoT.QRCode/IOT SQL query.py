def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(toegangssyteem.db)
    except Error as e:
        print(e)
    return conn

def create_persoon(conn, persoon):
    """
    Create a new project into the projects table
    :param conn:
    :param persoon:
    :return: persoon_id:
    """
    sql = ''' INSERT INTO personen(persoons_id,voornaam,achternaam,parkeren,prioriteit_parkeren,fietsenstalling,ruimte1,ruimte2)
              VALUES(0096545,Piet,Puk,1,0,1,1,0) '''
    sql = ''' INSERT INTO personen(persoons_id,voornaam,achternaam,parkeren,prioriteit_parkeren,fietsenstalling,ruimte1,ruimte2)
              VALUES(0065442,Sven,Visser,1,1,1,1,1) '''
    sql = ''' INSERT INTO personen(persoons_id,voornaam,achternaam,parkeren,prioriteit_parkeren,fietsenstalling,ruimte1,ruimte2)
              VALUES(0054885,Ralph,van Leeuwen,0,0,0,0,0) '''
    cur = conn.cursor()
    cur.execute(sql, personen)
    conn.commit()
    return cur.lastrowid

def create_tag(conn, tags):
    """
    Create a new task
    :param conn:
    :param tags:
    :return:
    """

    sql = ''' INSERT INTO tasks(tag_id,is_qr,is_rfid_id,persoons_id)
              VALUES(4444,0,1,0096545) '''
    sql = ''' INSERT INTO tasks(tag_id,is_qr,is_rfid_id,persoons_id)
              VALUES(5555,1,0,0065442) '''
    sql = ''' INSERT INTO tasks(tag_id,is_qr,is_rfid_id,persoons_id)
              VALUES(6666,1,1,0084885) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid