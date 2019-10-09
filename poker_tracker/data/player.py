class Player:
    """
    Class Player contains player relative information
    """
    def __init__(self, pseudo):
        """
        Initialize the Player class
        with default values
        """
        # Class Reference
        self.pseudo = pseudo
        # General Info
        self.hands = []
        self.games = []

    def __str__(self):
        printed = '<' + self.pseudo + '>'
        return printed
