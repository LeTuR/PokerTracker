from enum import Enum


class Color(Enum):
    """ An enumeration defining all the colors in a deck of 52 cards
    """
    UNDEFINED = 0
    HEARTS = 1
    CLUBS = 2
    SPADES = 3
    DIAMONDS = 4


class Value(Enum):
    """ An enumeration defining all the values in a deck of 52 cards
    """
    UNDEFINED = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7
    NINE = 8
    TEN = 9
    JACK = 10
    QUEEN = 11
    KING = 12
    ACE = 13


class Card:
    """ This class set the basic structure of a card in poker.
    
        A card is defined by 2 parameters : the value and the color
        The value is set with one of the following {TWO, THREE, FOUR,
        FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE,
        UNDEFINED}. The color is set with one of the following :
        {HEARTS, CLUBS, SPADES, DIAMONDS, UNDEFINED}

        Args:
            value (Value): the value of the card
            color (Color): the color of the card
        
        Returns:
            value (Value): the value of the card
            color (Color): the color of the card    
    """
    def __init__(self, value=Value.UNDEFINED, color=Color.UNDEFINED):
        self.value = value
        self.color = color

    def __eq__(self, other):
        if self.value == other.value and self.color == other.color:
            return True
        else:
            return False

    def __str__(self):
        printed = '<' + self.value.__str__() + '>' + '<' + self.color.__str__() + '>'
        return printed
