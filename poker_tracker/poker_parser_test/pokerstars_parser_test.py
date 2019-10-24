import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "hand"
hand_test_file = os.path.join(script_dir, rel_path)

from poker_tracker.data.card import Card, Value, Color
from poker_tracker.data.action import Action, ActionType
from poker_tracker.data.hand import Hand
from poker_tracker.poker_parser.pokerstars_parser import PokerStarsParser, read_action

def test_parse_header_and_setup():
    parser = PokerStarsParser(" ")

    line = "PokerStars Hand #202004455940: Tournament #2642898548, €0.93+€0.07 EUR Hold'em No Limit " \
           "- Level I (10/20) - 2019/07/04 21:31:39 CET [2019/07/04 15:31:39 ET] \n" \
           "Table '2642898548 1' 3-max Seat #1 is the button\n" \
           "Seat 1: leti5795 (500 in chips)\n" \
           "Seat 2: onucee (500 in chips)\n" \
           "Seat 3: MaGiCLeTuR (500 in chips)\n" \
           "onucee: posts small blind 10\n" \
           "MaGiCLeTuR: posts big blind 20\n"

    parser.part_dict['HEADER'] = line
    parser.parse_header()
    # Main Header
    assert parser.hand_id == 202004455940
    assert parser.game_id == 2642898548
    assert parser.buy_in == 1
    assert parser.small_blind == 10
    assert parser.big_blind == 20
    # Table Info
    assert parser.table_name == "2642898548 1"
    assert parser.table_size == 3
    assert parser.button_seat == 1

    parser.parse_setup()
    assert parser.positions["BTN"] == "leti5795"
    assert parser.positions["SB"] == "onucee"
    assert parser.positions["BB"] == "MaGiCLeTuR"
    assert parser.stacks["BTN"] == 500
    assert parser.stacks["SB"] == 500
    assert parser.stacks["BB"] == 500
    assert parser.players["leti5795"] == "BTN"
    assert parser.players["onucee"] == "SB"


def test_read_action():
    line = "leti5795: calls 20"

    pseudo, action_type, amount = read_action(line)

    assert pseudo == "leti5795"
    assert action_type == ActionType.CALL
    assert amount == 20

    line = "MaGiCLeTuR: checks"

    pseudo, action_type, amount = read_action(line)

    assert pseudo == "MaGiCLeTuR"
    assert action_type == ActionType.CHECK
    assert amount == 0


    line = "MaGiCLeTuR: raises 20 to 40"

    pseudo, action_type, amount = read_action(line)

    assert pseudo == "MaGiCLeTuR"
    assert action_type == ActionType.RAISE
    assert amount == 40


def test_parse_preflop():
    # TODO: create a fixture for the initialization
    parser = PokerStarsParser("")

    line = "Dealt to MaGiCLeTuR [2s Ah]\n" \
           "leti5795: calls 20\n" \
           "onucee: calls 10\n" \
           "MaGiCLeTuR: checks"
    
    parser.hand_id = 202004455940
    parser.game_id = 2642898548
    parser.buy_in = 1
    parser.small_blind = 10
    parser.big_blind = 20
    parser.positions["BTN"] = "leti5795"
    parser.positions["SB"] = "onucee"
    parser.positions["BB"] = "MaGiCLeTuR"
    parser.stacks["BTN"] = 500
    parser.stacks["SB"] = 500
    parser.stacks["BB"] = 500
    parser.players["leti5795"] = "BTN"
    parser.players["onucee"] = "SB"
    parser.players["MaGiCLeTuR"] = "BB"

    parser.part_dict['HOLE CARDS'] = line

    parser.parse_preflop()

    assert parser.cards["BB"][0] == Card(Value.TWO, Color.SPADES)
    assert parser.cards["BB"][1] == Card(Value.ACE, Color.HEARTS)

    assert parser.action_preflop.__len__() == 3
    assert parser.action_preflop[0] == Action("BTN", ActionType.CALL, 20)
    assert parser.action_preflop[1] == Action("SB", ActionType.CALL, 10)
    assert parser.action_preflop[2] == Action("BB", ActionType.CHECK, 0)


