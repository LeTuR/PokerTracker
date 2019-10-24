from poker_tracker.data.hand import Hand


def test_hand_constructor():
    hand_test = Hand()
    assert hand_test.id == 1
    hand_test2 = Hand()
    assert hand_test.id == 1
    assert hand_test2.id == 2