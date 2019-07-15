from enum import Enum


class ActionType(Enum):
    UNDEFINED = 0
    BET = 1
    RAISE = 2
    CHECK = 3
    FOLD = 4
    CALL = 5


class Action:
    """
    It defines all basic action. An action is composed by an action
    type (UNDEFINED, BET, RAISE, CHECK or FOLD) and an amount
    of chip
    """
    def __init__(self, action_type=ActionType.UNDEFINED, amount=0):
        self.action_type = action_type
        self.amount = amount

    def __eq__(self, other):
        if self.action_type == other.action_type and self.amount == other.amount:
            return True
        else:
            return False

    def __str__(self):
        printed = '<' + self.action_type.__str__() + ' ' + self.amount.__str__() + '>'
        return printed

