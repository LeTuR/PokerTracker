from poker_parser.poker_stars_parser import PokerStarsParser
from data.hand import SeatInfo, Action, ActionType
from data.player import Player
from data.card import Color, Value, Card


def test_header_tournament_parser():
    parser = PokerStarsParser()
    lines = ["PokerStars Hand #202004455940: Tournament #2642898548,"
             " €0.93+€0.07 EUR Hold'em No Limit - Level I (10/20) - "
             "2019/07/04 21:31:39 CET [2019/07/04 15:31:39 ET]",
             "Table '2642898548 1' 3-max Seat #1 is the button"]
    parser.header_tournament_parser(lines)

    assert parser.current_game.buy_in == 1
    assert parser.current_game.rake == 0.07
    assert parser.current_hand.small_blind == 10
    assert parser.current_hand.big_blind == 20
    assert parser.current_game.date == "2019/07/04"
    assert parser.current_hand.date == "2019/07/04"
    assert parser.current_hand.hour == "21:31:39"


def test_setup_parser():
    parser = PokerStarsParser()
    lines = ["Table '2642898548 1' 3-max Seat #1 is the button",
             "Seat 1: leti5795 (450 in chips)",
             "Seat 2: onucee (550 in chips)",
             "Seat 3: MaGiCLeTuR (500 in chips)"]
    parser.setup_parser(lines)
    assert parser.current_hand.dealer == 1
    # pseudo_positions
    assert parser.current_hand.pseudo_seats.__len__() == 3
    assert parser.current_hand.pseudo_seats["leti5795"] == 1
    assert parser.current_hand.pseudo_seats["onucee"] == 2
    assert parser.current_hand.pseudo_seats["MaGiCLeTuR"] == 3
    # positions
    assert parser.current_hand.seats.__len__() == 3
    assert parser.current_hand.seats[1].player.pseudo == "leti5795"
    assert parser.current_hand.seats[1].stack == 450
    assert parser.current_hand.seats[2].player.pseudo == "onucee"
    assert parser.current_hand.seats[2].stack == 550
    assert parser.current_hand.seats[3].player.pseudo == "MaGiCLeTuR"
    assert parser.current_hand.seats[3].stack == 500


def test_preflop_parser():
    parser = PokerStarsParser()
    # setup
    # pseudo_positions
    parser.current_hand.pseudo_seats["leti5795"] = 1
    parser.current_hand.pseudo_seats["onucee"] = 2
    parser.current_hand.pseudo_seats["MaGiCLeTuR"] = 3

    # positions
    parser.current_hand.seats[1] = SeatInfo(Player("leti5795"),
                                            450,
                                            [Card(), Card()])
    parser.current_hand.seats[2] = SeatInfo(Player("onucee"),
                                            550,
                                            [Card(), Card()])
    parser.current_hand.seats[3] = SeatInfo(Player("MaGiCLeTuR"),
                                            500,
                                            [Card(), Card()])

    lines = ["Dealt to MaGiCLeTuR [Ad 5c]",
             "onucee: folds",
             "MaGiCLeTuR: raises 20 to 40",
             "leti5795: calls 20"]
    parser.preflop_parser(lines)
    # check player hand
    assert parser.current_hand.seats[3].cards[0] == Card(Value.ACE, Color.DIAMONDS)
    assert parser.current_hand.seats[3].cards[1] == Card(Value.FIVE, Color.CLUBS)
    # check action list
    assert parser.current_hand.action_peflop.__len__() == 3
    assert parser.current_hand.action_peflop[0] == Action(ActionType.FOLD, 0)
    assert parser.current_hand.action_peflop[1] == Action(ActionType.RAISE, 40)
    assert parser.current_hand.action_peflop[2] == Action(ActionType.CALL, 20)


def test_flop_parser():
    parser = PokerStarsParser()

    lines = ["*** FLOP *** [Th Ac 8h]",
             "MaGiCLeTuR: bets 24",
             "leti5795: folds",
             "Uncalled bet (24) returned to MaGiCLeTuR",
             "MaGiCLeTuR collected 80 from pot",
             "MaGiCLeTuR: doesn't show hand"]

    parser.flop_parser(lines)
    # check board_flop
    assert parser.current_hand.board_flop.__len__() == 3
    assert parser.current_hand.board_flop[0] == Card(Value.TEN, Color.HEARTS)
    assert parser.current_hand.board_flop[1] == Card(Value.ACE, Color.CLUBS)
    assert parser.current_hand.board_flop[2] == Card(Value.EIGHT, Color.HEARTS)
    # check action list
    assert parser.current_hand.action_flop.__len__() == 2
    assert parser.current_hand.action_flop[0] == Action(ActionType.BET, 24)
    assert parser.current_hand.action_flop[1] == Action(ActionType.FOLD)


def test_turn_parser():
    parser = PokerStarsParser()

    lines = ["*** TURN *** [Ts Kc 9d] [3c]",
             "leti5795: checks",
             "onucee: checks"]

    parser.turn_parser(lines)
    # check board_turn
    assert parser.current_hand.board_turn.__len__() ==  1
    assert parser.current_hand.board_turn[0] == Card(Value.THREE, Color.CLUBS)
    # check turn actions
    assert parser.current_hand.action_turn.__len__() == 2
    assert parser.current_hand.action_turn[0] == Action(ActionType.CHECK)
    assert parser.current_hand.action_turn[1] == Action(ActionType.CHECK)


def test_river_parser():
    parser = PokerStarsParser()

    lines = ["*** RIVER *** [Ts Kc 9d 3c] [3s]",
             "leti5795: checks",
             "onucee: checks"]

    parser.river_parser(lines)
    # check board_river
    assert parser.current_hand.board_river.__len__() == 1
    assert parser.current_hand.board_river[0] == Card(Value.THREE, Color.SPADES)
    # check river actions
    assert parser.current_hand.action_river.__len__() == 2
    assert parser.current_hand.action_river[0] == Action(ActionType.CHECK)
    assert parser.current_hand.action_river[1] == Action(ActionType.CHECK)


def test_show_down_parser():
    parser = PokerStarsParser()
    # setup
    # pseudo_positions
    parser.current_hand.pseudo_seats["leti5795"] = 1
    parser.current_hand.pseudo_seats["onucee"] = 2
    parser.current_hand.pseudo_seats["MaGiCLeTuR"] = 3

    # positions
    parser.current_hand.seats[1] = SeatInfo(Player("leti5795"),
                                            450,
                                            [Card(), Card()])
    parser.current_hand.seats[2] = SeatInfo(Player("onucee"),
                                            550,
                                            [Card(), Card()])
    parser.current_hand.seats[3] = SeatInfo(Player("MaGiCLeTuR"),
                                            500,
                                            [Card(), Card()])

    lines = ["*** SHOW DOWN ***",
             "onucee: shows [7s 9d] (a pair of Eights)",
             "MaGiCLeTuR: shows [2s Ah] (two pair, Eights and Deuces)",
             "MaGiCLeTuR collected 120 from pot"]

    parser.show_down_parser(lines)
    assert parser.current_hand.seats[2].cards[0] == Card(Value.SEVEN, Color.SPADES)
    assert parser.current_hand.seats[2].cards[1] == Card(Value.NINE, Color.DIAMONDS)
    assert parser.current_hand.seats[3].cards[0] == Card(Value.TWO, Color.SPADES)
    assert parser.current_hand.seats[3].cards[1] == Card(Value.ACE, Color.HEARTS)

