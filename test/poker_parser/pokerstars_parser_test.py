from poker_parser.pokerstars_parser import PokerStarsParser, Card, Value, Color, Action, ActionType, read_action


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

# def test_header_tournament_parser():
#     parser = PokerStarsParser()
#     lines = ["PokerStars Hand #202004455940: Tournament #2642898548,"
#              " €0.93+€0.07 EUR Hold'em No Limit - Level I (10/20) - "
#              "2019/07/04 21:31:39 CET [2019/07/04 15:31:39 ET]",
#              "Table '2642898548 1' 3-max Seat #1 is the button"]
#     parser.header_tournament_parser(lines)
#
#     assert parser.current_game.buy_in == 1
#     assert parser.current_game.rake == 0.07
#     assert parser.current_hand.small_blind == 10
#     assert parser.current_hand.big_blind == 20
#     assert parser.current_game.date == "2019/07/04"
#     assert parser.current_hand.date == "2019/07/04"
#     assert parser.current_hand.hour == "21:31:39"
#
#
# def test_setup_parser():
#     parser = PokerStarsParser()
#     lines = ["Table '2642898548 1' 3-max Seat #1 is the button",
#              "Seat 1: leti5795 (450 in chips)",
#              "Seat 2: onucee (550 in chips)",
#              "Seat 3: MaGiCLeTuR (500 in chips)"]
#     parser.setup_parser(lines)
#     assert parser.current_hand.dealer == 1
#     # pseudo_positions
#     assert parser.current_hand.pseudo_seats.__len__() == 3
#     assert parser.current_hand.pseudo_seats["leti5795"] == 1
#     assert parser.current_hand.pseudo_seats["onucee"] == 2
#     assert parser.current_hand.pseudo_seats["MaGiCLeTuR"] == 3
#     # positions
#     assert parser.current_hand.seats.__len__() == 3
#     assert parser.current_hand.seats[1].player.pseudo == "leti5795"
#     assert parser.current_hand.seats[1].stack == 450
#     assert parser.current_hand.seats[2].player.pseudo == "onucee"
#     assert parser.current_hand.seats[2].stack == 550
#     assert parser.current_hand.seats[3].player.pseudo == "MaGiCLeTuR"
#     assert parser.current_hand.seats[3].stack == 500
#
#
# def test_preflop_parser():
#     parser = PokerStarsParser()
#     # setup
#     # pseudo_positions
#     parser.current_hand.pseudo_seats["leti5795"] = 1
#     parser.current_hand.pseudo_seats["onucee"] = 2
#     parser.current_hand.pseudo_seats["MaGiCLeTuR"] = 3
#
#     # positions
#     parser.current_hand.seats[1] = SeatInfo(Player("leti5795"),
#                                             450,
#                                             [Card(), Card()])
#     parser.current_hand.seats[2] = SeatInfo(Player("onucee"),
#                                             550,
#                                             [Card(), Card()])
#     parser.current_hand.seats[3] = SeatInfo(Player("MaGiCLeTuR"),
#                                             500,
#                                             [Card(), Card()])
#
#     lines = ["Dealt to MaGiCLeTuR [Ad 5c]",
#              "onucee: folds",
#              "MaGiCLeTuR: raises 20 to 40",
#              "leti5795: calls 20"]
#     parser.preflop_parser(lines)
#     # check player hand
#     assert parser.current_hand.seats[3].cards[0] == Card(Value.ACE, Color.DIAMONDS)
#     assert parser.current_hand.seats[3].cards[1] == Card(Value.FIVE, Color.CLUBS)
#     # check action list
#     assert parser.current_hand.action_peflop.__len__() == 3
#     assert parser.current_hand.action_peflop[0] == Action(ActionType.FOLD, 0)
#     assert parser.current_hand.action_peflop[1] == Action(ActionType.RAISE, 40)
#     assert parser.current_hand.action_peflop[2] == Action(ActionType.CALL, 20)
#
#
# def test_flop_parser():
#     parser = PokerStarsParser()
#
#     lines = ["*** FLOP *** [Th Ac 8h]",
#              "MaGiCLeTuR: bets 24",
#              "leti5795: folds",
#              "Uncalled bet (24) returned to MaGiCLeTuR",
#              "MaGiCLeTuR collected 80 from pot",
#              "MaGiCLeTuR: doesn't show hand"]
#
#     parser.flop_parser(lines)
#     # check board_flop
#     assert parser.current_hand.board_flop.__len__() == 3
#     assert parser.current_hand.board_flop[0] == Card(Value.TEN, Color.HEARTS)
#     assert parser.current_hand.board_flop[1] == Card(Value.ACE, Color.CLUBS)
#     assert parser.current_hand.board_flop[2] == Card(Value.EIGHT, Color.HEARTS)
#     # check action list
#     assert parser.current_hand.action_flop.__len__() == 2
#     assert parser.current_hand.action_flop[0] == Action(ActionType.BET, 24)
#     assert parser.current_hand.action_flop[1] == Action(ActionType.FOLD)
#
#
# def test_turn_parser():
#     parser = PokerStarsParser()
#
#     lines = ["*** TURN *** [Ts Kc 9d] [3c]",
#              "leti5795: checks",
#              "onucee: checks"]
#
#     parser.turn_parser(lines)
#     # check board_turn
#     assert parser.current_hand.board_turn.__len__() ==  1
#     assert parser.current_hand.board_turn[0] == Card(Value.THREE, Color.CLUBS)
#     # check turn actions
#     assert parser.current_hand.action_turn.__len__() == 2
#     assert parser.current_hand.action_turn[0] == Action(ActionType.CHECK)
#     assert parser.current_hand.action_turn[1] == Action(ActionType.CHECK)
#
#
# def test_river_parser():
#     parser = PokerStarsParser()
#
#     lines = ["*** RIVER *** [Ts Kc 9d 3c] [3s]",
#              "leti5795: checks",
#              "onucee: checks"]
#
#     parser.river_parser(lines)
#     # check board_river
#     assert parser.current_hand.board_river.__len__() == 1
#     assert parser.current_hand.board_river[0] == Card(Value.THREE, Color.SPADES)
#     # check river actions
#     assert parser.current_hand.action_river.__len__() == 2
#     assert parser.current_hand.action_river[0] == Action(ActionType.CHECK)
#     assert parser.current_hand.action_river[1] == Action(ActionType.CHECK)
#
#
# def test_show_down_parser():
#     parser = PokerStarsParser()
#     # setup
#     # pseudo_positions
#     parser.current_hand.pseudo_seats["leti5795"] = 1
#     parser.current_hand.pseudo_seats["onucee"] = 2
#     parser.current_hand.pseudo_seats["MaGiCLeTuR"] = 3
#
#     # positions
#     parser.current_hand.seats[1] = SeatInfo(Player("leti5795"),
#                                             450,
#                                             [Card(), Card()])
#     parser.current_hand.seats[2] = SeatInfo(Player("onucee"),
#                                             550,
#                                             [Card(), Card()])
#     parser.current_hand.seats[3] = SeatInfo(Player("MaGiCLeTuR"),
#                                             500,
#                                             [Card(), Card()])
#
#     lines = ["*** SHOW DOWN ***",
#              "onucee: shows [7s 9d] (a pair of Eights)",
#              "MaGiCLeTuR: shows [2s Ah] (two pair, Eights and Deuces)",
#              "MaGiCLeTuR collected 120 from pot"]
#
#     parser.show_down_parser(lines)
#     assert parser.current_hand.seats[2].cards[0] == Card(Value.SEVEN, Color.SPADES)
#     assert parser.current_hand.seats[2].cards[1] == Card(Value.NINE, Color.DIAMONDS)
#     assert parser.current_hand.seats[3].cards[0] == Card(Value.TWO, Color.SPADES)
#     assert parser.current_hand.seats[3].cards[1] == Card(Value.ACE, Color.HEARTS)
#
#
# def test_hand_parser():
#     parser = PokerStarsParser()
#
#     lines = ["PokerStars Hand #202004487429: Tournament #2642898548, €0.93+€0.07 EUR Hold'em No Limit - "
#              "Level I (10/20) - 2019/07/04 21:32:32 CET [2019/07/04 15:32:32 ET]",
#              "Table '2642898548 1' 3-max Seat #3 is the button",
#              "Seat 1: leti5795 (440 in chips)",
#              "Seat 2: onucee (450 in chips)",
#              "Seat 3: MaGiCLeTuR (610 in chips)",
#              "leti5795: posts small blind 10",
#              "onucee: posts big blind 20",
#              "*** HOLE CARDS ***",
#              "Dealt to MaGiCLeTuR [Qd 2c]",
#              "MaGiCLeTuR: folds",
#              "leti5795: calls 10",
#              "onucee: checks",
#              "*** FLOP *** [Ts Kc 9d]",
#              "leti5795: checks",
#              "onucee: checks",
#              "*** TURN *** [Ts Kc 9d] [3c]",
#              "leti5795: checks",
#              "onucee: checks",
#              "*** RIVER *** [Ts Kc 9d 3c] [3s]",
#              "leti5795: checks",
#              "onucee: checks",
#              "*** SHOW DOWN ***",
#              "leti5795: shows [7d Js] (a pair of Threes)",
#              "onucee: mucks hand",
#              "leti5795 collected 40 from pot",
#              "*** SUMMARY ***",
#              "Total pot 40 | Rake 0",
#              "Board [Ts Kc 9d 3c 3s]",
#              "Seat 1: leti5795 (small blind) showed [7d Js] and won (40) with a pair of Threes",
#              "Seat 2: onucee (big blind) mucked [2d 5s]",
#              "Seat 3: MaGiCLeTuR (button) folded before Flop (didn't bet)"]
#
#     parser.hand_parser(lines)