def test_parse_flop():
    parser = PokerStarsParser("")

    line = " [Th Ac 8h]\n"\
           "leti5795: calls 20\n" \
           "onucee: calls 10\n" \
           "MaGiCLeTuR: checks"

    parser.hand_id = 202004455940
    parser.game_id = 2642898548
    parser.buy_in = 1
    parser.small_blind = 10
    parser.big_blind = 20
    parser.positions["BTN"] = "leti5795"
    parser.positions["SB"] = "onucee"
    parser.positions["BB"] = "MaGiCLeTuR"
    parser.stacks["BTN"] = 500
    parser.stacks["SB"] = 500
    parser.stacks["BB"] = 500
    parser.players["leti5795"] = "BTN"
    parser.players["onucee"] = "SB"
    parser.players["MaGiCLeTuR"] = "BB"

    parser.part_dict['FLOP'] = line

    parser.parse_flop()

    assert parser.board_flop.__len__() == 3
    assert parser.board_flop[0] == Card(Value.TEN, Color.HEARTS)
    assert parser.board_flop[1] == Card(Value.ACE, Color.CLUBS)
    assert parser.board_flop[2] == Card(Value.EIGHT, Color.HEARTS)

    assert parser.action_flop.__len__() == 3
    assert parser.action_flop[0] == Action("BTN", ActionType.CALL, 20)
    assert parser.action_flop[1] == Action("SB", ActionType.CALL, 10)
    assert parser.action_flop[2] == Action("BB", ActionType.CHECK, 0)


def test_parse_turn():
    parser = PokerStarsParser("")

    line = "[5s 8c Tc] [Th]\n" \
           "leti5795: calls 20\n" \
           "onucee: calls 10\n" \
           "MaGiCLeTuR: checks"

    parser.hand_id = 202004455940
    parser.game_id = 2642898548
    parser.buy_in = 1
    parser.small_blind = 10
    parser.big_blind = 20
    parser.positions["BTN"] = "leti5795"
    parser.positions["SB"] = "onucee"
    parser.positions["BB"] = "MaGiCLeTuR"
    parser.stacks["BTN"] = 500
    parser.stacks["SB"] = 500
    parser.stacks["BB"] = 500
    parser.players["leti5795"] = "BTN"
    parser.players["onucee"] = "SB"
    parser.players["MaGiCLeTuR"] = "BB"
    
    parser.part_dict['TURN'] = line

    parser.parse_turn()

    assert parser.board_turn.__len__() == 1
    assert parser.board_turn[0] == Card(Value.TEN, Color.HEARTS)

    assert parser.action_turn.__len__() == 3
    assert parser.action_turn[0] == Action("BTN", ActionType.CALL, 20)
    assert parser.action_turn[1] == Action("SB", ActionType.CALL, 10)
    assert parser.action_turn[2] == Action("BB", ActionType.CHECK, 0)


def test_parse_river():
    parser = PokerStarsParser("")

    line = "[5s 8c Tc 2h] [Th]\n" \
           "leti5795: calls 20\n" \
           "onucee: calls 10\n" \
           "MaGiCLeTuR: checks"

    parser.hand_id = 202004455940
    parser.game_id = 2642898548
    parser.buy_in = 1
    parser.small_blind = 10
    parser.big_blind = 20
    parser.positions["BTN"] = "leti5795"
    parser.positions["SB"] = "onucee"
    parser.positions["BB"] = "MaGiCLeTuR"
    parser.stacks["BTN"] = 500
    parser.stacks["SB"] = 500
    parser.stacks["BB"] = 500
    parser.players["leti5795"] = "BTN"
    parser.players["onucee"] = "SB"
    parser.players["MaGiCLeTuR"] = "BB"

    parser.part_dict['RIVER'] = line

    parser.parse_river()

    assert parser.board_river.__len__() == 1
    assert parser.board_river[0] == Card(Value.TEN, Color.HEARTS)

    assert parser.action_river.__len__() == 3
    assert parser.action_river[0] == Action("BTN", ActionType.CALL, 20)
    assert parser.action_river[1] == Action("SB", ActionType.CALL, 10)
    assert parser.action_river[2] == Action("BB", ActionType.CHECK, 0)


