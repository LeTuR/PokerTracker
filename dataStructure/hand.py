class Hand:
    """"It defines the action on one hand which is composed by a pre-flop
    action, a flop action, a turn action and a river action. The id is
    auto-generated with Hand initialization."""

    idCounter = 1

    def __init__(self):
        """Initialize the class with default values"""
        # Class Reference
        self.id = Hand.idCounter
        Hand.idCounter += 1
        # General Info
        self.gameId = 0
        self.date = ""
        self.blind = 0
        self.ante = 0
        self.positions = {}
        self.board = []
        # Actions
        self.actionPeflop = []
        self.actionFlop = []
        self.actionTurn = []
        self.actionRiver = []

    def __str__(self):
        printed = '<' + "Hand Id : " + str(self.id) + '>'
        return printed
