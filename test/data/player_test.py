from data.player import Player


def test_player_constructor():
    player_test = Player("MaGiCLeTuR")
    assert player_test.pseudo == "MaGiCLeTuR"
