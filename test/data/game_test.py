from dataStructure.game import Game


def test_game_constructor():
    """Test id generation"""
    game_test = Game()
    assert game_test.id == 1
    game_test2 = Game()
    assert game_test.id == 1
    assert game_test2.id == 2
