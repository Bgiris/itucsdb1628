import psycopg2 as dbapi2
from dao.post import *
from dao.user import *
from dao.comment import *
from dao.song import *
from dao.genre import *
from dao.artist import *
from dao.album import *
from dao import messages as Messages
import datetime
from song import *
from genre import insert_genre
from artist import *
from album import *
from dao.userdetails import *

from dsn_conf import get_dsn

dsn = get_dsn()

def drop_suggestion_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS SUGGESTION"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()


def create_suggestion_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement =     """CREATE TABLE IF NOT EXISTS SUGGESTION(
            ID SERIAL PRIMARY KEY,
            USERID INTEGER NOT NULL REFERENCES USERDATA(ID) ON DELETE CASCADE,
            ARTIST VARCHAR(50) NOT NULL,
            SONGNAME VARCHAR(50) NOT NULL,
            SUGGESTIONDATE DATE,
            RELEASEDATE DATE,
            STATU INT
            CHECK (STATU > -1 AND STATU < 3)
            )"""
            cursor.execute(statement)
            statement = """INSERT INTO SUGGESTION(USERID,ARTIST,SONGNAME,SUGGESTIONDATE,RELEASEDATE,STATU)
                            VALUES(%s,%s,%s,%s,%s,%s)"""
            cursor.execute(statement,(1,"Metallica","Nothing else matters",'1.10.2016','1.10.2016',2));
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()


def drop_like_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS LIKES"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def create_like_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement =     """CREATE TABLE IF NOT EXISTS LIKES(
            ID SERIAL PRIMARY KEY,
            POSTID INTEGER NOT NULL REFERENCES POST(ID) ON DELETE CASCADE,
            USERID INTEGER NOT NULL REFERENCES USERDATA(ID) ON DELETE CASCADE,
            LIKEDATE TIMESTAMP
            )"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def drop_post_table():
     with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS POST"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError:
            connection.rollback()

def create_post_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """CREATE TABLE IF NOT EXISTS POST(
            ID SERIAL PRIMARY KEY,
            CONTENT VARCHAR(100) NOT NULL,
            POSTDATE TIMESTAMP,
            USERID INTEGER NOT NULL REFERENCES USERDATA(ID) ON DELETE CASCADE,
            SONGID INTEGER NOT NULL REFERENCES SONG(ID) ON DELETE CASCADE,
            LIKECOUNTER INT DEFAULT 0
            )"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def create_album_cover_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS ALBUMCOVER"""
            cursor.execute(statement);
            statement = """CREATE TABLE IF NOT EXISTS ALBUMCOVER(
                ID SERIAL PRIMARY KEY,
                FILEPATH VARCHAR(100) NOT NULL
                )"""
            cursor.execute(statement)
            statement = """INSERT INTO ALBUMCOVER (FILEPATH)
                             VALUES ('/static/images/beatles.jpg')"""
            cursor.execute(statement)
            statement = """INSERT INTO ALBUMCOVER (FILEPATH)
                             VALUES ('/static/images/ledzeplin.jpg')"""
            cursor.execute(statement)
            statement = """INSERT INTO ALBUMCOVER (FILEPATH)
                             VALUES ('/static/images/metallica.jpg')"""
            cursor.execute(statement)
            statement = """INSERT INTO ALBUMCOVER (FILEPATH)
                             VALUES ('/static/images/pinkfloyd.jpg')"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()



def insert_post(post):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement= """INSERT INTO POST(CONTENT,POSTDATE,USERID,SONGID,ALBUMCOVERID) VALUES(%s,%s,%s,%s,%s)"""
            cursor.execute(statement,(post.content,post.postdate,post.userid,post.songid,post.albumcoverid))
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()


''' ***************************************IMPORTANT CREATION OF USER MUST BE ON TOP ******************************'''
def drop_user_table():
     with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS USERDATA"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError:
            connection.rollback()

def create_user_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """CREATE TABLE IF NOT EXISTS USERDATA(
            ID SERIAL PRIMARY KEY,
            USERNAME  VARCHAR(50) UNIQUE NOT NULL,
            PASSWORD VARCHAR(20) NOT NULL
            )"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError:
            connection.rollback()



def insert_user(user):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement= """INSERT INTO USERDATA(USERNAME,PASSWORD) VALUES(%s,%s)"""
            cursor.execute(statement,(user.username,user.password))
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

'''******************************************************************************************************************'''



