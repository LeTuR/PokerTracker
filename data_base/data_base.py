import sqlite3
from data.game import Game


def create_table_game():
    """
    Create a table game in the database
    :return: nothing
    """
    try:
        conn = sqlite3.connect('db_tracker.db')
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS t_game(
             d_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
             d_date TEXT,
             d_buyIn INTEGER,
             d_rake INTEGER,
             d_prizePool INTEGER,
             d_nbPlayer INTEGER,
             d_format TEXT,
             d_position INTEGER,
             d_earnings INTEGER
        )
        """)
        conn.commit()
    except sqlite3.OperationalError:
        print('Erreur la table existe déjà')
    except Exception as e:
        print("Erreur")
        conn.rollback()
        # raise e
    finally:
        conn.close()


def insert_game_to_table_game(game):
    """
    insert a game in the game table
    :param game: type class game
    :return:
    """
    try:
        conn = sqlite3.connect('db_tracker.db')
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO t_game(d_date, d_buyIn, d_rake, d_prizePool, d_nbPlayer, d_format, d_position, d_earnings)\
        ...VALUES(?,?,?,?,?,?,?,?)""",
                       (game.date,
                        game.buy_in,
                        game.rake,
                        game.prizePool,
                        game.nbPlayer,
                        game.gameFormat,
                        game.position,
                        game.earning))
        conn.commit()
    except sqlite3.OperationalError:
        print('Erreur fail to insert')
    except Exception as e:
        print("Erreur")
        conn.rollback()
        # raise e
    finally:
        conn.close()


def delete_table_game():
    """
    delete table t_game
    :return:
    """
    try:
        conn = sqlite3.connect('db_tracker')
        cursor = conn.cursor()
        cursor.execute("""
        DROP TABLE t_game
        """)
        conn.commit()
    except sqlite3.OperationalError:
        print('Erreur delete impossible')
    except Exception as e:
        print("Erreur")
        conn.rollback()
        # raise e
    finally:
        conn.close()


def print_table_game():
    """
    affiche la table game id and date
    :return: nothing
    """
    try:
        conn = sqlite3.connect('db_tracker.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT d_date, d_buyIn, d_id FROM t_game""")
        res = cursor.fetchone()
        print(res)
    except sqlite3.OperationalError:
        print('Erreur print impossible')
    except Exception as e:
        print("Erreur")
        # raise e


game_test = Game()
game_test.date = "08/07/2019 22:50:25"
game_test.buy_in = 23
game_test.rake = 2
game_test.prizePool = 50
game_test.nbPlayer = 3
game_test.gameFormat = "Hold'em No Limit"
game_test.position = 1
game_test.earning = 50


create_table_game()
insert_game_to_table_game(game_test)
print_table_game()
#delete_table_game()
