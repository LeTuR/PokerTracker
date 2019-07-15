class SeatInfo:
    """
    This class contains the main info of the current seat:
        - The Player
        - The Player Stack
        - The Player Cards
    """

    def __init__(self, player=None, stack=0, cards=None):
        self.player = player
        self.stack = stack
        self.cards = cards


class Hand:
    """"
    It defines the action on one hand which is composed by a pre-flop
    action, a flop action, a turn action and a river action. The id is
    auto-generated with Hand initialization.
    """

    idCounter = 1

    def __init__(self):
        """
        Initialize the class with default values
        """
        # Class Reference
        self.id = Hand.idCounter
        Hand.idCounter += 1
        # General Info
        self.game_id = 0
        # set the actual player perspective
        self.player_pseudo = ""
        self.date = ""
        self.hour = ""
        self.dealer = 0
        self.small_blind = 0
        self.big_blind = 0
        self.ante = 0
        # TODO: check if dict of named tuple is possible here
        self.pseudo_seats = {}
        self.seats = {}
        self.board_flop = []
        self.board_turn = []
        self.board_river = []
        # Actions
        self.action_peflop = []
        self.action_flop = []
        self.action_turn = []
        self.action_river = []

    def __str__(self):
        printed = '<' + "Hand Id : " + str(self.id) + '>'
        return printed