def create_avatar_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS AVATAR"""
            cursor.execute(statement);
            statement = """CREATE TABLE IF NOT EXISTS AVATAR(
                ID SERIAL PRIMARY KEY,
                FILEPATH VARCHAR(100) NOT NULL
                )"""
            cursor.execute(statement)
            statement = """INSERT INTO AVATAR (FILEPATH)
                             VALUES ('/static/images/avatar.jpg')"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def drop_comment_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS COMMENT"""
            cursor.execute(statement);
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def create_comment_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """CREATE TABLE IF NOT EXISTS COMMENT(
            ID SERIAL PRIMARY KEY,
            COMMENT VARCHAR(150) NOT NULL,
            USERID INTEGER NOT NULL REFERENCES USERDATA(ID) ON DELETE CASCADE,
            POSTID INTEGER NOT NULL REFERENCES POST(ID) ON DELETE CASCADE,
            AVATARID INTEGER NOT NULL REFERENCES AVATAR(ID) ON DELETE CASCADE,
            ALBUMCOVERID INTEGER NOT NULL REFERENCES PICTURE(ID) ON DELETE CASCADE,
            CDATE TIMESTAMP
            )"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError:
            connection.rollback()


def insert_comment(comment):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """INSERT INTO COMMENT(COMMENT,USERID,POSTID,AVATARID,ALBUMCOVERID,CDATE) VALUES(%s,%s,%s,%s,%s,%s)"""
            cursor.execute(statement,(comment.content,comment.userid,comment.postid,comment.cdate))
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def create_share_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement =     """CREATE TABLE IF NOT EXISTS SHARE(
            ID SERIAL PRIMARY KEY,
            POSTID INTEGER NOT NULL REFERENCES POST(ID) ON DELETE CASCADE,
            REPOSTERID INTEGER NOT NULL REFERENCES USERDATA(ID) ON DELETE CASCADE,
            SHAREDATE TIMESTAMP
            )"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def drop_share_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS SHARE"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()
'''****************************************************************************************************************************************************'''
def drop_messages_table():
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                    """DROP TABLE IF EXISTS message_room CASCADE;
                    DROP TABLE IF EXISTS message CASCADE;
                    DROP TABLE IF EXISTS message_participant;
                    DROP TABLE IF EXISTS message_status;
                    DROP TABLE IF EXISTS message_room_admins;
                    DROP TABLE IF EXISTS message_room_event; """)

def create_messages_table():
    """ Drops(if exits) and Creates all tables for Messages """
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    CREATE TABLE
                      message_room (
                       id             SERIAL    PRIMARY KEY,
                       room_name      TEXT      NULL,
                       admin_id       INTEGER   NOT NULL   REFERENCES USERDATA(ID) ON DELETE SET NULL,
                       activity_date  TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
                      );

                    CREATE TABLE
                      message (
                        id            SERIAL    PRIMARY KEY,
                        note          TEXT      NOT NULL,
                        message_date  TIMESTAMP NOT NULL   DEFAULT CURRENT_TIMESTAMP,
                        room_id       INTEGER   NOT NULL   REFERENCES message_room(id) ON DELETE CASCADE,
                        sender_id     INTEGER   NOT NULL   REFERENCES USERDATA(ID) ON DELETE CASCADE
                      );

                    CREATE TABLE
                      message_participant (
                        room_id       INTEGER   NOT NULL   REFERENCES message_room(id) ON DELETE CASCADE,
                        user_id       INTEGER   NOT NULL   REFERENCES USERDATA(ID) ON DELETE CASCADE,
                        join_date     TIMESTAMP NOT NULL   DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (room_id, user_id)
                      );

                    CREATE TABLE
                      message_status (
                        message_id    INTEGER   NOT NULL   REFERENCES message(id) ON DELETE CASCADE,
                        receiver_id   INTEGER   NOT NULL   REFERENCES USERDATA(ID) ON DELETE CASCADE,
                        PRIMARY KEY (message_id, receiver_id)
                      );

                    CREATE TABLE
                      message_room_event (
                        id            SERIAL    PRIMARY KEY,
                        room_id       INTEGER   NOT NULL   REFERENCES message_room(id) ON DELETE CASCADE,
                        user_id       INTEGER   NOT NULL   REFERENCES USERDATA(ID) ON DELETE CASCADE,
                        event_date    TIMESTAMP NOT NULL   DEFAULT CURRENT_TIMESTAMP,
                        action_id     INTEGER   NOT NULL
                      ); """
            )


def insert_bulk_messages():
    room1 = Messages.Room(name="roomName1", admin=1, participants=[1, 2, 3])
    room1.create()
    room2 = Messages.Room(name="roomName2", admin=2, participants=[2, 3])
    room2.create()
    room3 = Messages.Room(name="roomName3", admin=1, participants=[1, 3])
    room3.create()

    room1.send_message("Hello Room1!")
    room2.send_message("Hello Room2!")
    room2.send_message("Hello Room2 2!")
    room3.send_message("Hello Room3!")

#####################################BERKAY#####################################
#song table
def create_song_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS SONG"""
            cursor.execute(statement);
            statement = """CREATE TABLE IF NOT EXISTS SONG(
            ID SERIAL PRIMARY KEY,
            NAME VARCHAR(50) NOT NULL,
            ARTIST INTEGER REFERENCES ARTIST(ID) ON DELETE CASCADE,
            ALBUM INTEGER REFERENCES ALBUM(ID) ON DELETE CASCADE,
            GENRE INTEGER REFERENCES GENRE(ID) ON DELETE SET NULL,
            FILEPATH VARCHAR(200) UNIQUE NOT NULL
            )"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError:
            connection.rollback()

def drop_song_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS SONG"""
            cursor.execute(statement);
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def create_genre_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS GENRE"""
            cursor.execute(statement);
            statement = """CREATE TABLE IF NOT EXISTS GENRE(
            ID SERIAL PRIMARY KEY,
            NAME VARCHAR(20) UNIQUE NOT NULL
            )"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError:
            connection.rollback()

