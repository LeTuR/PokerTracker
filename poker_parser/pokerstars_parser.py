import re
import logging
from data.action import ActionType, Action
from data.card import Card, Value, Color


def define_card_color(char):
    """This function is a transcoder from PokerStars
    cards color's representation to the data card color's representation.
    If an unknown character is given, and UNDEFINED color is
    return"""
    if char == 's':
        return Color.SPADES
    elif char == 'c':
        return Color.CLUBS
    elif char == 'd':
        return Color.DIAMONDS
    elif char == 'h':
        return Color.HEARTS
    else:
        return Color.UNDEFINED


def define_card_value(char):
    """
    This function is a transcoder from PokerStars
    cards value representation to the data card value's representation.
    If an unknown character is given, and UNDEFINED value is
    return

    :param char: the PokerStars character to represent the value of a card
    :return: Return the card Value
    """
    if char == '2':
        return Value.TWO
    elif char == '3':
        return Value.THREE
    elif char == '4':
        return Value.FOUR
    elif char == '5':
        return Value.FIVE
    elif char == '6':
        return Value.SIX
    elif char == '7':
        return Value.SEVEN
    elif char == '8':
        return Value.EIGHT
    elif char == '9':
        return Value.NINE
    elif char == 'T':
        return Value.TEN
    elif char == 'J':
        return Value.JACK
    elif char == 'Q':
        return Value.QUEEN
    elif char == 'K':
        return Value.KING
    elif char == 'A':
        return Value.ACE
    else:
        return Value.UNDEFINED


def define_card(card):
    """
    Returns the cards as a Card

    :param card: card string in PokerStars format
    :return: the card as a Card
    """
    try:
        value = define_card_value(card[0])
        color = define_card_color(card[1])
        return Card(value, color)
    except AttributeError:
        pass


def define_action(char):
    """
    Take a PokerStars file action as an entry and
    return an ActionType from hand.py

    :param char: PokerStars action as entry
    :return: ActionType from hand.py
    """
    if char == "checks":
        return ActionType.CHECK
    elif char == "folds":
        return ActionType.FOLD
    elif char == "bets":
        return ActionType.BET
    elif char == "raises":
        return ActionType.RAISE
    elif char == "calls":
        return ActionType.CALL
    else:
        return ActionType.UNDEFINED


def read_action(line):
    """
    Read and return an action from PokerStars file

    :param line: an action line
    :return: a Player Pseudo and an Action [pseudo, action_type, amount]
    """
    try:
        reg_action = re.search(r'(.+): ([a-z]+)', line)
        player_pseudo = reg_action.group(1)
        action_type = define_action(reg_action.group(2))
        if action_type == ActionType.CHECK:
            return [player_pseudo, action_type, 0]
        elif action_type == ActionType.FOLD:
            return [player_pseudo, action_type, 0]
        elif action_type == ActionType.CALL:
            amount = float(re.search(' €?([0-9-.]+)', line).group(1))
            return [player_pseudo, action_type, amount]
        elif action_type == ActionType.BET:
            amount = float(re.search(' €?([0-9-.]+)', line).group(1))
            return [player_pseudo, action_type, amount]
        elif action_type == ActionType.RAISE:
            amount = float(re.search('to €?([0-9-.]+)', line).group(1))
            return [player_pseudo, action_type, amount]
        else:
            return [None, None, None]

    except AttributeError:
        pass



