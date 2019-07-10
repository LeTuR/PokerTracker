class Game:
    """Game can represent a poker tournament a cash game or
    any poker type of game, which is composed by a set of
    hands. The game id is auto-generated during the initialization."""

    idCounter = 1

    def __init__(self):
        """Initialized the Game class with
        default values"""
        # Class Reference
        self.id = Game.idCounter
        Game.idCounter += 1
        # General Info
        self.date = ""
        self.buyIn = 0
        self.prizePool = 0
        self.gameFormat = ""
        self.players = []
        self.hands = []

    def __str__(self):
        printed = '<' + "Game ID : " + str(self.id) + '>'
        return printed