def drop_genre_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS GENRE"""
            cursor.execute(statement);
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def create_artist_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS ARTIST"""
            cursor.execute(statement);
            statement = """CREATE TABLE IF NOT EXISTS ARTIST(
            ID SERIAL PRIMARY KEY,
            PICTUREID INTEGER REFERENCES PICTURE(ID) ON DELETE SET NULL,
            NAME VARCHAR(64) UNIQUE NOT NULL
            )"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError:
            connection.rollback()

def drop_artist_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS ARTIST"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError:
            connection.rollback()


def insert_default_genres():
    insert_genre(Genre("Rock"))
    insert_genre(Genre("Pop"))
    insert_genre(Genre("Classic"))
    insert_genre(Genre("Jazz"))
    insert_genre(Genre("Hip-hop"))
    insert_genre(Genre("Electronic"))

def create_pic_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS PICTURE"""
            cursor.execute(statement);
            statement = """CREATE TABLE IF NOT EXISTS PICTURE(
                ID SERIAL PRIMARY KEY,
                TYPE INTEGER NOT NULL,
                FILEPATH VARCHAR(200) NOT NULL
                )"""
            cursor.execute(statement)
            statement = """INSERT INTO PICTURE (FILEPATH,TYPE)
                             VALUES ('/static/images/avatar.jpg',1)"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

#####################################BERKAY#####################################
'''****************************************userdetails ******************************************************************'''
def drop_userdetails_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS USERDETAILS"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()




def create_userdetails_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """CREATE TABLE IF NOT EXISTS USERDETAILS(
            ID SERIAL PRIMARY KEY,
            USERID INTEGER NOT NULL REFERENCES USERDATA(ID) ON DELETE CASCADE,
            NAME  VARCHAR(50),
            SURNAME VARCHAR(50),
            EMAIL VARCHAR(50),
            PHONENUMBER VARCHAR(15)
            )"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError:
            connection.rollback()



def insert_userdetails(userdetails):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement= """INSERT INTO USERDETAILS(USERID,NAME,SURNAME,EMAIL,PHONENUMBER) VALUES(%s,%s,%s,%s,%s)"""
            cursor.execute(statement,(userdetails.userid,userdetails.name,userdetails.surname,userdetails.email,userdetails.phonenumber))
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

'''*************************************************************************************************************************'''
## create album-table ##
def create_album_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """CREATE TABLE IF NOT EXISTS ALBUM(
            ID SERIAL PRIMARY KEY,
            NAME VARCHAR(40) NOT NULL,
            ALBUMDATE INTEGER,
            ALBUMCOVERID INTEGER NOT NULL REFERENCES PICTURE(ID)
            ) """
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError:
            connection.rollback()
## create album table ##

## drop album-table ##

def drop_album_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS ALBUM"""
            cursor.execute(statement);
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()


## drop album-table ##

## album-table ##


def reset_database():

    drop_suggestion_table()
    drop_userdetails_table()
    drop_share_table()
    drop_like_table()
    drop_comment_table()
    drop_post_table()
    drop_song_table()   # CHECK DROP ORDER
    drop_artist_table()
    drop_genre_table()
    drop_album_table() #####
    drop_messages_table()
    drop_user_table()







def insert_sample_data():
    create_user_table()
    firstuser = User(1,"admin","admin")
    insert_user(firstuser)
    seconduser = User(2,"user1", "password1")
    insert_user(seconduser)
    thirduser = User(3,"kagan95", "123")
    insert_user(thirduser)
    fourthuser = User(4,"listnto", "9999")
    insert_user(fourthuser)
    create_userdetails_table()
    userdetails = Userdetails(1,"berkay","g","berkay@listnto.com","+90212xxxxxx")
    insert_userdetails(userdetails)
    user2details = Userdetails(2,"kagan","ozgun","kagan@listnto.com","+90212xxxxxx")
    insert_userdetails(user2details)
    create_suggestion_table()
    create_album_cover_table()
    create_avatar_table()
    create_pic_table()
    create_album_table()
    create_genre_table()
    create_artist_table()
    create_song_table()
    create_post_table()
    create_like_table()
    create_share_table()
    create_comment_table()
    firstPost = Post("perfect!", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1, 1, 1)
    insert_post(firstPost)
    create_messages_table()
    # insert_bulk_messages()

    insert_default_genres()
    insert_sample_artists()
    insert_sample_albums()
    insert_sample_songs()

