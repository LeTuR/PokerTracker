class Hand:
    """"Primitive Class Hand : It defines the action on one hand
    which is composed by a pre-flop action, a flop action, a turn
    action and a river action"""

    def __init__(self):
        """Initialize the class with default values"""
        """Class Reference Id"""
        self.id = 0
        """General Info"""
        self.gameId = 0
        self.date = ""
        self.blind = 0
        self.ante = 0
        self.positions = {}
        self.board = []
        """Actions"""
        self.actionPeflop = []
        self.actionFlop = []
        self.actionTurn = []
        self.actionRiver = []