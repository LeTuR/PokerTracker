import sqlite3
from data.game import Game

game_test = Game()
game_test.date = "08/07/2019 22:50:25"
game_test.buy_in = 23
game_test.rake = 2
game_test.prizePool = 50
game_test.nbPlayer = 3
game_test.gameFormat = "Hold'em No Limit"
game_test.position = 1
game_test.earning = 50


def create_table_game():
    """
    Create a table game in the database
    :return: nothing
    """
    try:
        conn = sqlite3.connect('db_tracker')
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS t_game(
            d_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            d_date TEXT
            d_buyIn INTEGER
            d_rake INTEGER
            d_prizePool INTEGER
            d_nbPlayer INTEGER
            d_format TEXT
            d_position INTEGER
            d_earnings INTEGER
        )
        """)
        conn.commit()
    except sqlite3.OperationalError:
        print('Erreur la table existe déjà')
    except:
        print("Erreur")
        conn.rollback()
        # raise e
    finally:
        conn.close()


def insert_game_to_table_game():
    """

    :return:
    """
    try:
        conn = sqlite3.connect('db_tracker')
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO t_game(d_date, d_buyIn, d_rake, d_prizePool, d_nbPlayer, d_format, d_position, d_earnings)\
        ...VALUES(?,?,?,?,?,?,?,?)""",
                       (game_test.date,
                        game_test.buy_in,
                        game_test.rake,
                        game_test.prizePool,
                        game_test.nbPlayer,
                        game_test.gameFormat,
                        game_test.position,
                        game_test.earning))

        cursor.commit()
    except sqlite3.OperationalError:
        print('Erreur fail to insert')
    except Exception as e:
        print("Erreur")
        conn.rollback()
        # raise e
    finally:
        conn.close()
