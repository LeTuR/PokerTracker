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

conn = sqlite3.connect('my_data_base')

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS t_game(
    d_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    d_date TEXT
    d_buyIn INTEGER
    d_rake INTEGER
    d_prizePool INTEGER
    d_format TEXT
    d_position INTEGER
    d_nbPlayer INTEGER
    d_earnings INTEGER
)
""")
conn.commit()


cursor.execute("""
INSERT INTO tournament(d_date, d_buyIn, d_prizePool, d_format, d_place, d_nbPlayer, d_earnings) VALUES(?, ?)""", ("olivier", 30))

