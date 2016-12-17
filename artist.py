import psycopg2 as dbapi2
from flask import request

from dsn_conf import get_dsn

dsn = get_dsn()

def insert_artist(artist):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement= """INSERT INTO ARTIST(NAME,PICTUREID) VALUES(%s,%s)"""
            cursor.execute(statement,(artist.name,artist.pictureid))
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def delete_artist(DELETEID):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""DELETE FROM ARTIST WHERE ID = %s""", (int(DELETEID),))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def update_artist(UPDATEID,newname):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""UPDATE ARTIST SET NAME = '%s' WHERE ID = %d""" % (newname,int(UPDATEID)))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def select_all_artist():
    content =[]
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""SELECT ARTIST.ID, ARTIST.NAME, PICTURE.FILEPATH
                       FROM ARTIST INNER JOIN PICTURE ON ARTIST.PICTUREID = PICTURE.ID
                       ORDER BY ARTIST.NAME""")
            connection.commit()
            content = list(cursor)
            return content
        except dbapi2.DatabaseError as e:
            connection.rollback()