class PokerStarsParser:
    """
    Parser PokerStars
    """

    position_name_list = [
        ["BTN", "BB"],
        ["BTN", "SB", "BB"],
        ["BTN", "SB", "BB", "CO"],
        ["BTN", "SB", "BB", "UTG", "CO"],
        ["BTN", "SB", "BB", "UTG", "MP1", "CO"],
        ["BTN", "SB", "BB", "UTG", "MP1", "MP2", "CO"],
        ["BTN", "SB", "BB", "UTG", "MP1", "MP2", "MP3", "CO"],
        ["BTN", "SB", "BB", "UTG", "UTG+1", "MP1", "MP2", "MP3", "CO"],
        ["BTN", "SB", "BB", "UTG", "UTG+1", "UTG+2", "MP1", "MP2", "MP3", "CO"],
    ]

    def __init__(self, hand_file):
        """
        Parse a hand given in argument.

        :param hand_file: the hand to parse (basically a string)
        """
        self.hand_file = hand_file

        # header info
        self.hand_id = 0      # Hand id
        self.game_id = 0      # Tournament id (this id do not exist for cash game)
        self.game_mode = ""   # Game mode (ex: Hold'em No Limit)
        self.buy_in = 0       # Buy-in
        self.rake = 0         # Rake
        self.small_blind = 0  # Small blind
        self.big_blind = 0    # Big blind
        self.ante = 0         # Ante
        self.date = ""        # Date
        self.hour = ""        # hour

        # Set up info
        self.table_name = ""     # Table name
        self.table_size = ""     # Table size
        self.players_number = 0  # Indicate the number of players at the table
        self.button_seat = 0     # Indicate the seat with the button

        # Players info :
        self.cards = {}      # key: position_name         | value: cards of the player
        self.stacks = {}     # key: position_name         | value: initial stack of the player
        self.players = {}    # key: pseudo of the players | value: position_name
        self.positions = {}  # key: position_name         | value: pseudo of the players

        # Actions :
        self.action_preflop = []  # Action pre-flop
        self.action_flop = []     # Action on the flop
        self.action_turn = []     # Action on the turn
        self.action_river = []    # Action on the river

        # Board :
        self.board_flop = []   # Cards on the flop
        self.board_turn = []   # Cards on the turn
        self.board_river = []  # Cards on the river

        # utility
        self.part_dict = {}   # key: part name | value: line with action sequence and extra info (board, card dealt)

        # log manager
        self.logger = logging.getLogger()
        self.formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

    def parse_part(self):
        """
        Not all hands have the name number of parts, it return a dict with the part name as key and content as value

        :return: Return a dict of the different division of the hand history
        """
        parts = []
        for part in re.split(r'\*\*\* ([A-Z- ]+) \*\*\*', self.hand_file):  # return [ 'part1', 'splitter1', 'part2',..
            parts.append(part)

        for i in range(0, len(parts)):
            if i == 0:
                self.part_dict['HEADER'] = parts[i]
            if i % 2 != 0:  # number is odd
                self.part_dict[parts[i]] = parts[i + 1]


    def parse_header(self):
        """
        Parse the header.

        :return: Extract the base information on the hand context.
        """
        players_number = 0
        try:
            lines = self.part_dict['HEADER'].split('\n')
            for line in lines:

                # parse first part of the header : PokerStars basic info
                if line[0:5] == "Poker":
                    # find hand id
                    reg_hand_id = re.search(r'Hand #([0-9-]+):', line)
                    self.hand_id = int(reg_hand_id.group(1))
                    # find tournament id
                    try:
                        reg_game_id = re.search(r'Tournament #([0-9]+),', line)
                        self.game_id = int(reg_game_id.group(1))
                    except AttributeError:
                        pass
                    # find blind
                    reg_blind = re.search(r'\(€?([0-9-.]+)/€?([0-9-.]+)( EUR)?\)', line)
                    self.small_blind = float(reg_blind.group(1))
                    self.big_blind = float(reg_blind.group(2))
                    # find buy in
                    try:
                        reg_buy_in = re.search(r'€?([0-9-.]+)\+€?([0-9-.]+)( EUR)?', line)
                        self.buy_in = float(reg_buy_in.group(1)) + float(reg_buy_in.group(2))
                        self.rake = float(reg_buy_in.group(2))
                    except AttributeError:
                        pass

                # parse second part of the header : Table info
                elif line[0:5] == "Table":
                    # find table name
                    reg_table_name = re.search(r'Table \'([0-9A-Za-z ]+)\'', line)
                    self.table_name = reg_table_name.group(1)
                    # find table size
                    try:
                        reg_table_size = re.search(r'([0-9]+)-max', line)
                        self.table_size = int(reg_table_size.group(1))
                    except AttributeError:
                        pass
                    # find button position
                    reg_button_position = re.search(r'Seat #([0-9]+)', line)
                    self.button_seat = int(reg_button_position.group(1))

                # count the number of players in the game
                elif line[0:4] == "Seat":
                    players_number += 1
                    self.players_number = players_number
        except AttributeError:
            # TODO: Add a better log manager
            self.logger.warning("There is no HEADER in the current file.")
            pass

    def parse_setup(self):
        """
        Parse the setup part which set the players pseudo, position and stack

        :return: The players pseudo, position and stack
        """
        lines = self.part_dict['HEADER'].split('\n')
        for line in lines:
            if line[0:4] == "Seat":
                reg_player = re.search(r'(.): (.+) \(€?([0-9-.]+)', line)
                player_seat = int(reg_player.group(1))
                player_name = reg_player.group(2)
                player_stack = float(reg_player.group(3))
                position = self.position(player_seat)
                self.positions[position] = player_name
                self.players[player_name] = position
                self.stacks[position] = player_stack

    def position(self, seat):
        """
        Define the position of the player according to the seat and the
        button position. The number of players must be set before using this
        method.

        :param seat: The player seat
        :return: It returns the player position from position_name_list
        """
        index = seat - self.button_seat
        return PokerStarsParser.position_name_list[self.players_number-2][index]

    def parse_preflop(self):
        """
        Define the hero cards, and the preflop actions

        :return: The player and and the actions
        """
        # TODO: refactor preflop, flop, turn and river in order to have one function only
        try:
            lines = self.part_dict['HOLE CARDS'].split('\n')
            for line in lines:
                if line[0:5] == "Dealt":
                    try:
                        reg_hero_hand = re.search(r'Dealt to (.+) \[(.+)\]', line)
                        hand = reg_hero_hand.group(2).split(' ')
                        # set the cards of the player
                        self.cards[self.players[reg_hero_hand.group(1)]] = [define_card(hand[0]), define_card(hand[1])]
                    except AttributeError:
                        pass
                if line[0:8] == "Uncalled":
                    # TODO: add a better Uncalled manager
                    break
                elif line == '':
                    pass
                else:
                    try:
                        pseudo, action_type, amount = read_action(line)
                        self.action_preflop.append(Action(self.players[pseudo], action_type, amount))
                    except TypeError:
                        pass
        except AttributeError:
            pass

    def parse_flop(self):
        try:
            lines = self.part_dict['FLOP'].split('\n')
            for i in range(0, len(lines)):
                if i == 0:
                    try:
                        reg_board = re.search(r'\[(.+)\]', lines[i])
                        board = reg_board.group(1).split(' ')
                        for card in board:
                            self.board_flop.append(define_card(card))
                    except AttributeError:
                        pass
                elif lines[i][0:8] == "Uncalled":
                    # TODO: add a better Uncalled manager
                    break
                elif lines[i] == '':
                    pass
                else:
                    try:
                        pseudo, action_type, amount = read_action(lines[i])
                        self.action_flop.append(Action(self.players[pseudo], action_type, amount))
                    except AttributeError:
                        pass
        except AttributeError:
            pass

    def parse_turn(self):
        try:
            lines = self.part_dict['TURN'].split('\n')
            for i in range(0, len(lines)):
                if i == 0:
                    try:
                        reg_board = re.search(r'\[(.+)\] \[(.+)\]', lines[i])
                        board = reg_board.group(2).split(' ')
                        for card in board:
                            self.board_turn.append(define_card(card))
                    except AttributeError:
                        pass
                elif lines[i][0:8] == "Uncalled":
                    # TODO: add a better Uncalled manager
                    break
                elif lines[i] == '':
                    pass
                else:
                    try:
                        pseudo, action_type, amount = read_action(lines[i])
                        self.action_turn.append(Action(self.players[pseudo], action_type, amount))
                    except AttributeError:
                        pass
        except AttributeError:
            pass

    def parse_river(self):
        try:
            lines = self.part_dict['RIVER'].split('\n')
            for i in range(0, len(lines)):
                if i == 0:
                    try:
                        reg_board = re.search(r'\[(.+)\] \[(.+)\]', lines[i])
                        board = reg_board.group(2).split(' ')
                        for card in board:
                            self.board_river.append(define_card(card))
                    except AttributeError:
                        pass
                elif lines[i][0:8] == "Uncalled":
                    # TODO: add a better Uncalled manager
                    break
                elif lines[i] == '':
                    pass
                else:
                    try:
                        pseudo, action_type, amount = read_action(lines[i])
                        self.action_river.append(Action(self.players[pseudo], action_type, amount))
                    except AttributeError:
                        pass
        except AttributeError:
            pass

    def parse_showdown(self):
        try:
            lines = self.part_dict['SHOW DOWN'].split('\n')
            for line in lines:
                try:
                    reg_show = re.search(r'(.+): shows \[(.+)\]', line)
                    player = reg_show.group(1)
                    hand = reg_show.group(2).split(' ')
                    cards = []
                    for card in hand:
                        cards.append(define_card(card))
                    try:
                        if self.cards[self.players[player]].__len__() > len(cards):
                            self.cards[self.players[player]] = cards
                    except KeyError:
                        self.cards[self.players[player]] = cards
                except AttributeError:
                    pass
        except AttributeError:
            pass

    def parse_hand(self):
        """
        Parse all the hand

        :return:
        """
        self.parse_part()
        self.parse_header()
        self.parse_setup()
        self.parse_preflop()
        self.parse_flop()
        self.parse_turn()
        self.parse_river()
        self.parse_showdown()

