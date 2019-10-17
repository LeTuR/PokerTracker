class SeatInfo:
    """ This class contains the main info of the current seat.
        
        The main information are :
        - The Player
        - The Player Stack
        - The Player Cards
    """

    def __init__(self, player=None, stack=0, cards=None):
        self.player = player
        self.stack = stack
        self.cards = cards


class Hand:
    """ It defines the action on for one hand.
    
        The hand is composed by a pre-flop action, a flop action, a turn action
        and a river action. The id is auto-generated with Hand initialization.

        Attributes :
            id (int): The id is unique for each hand. It can be used as a
                reference to the hand.
            game_id (int): The game_id is a reference to the game where the
                hand was played.
            hero (string): The pseudo of the main player in the hand.
            date (string): The month/day/year when the hand was played.
            hour (string): The time when the hand was played XX:XX:XX
            dealer (string): The position of the dealer
            small_blind(float): The small blind value.
            big_blind (float): The big blind value.
            ante (float): The ante value.
            pseudo_seats (dict): associate each player's pseudo with a seat
            seats (dict): associate each seat with a player's pseudo
            board_flop (list): list of the cards (use of the class Card) at 
                the flop.
            board_turn (list): list of the cards (use of the class Card) at 
                the turn.
            board_river (list): list of the cards (use of the class Card) at 
                the river.
            action_preflop (list): ordered list of all the action in the
                the preflop part of the hand.
                The first action in the list is the first action that happened
                in the game.
            action_flop (list): ordered list of all the action in the
                the flop part of the hand.
                The first action in the list is the first action that happened
                in the game.
            action_turn (list): ordered list of all the action in the
                the turn part of the hand.
                The first action in the list is the first action that happened
                in the game.
            action_river (list): ordered list of all the action in the
                the river part of the hand.
                The first action in the list is the first action that happened
                in the game.
    """

    idCounter = 1

    def __init__(self):
        # Class Reference
        self.id = Hand.idCounter
        Hand.idCounter += 1
        # General Info
        self.game_id = 0
        # set the actual player perspective
        self.hero = ""
        self.date = ""
        self.hour = ""
        self.dealer = ""
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
        self.action_preflop = []
        self.action_flop = []
        self.action_turn = []
        self.action_river = []

    def __str__(self):
        printed = '<' + "Hand Id : " + str(self.id) + '>'
        return printed
