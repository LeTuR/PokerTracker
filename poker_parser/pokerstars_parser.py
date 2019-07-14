from data.game import Game
from data.hand import Hand, SeatInfo, ActionType, Action
from data.player import Player
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
    """This function is a transcoder from PokerStars
    cards value representation to the data card value's representation.
    If an unknown character is given, and UNDEFINED value is
    return"""
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


def define_action(char):
    """Take a PokerStars file action as an entry and
    return an ActionType from hand.py"""
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


class PokerStarsParser:

    def __init__(self):
        # TODO: some problems may come with current_Game id. A special reset must be implemented
        self.current_game = Game()
        self.current_hand = Hand()

    def header_tournament_parser(self, lines):
        """Parse a tournament header hand history file which gives the current
        blinds, the buy-in the date and hour of the hand"""
        line = lines[0].split(" ")
        self.current_game.buy_in = float(line[5].split("+")[0][1:]) + float(line[5].split("+")[1][1:])
        self.current_game.rake = float(line[5].split("+")[1][1:])
        blinds = line[13].split("/")
        # TODO: Check if the ante is set with the SB and BB here
        self.current_hand.small_blind = int(blinds[0][1:])
        self.current_hand.big_blind = int(blinds[1][:-1])
        self.current_hand.date = line[15]
        self.current_game.date = line[15]
        self.current_hand.hour = line[16]

    def setup_parser(self, lines):
        """Find the button position and all the player at the table with
        their associated stack"""
        line = lines[0].split(" ")
        flag = 0
        for word in line:
            if flag == 1:
                button_position = int(word[1:])
                self.current_hand.dealer = button_position
                break
            if word == "Seat":
                flag = 1
        i = 1
        line = lines[i].split(" ")
        while line[0] == "Seat":
            new_player = Player(line[2])
            new_player_seat = int(line[1][:-1])
            new_player_stack = int(line[3][1:])
            self.current_hand.pseudo_seats[new_player.pseudo] = new_player_seat
            self.current_hand.seats[new_player_seat] = SeatInfo(new_player,
                                                                new_player_stack,
                                                                [Card(), Card()])
            i += 1
            if i < len(lines):
                line = lines[i].split(" ")
            else:
                break

    def preflop_parser(self, lines):
        """Read the preflop actions. Set the hand's main player (which is
        the perspective). Set the main player hand. Read the preflop actions
          and check if the hand is over preflop"""
        hand = lines[0].split(" ")[3:5]
        # read first card
        first_card_value = define_card_value(hand[0][1])
        first_card_color = define_card_color(hand[0][2])
        first_card = Card(first_card_value, first_card_color)
        # read second card
        second_card_value = define_card_value(hand[1][0])
        second_card_color = define_card_color(hand[1][1])
        second_card = Card(second_card_value, second_card_color)
        # read who's player perspective the hand is
        player = lines[0].split(" ")[2]
        position = self.current_hand.pseudo_seats[player]
        self.current_hand.seats[position].cards = [first_card, second_card]

        for line in lines[1:]:
            words = line.split(" ")
            if words[0] == "Uncalled":
                break
            elif words[1] == "raises":
                action_type = define_action(words[1])
                amount = float(words[4])
                action = Action(action_type, amount)
            elif words[1] == "bets" or words[1] == "calls":
                action_type = define_action(words[1])
                amount = float(words[2])
                action = Action(action_type, amount)
            else:
                action_type = define_action(words[1])
                action = Action(action_type)
            self.current_hand.action_peflop.append(action)

    def flop_parser(self, lines):
        """Read the flop cards and the flop action. Check if the hand
        is over"""
        flop = lines[0].split(" ")[3:]
        # read the first card
        first_card_value = define_card_value(flop[0][1])
        first_card_color = define_card_color(flop[0][2])
        first_card = Card(first_card_value, first_card_color)
        # read the second card
        second_card_value = define_card_value(flop[1][0])
        second_card_color = define_card_color(flop[1][1])
        second_card = Card(second_card_value, second_card_color)
        # read the third card
        third_card_value = define_card_value(flop[2][0])
        third_card_color = define_card_color(flop[2][1])
        third_card = Card(third_card_value, third_card_color)
        self.current_hand.board_flop = [first_card,
                                        second_card,
                                        third_card]
        for line in lines[1:]:
            words = line.split(" ")
            if words[0] == "Uncalled":
                break
            elif words[1] == "raises":
                action_type = define_action(words[1])
                amount = float(words[4])
                action = Action(action_type, amount)
            elif words[1] == "bets" or words[1] == "calls":
                action_type = define_action(words[1])
                amount = float(words[2])
                action = Action(action_type, amount)
            else:
                action_type = define_action(words[1])
                action = Action(action_type)
            self.current_hand.action_flop.append(action)

    def turn_parser(self, lines):
        """Read the turn card and the turn action. Check if the hand
        is over"""
        turn = lines[0].split(" ")[6]
        # read turn card
        turn_card_value = define_card_value(turn[1])
        turn_card_color = define_card_color(turn[2])
        turn_card = Card(turn_card_value, turn_card_color)
        self.current_hand.board_turn.append(turn_card)
        for line in lines[1:]:
            words = line.split(" ")
            if words[0] == "Uncalled":
                break
            elif words[1] == "raises":
                action_type = define_action(words[1])
                amount = float(words[4])
                action = Action(action_type, amount)
            elif words[1] == "bets" or words[1] == "calls":
                action_type = define_action(words[1])
                amount = float(words[2])
                action = Action(action_type, amount)
            else:
                action_type = define_action(words[1])
                action = Action(action_type)
            self.current_hand.action_turn.append(action)

    def river_parser(self, lines):
        """Read the river card and the river action. Check if the hand
        is over"""
        river = lines[0].split(" ")[7]
        river_card_value = define_card_value(river[1])
        river_card_color = define_card_color(river[2])
        river_card = Card(river_card_value, river_card_color)
        self.current_hand.board_river.append(river_card)
        for line in lines[1:]:
            words = line.split(" ")
            if words[0] == "Uncalled":
                break
            elif words[1] == "raises":
                action_type = define_action(words[1])
                amount = float(words[4])
                action = Action(action_type, amount)
            elif words[1] == "bets" or words[1] == "calls":
                action_type = define_action(words[1])
                amount = float(words[2])
                action = Action(action_type, amount)
            else:
                action_type = define_action(words[1])
                action = Action(action_type)
            self.current_hand.action_river.append(action)

    def show_down_parser(self, lines):
        """Read the show down cards. All the cards shown are recorded to
        the SeatInfo."""
        for line in lines:
            words = line.split(" ")
            if words[1] == "shows":
                player_pseudo = words[0][:-1]
                player_first_card_value = define_card_value(words[2][1])
                player_first_card_color = define_card_color(words[2][2])
                player_first_card = Card(player_first_card_value,
                                         player_first_card_color)
                player_second_card_value = define_card_value(words[3][0])
                player_second_card_color = define_card_color(words[3][1])
                player_second_card = Card(player_second_card_value,
                                          player_second_card_color)
                player_seat = self.current_hand.pseudo_seats[player_pseudo]
                self.current_hand.seats[player_seat].cards = [player_first_card,
                                                              player_second_card]

    def hand_parser(self, lines):
        """This methods reads a hand and redefine the self.current_hand
        with the new hand"""
        # TODO: optimisation are possible by removing useless lines copy

        # reset current_hand
        self.current_hand = Hand()

        # read header
        # TODO: add a selection for the header
        self.header_tournament_parser(lines[0])

        line_counter = 0
        flop_flag = False
        flag_turn = False
        flag_river = False
        flag_show_down = False

        # find the setup
        setup_lines = []
        for line in lines[1:]:
            if line == "*** HOLE CARDS ***":
                break
            setup_lines.append(line)
            line_counter += 1
        self.setup_parser(setup_lines)

        # read preflop and check for an eventual flop
        preflop_lines = []
        for line in lines[1+line_counter+1:]:
            if line.split(" ")[0] == "***":
                if line.split(" ")[1] == "FLOP":
                    flop_flag = True
                break
            else:
                preflop_lines.append(line)
                line_counter += 1
        self.preflop_parser(preflop_lines)

        # read eventual flop and check for an eventual turn
        if flop_flag:
            flop_lines = []
            for line in lines[1+line_counter:]:
                if line.split(" ")[0] == "***":
                    if line.split(" ")[1] == "TURN":
                        flag_turn = True
                    break
                else:
                    flop_lines.append(lines)
                    line_counter += 1
            self.flop_parser(flop_lines)

        if flag_turn:
            turn_lines = []
            for line in lines[1+line_counter:]:
                if line.split(" ")[0] == "***":
                    if line.split(" ")[1] == "RIVER":
                        flag_river = True
                    break
                else:
                    turn_lines.append(lines)
                    line_counter += 1
            self.turn_parser(turn_lines)

        if flag_river:
            river_lines = []
            for line in lines[1+line_counter:]:
                if line.split(" ")[0] == "***":
                    if line.split(" ")[1] == "SHOW":
                        flag_show_down = True
                    break
                else:
                    river_lines.append(lines)
                    line_counter += 1
            self.river_parser(river_lines)

        if flag_show_down:
            show_down_lines = []
            for line in lines[1+line_counter+1:]:
                if line.split(" ")[1] == "SUMMARY":
                    break
                else:
                    show_down_lines.append(lines)
                    line_counter += 1
            self.show_down_parser(show_down_lines)