def test_parse_showdown():
    parser = PokerStarsParser("")

    line = "onucee: shows [7s 9d] (a pair of Eights)\n"\
           "MaGiCLeTuR: shows [2s Ah] (two pair, Eights and Deuces)\n"\
           "MaGiCLeTuR collected 120 from pot"

    parser.hand_id = 202004455940
    parser.game_id = 2642898548
    parser.buy_in = 1
    parser.small_blind = 10
    parser.big_blind = 20
    parser.positions["BTN"] = "leti5795"
    parser.positions["SB"] = "onucee"
    parser.positions["BB"] = "MaGiCLeTuR"
    parser.stacks["BTN"] = 500
    parser.stacks["SB"] = 500
    parser.stacks["BB"] = 500
    parser.players["leti5795"] = "BTN"
    parser.players["onucee"] = "SB"
    parser.players["MaGiCLeTuR"] = "BB"

    parser.part_dict['SHOW DOWN'] = line

    parser.parse_showdown()
    assert parser.cards["SB"].__len__() == 2

    assert parser.cards["SB"][0] == Card(Value.SEVEN, Color.SPADES)
    assert parser.cards["SB"][1] == Card(Value.NINE, Color.DIAMONDS)

    assert parser.cards["BB"].__len__() == 2
    assert parser.cards["BB"][0] == Card(Value.TWO, Color.SPADES)
    assert parser.cards["BB"][1] == Card(Value.ACE, Color.HEARTS)


def test_parse_hand():
    file = open(hand_test_file, encoding='UTF-8')
    line = file.read()
    parser = PokerStarsParser(line)
    parser.parse_hand()

    # Main Header
    assert parser.hand_id == 202004455940
    assert parser.game_id == 2642898548
    assert parser.buy_in == 1
    assert parser.small_blind == 10
    assert parser.big_blind == 20
    # Table Info
    assert parser.table_name == "2642898548 1"
    assert parser.table_size == 3
    assert parser.button_seat == 1

    # Hand global info
    assert parser.positions["BTN"] == "leti5795"
    assert parser.positions["SB"] == "onucee"
    assert parser.positions["BB"] == "MaGiCLeTuR"
    assert parser.stacks["BTN"] == 500
    assert parser.stacks["SB"] == 500
    assert parser.stacks["BB"] == 500
    assert parser.players["leti5795"] == "BTN"
    assert parser.players["onucee"] == "SB"

    # Hero hand
    assert parser.cards["BB"][0] == Card(Value.TWO, Color.SPADES)
    assert parser.cards["BB"][1] == Card(Value.ACE, Color.HEARTS)

    # preflop actions
    assert parser.action_preflop.__len__() == 3
    assert parser.action_preflop[0] == Action("BTN", ActionType.CALL, 20)
    assert parser.action_preflop[1] == Action("SB", ActionType.CALL, 10)
    assert parser.action_preflop[2] == Action("BB", ActionType.CHECK, 0)

    # Flop
    assert parser.board_flop.__len__() == 3
    assert parser.board_flop[0] == Card(Value.FIVE, Color.SPADES)
    assert parser.board_flop[1] == Card(Value.EIGHT, Color.CLUBS)
    assert parser.board_flop[2] == Card(Value.TEN, Color.CLUBS)

    assert parser.action_flop.__len__() == 3
    assert parser.action_flop[0] == Action("SB", ActionType.CHECK, 0)
    assert parser.action_flop[1] == Action("BB", ActionType.CHECK, 0)
    assert parser.action_flop[2] == Action("BTN", ActionType.CHECK, 0)


    # Turn
    assert parser.board_turn.__len__() == 1
    assert parser.board_turn[0] == Card(Value.TWO, Color.HEARTS)

    assert parser.action_turn.__len__() == 4
    assert parser.action_turn[0] == Action("SB", ActionType.CHECK, 0)
    assert parser.action_turn[1] == Action("BB", ActionType.BET, 30)
    assert parser.action_turn[2] == Action("BTN", ActionType.FOLD, 0)
    assert parser.action_turn[3] == Action("SB", ActionType.CALL, 30)


    # River
    assert parser.board_river.__len__() == 1
    assert parser.board_river[0] == Card(Value.EIGHT, Color.DIAMONDS)

    assert parser.action_river.__len__() == 2
    assert parser.action_river[0] == Action("SB", ActionType.CHECK, 0)
    assert parser.action_river[1] == Action("BB", ActionType.CHECK, 0)

    # Showdown
    assert parser.cards["SB"].__len__() == 2
    assert parser.cards["SB"][0] == Card(Value.SEVEN, Color.SPADES)
    assert parser.cards["SB"][1] == Card(Value.NINE, Color.DIAMONDS)

    assert parser.cards["BB"].__len__() == 2
    assert parser.cards["BB"][0] == Card(Value.TWO, Color.SPADES)
    assert parser.cards["BB"][1] == Card(Value.ACE, Color.HEARTS)

    file.close()


