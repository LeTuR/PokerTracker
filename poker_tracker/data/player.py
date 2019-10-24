class Player:
    """ Class Player contains player relative information

        Args:
            pseudo (string): The pseudo of the player

        Attributes:
            pseudo (string): The in-game pseudoof the player
            hands (list): The list of all the hands played by the player
            games (list): The list of all the games played by the player
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
