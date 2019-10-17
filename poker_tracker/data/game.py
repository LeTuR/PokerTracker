class Game:
    """ Game can represent any poker game.

        A game can represent a poker tournament a cash game for
        example.
    
        The game is composed by a set of hands. The game is reference by
        an id auto-generated during the initialization.

        Attributes :
            id (int): an auto generated unique id that make reference to
                the game.
            date (string): The date of the game mm/dd/year.
            buy_in (float): The buy to the game (only for tournaments).
            rake (int): The taxes to get into the game (included in the
                buy-in).
            prize_pool (float): The total prize pool of the game (only for tournaments).
            game_format (string): The format of the game such as Hold'em No Limit ...etc.
            number_of_players (string): The number of players in the game.
            position (int): The final position of the hero in the game (tournament only).
            earning (int): The hero earning's in the game (tournament only).
            players (dict): List of all the players played with the hero in the game.
            hands (dict): List of all the hands played by the hero in the game
    """
    idCounter = 1

    def __init__(self):
        # Class Reference
        self.id = Game.idCounter
        Game.idCounter += 1
        # General Info
        self.date = ""
        self.buy_in = 0
        self.rake = 0
        self.prize_pool = 0
        self.game_format = ""
        self.number_of_players = 0
        self.position = 0 # TODO: ???
        self.earning = 0
        self.players = {}
        self.hands = {}

    def __str__(self):
        printed = '<' + "Game ID : " + str(self.id) + '>'
        return printed