def test_load_hand():
    file = open(hand_test_file, encoding='UTF-8')
    line = file.read()
    parser = PokerStarsParser(line)
    parser.parse_hand()
    hand = parser.load()

    # Game and Hand ID
    assert hand.id == parser.hand_id
    assert hand.game_id == parser.game_id
    
    # General Information
    assert hand.date == parser.date
    assert hand.hour == parser.hour
    assert hand.dealer == parser.positions['BTN']
    assert hand.small_blind == parser.small_blind
    assert hand.big_blind == parser.big_blind
    assert hand.ante == parser.ante

    # Game init
    assert hand.seats['BTN'].player == "leti5795"
    assert hand.seats['BTN'].stack == 500
    assert hand.seats['BTN'].cards[0] == Card()
    assert hand.seats['BTN'].cards[1] == Card()

    assert hand.seats['SB'].player == "onucee"
    assert hand.seats['SB'].stack == 500
    assert hand.seats['SB'].cards[0] == Card(Value.SEVEN, Color.SPADES)
    assert hand.seats['SB'].cards[1] == Card(Value.NINE, Color.DIAMONDS)

    assert hand.seats['BB'].player == "MaGiCLeTuR"
    assert hand.seats['BB'].stack == 500
    assert hand.seats['BB'].cards[0] == Card(Value.TWO, Color.SPADES)
    assert hand.seats['BB'].cards[1] == Card(Value.ACE, Color.HEARTS)

    # Board Flop
    assert hand.board_flop[0] == parser.board_flop[0]
    assert hand.board_flop[1] == parser.board_flop[1]
    assert hand.board_flop[2] == parser.board_flop[2]

    # Board Turn
    assert hand.board_turn[0] == parser.board_turn[0]

    # Board River
    assert hand.board_river[0] == parser.board_river[0]

    # Action Preflop
    for i in range(0, hand.action_preflop.__len__()):
        assert hand.action_preflop[i] == parser.action_preflop[i]

    # Action Flop
    for i in range(0, hand.action_flop.__len__()):
        assert hand.action_flop[i] == parser.action_flop[i]
    
    # Action Turn
    for i in range(0, hand.action_turn.__len__()):
        assert hand.action_turn[i] == parser.action_turn[i]
    
    # Action River
    for i in range(0, hand.action_river.__len__()):
        assert hand.action_river[i] == parser.action_river[i]
    
    file.close()
