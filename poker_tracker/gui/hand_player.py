import sys
import random
import math

from poker_tracker.data import card
from PySide2 import QtCore, QtWidgets, QtGui

heartsPNG = './poker_tracker/gui/card/color/heart.png'
diamondsPNG = './poker_tracker/gui/card/color/diamond.png'
spadesPNG = './poker_tracker/gui/card/color/spade.png'
clubsPNG = './poker_tracker/gui/card/color/clubs.png'

redbackJPG = './poker_tracker/gui/card/background/redback.jpg'

redbackPNG = './poker_tracker/gui/card/background/redback.png'

class Player(QtWidgets.QWidget):
    """The Player widget displays the player information

        The player visualization widget will display the hand of the player by using
        the Card widget. It also displays all the information concerning the player
        such as the chip stack, pseudo. The player's information is set with a
        QGridLayout.

        Attribute:
            width (int): the width of the player widget
            height (int): the height of the player widget
            card_1 (card.Card): one card in the hand of the player
            card_2 (card.Card): one card in the hand of the player
            chips (float): the chip stack of the player
            chips_label (QtWidgets.QLabel): QLabel representing the chips info
            layout (QtWidgets.QGridLayout): the layout used to display the 
                player information. 

        TODO set a dynamic hand size for the player (allowing omaha and other variations)
    """
    def __init__(self):
        super().__init__()
        self.setObjectName('player')

        self.width = 140
        self.height = 180
        self.resize(self.width, self.height)

        self.card_1 = Card()
        self.card_2 = Card()
        self.chips = 0

        self.chips_label = QtWidgets.QLabel(text='Chips : ' + self.chips.__str__())
        self.chips_label.setObjectName('playerChips')

        self.layout = QtWidgets.QGridLayout()
        
        self.layout.addWidget(self.card_1, 0, 0)
        self.layout.addWidget(self.card_2, 0, 1)
        self.layout.addWidget(self.chips_label, 1, 0, QtGui.Qt.AlignCenter)
        self.setLayout(self.layout)

    def set_hand(self, card_1=card.Card(), card_2=card.Card()):
        self.card_1.set_card(card_1)
        self.card_2.set_card(card_2)


class Card(QtWidgets.QWidget):
    """ The Card visualization widget allows a card to be displayed.
    
        The Card widget contains a reference to the card to be displayed. An unknown 
        card value or color will imply the display of the back of the card.

        Attributes:
            card (card.Card): a reference to the card to be displayed
            height (int): the card's height
            width (int): the card's width
            x (int): x position of the card
            y (int): y position of the card
            value (string): value of the card
            color (QPixmap): define the color png to be displayed. The pixmap
                is created thanks to a .png file in the ``./card/color`` folder
            font (QFont): define the font and the size for the value text displayed 
    """
    def __init__(self):
        super().__init__()
        
        self.card = card
    
        self.height = 70
        self.width = 50
        self.x = 0
        self.y = 0

        self.value = ''
        self.color = None
        self.font = QtGui.QFont('Calibri', 25)

    def update_card(self):
        """ Update the value and the color of the card to be displayed.

            Color enum is converted into the correct pixmap using the right .PNG file.
            The card value is converted into a string.
        """
        # Set the card's color
        if (self.card.color == card.Color.SPADES) : 
            self.color = QtGui.QPixmap(spadesPNG)
        elif (self.card.color == card.Color.HEARTS) : 
            self.color = QtGui.QPixmap(heartsPNG)
        elif (self.card.color == card.Color.CLUBS) : 
            self.color = QtGui.QPixmap(clubsPNG)
        elif (self.card.color == card.Color.DIAMONDS) : 
            self.color = QtGui.QPixmap(diamondsPNG)
        else : 
            self.color = None
        # Set the card's value
        if (self.card.value == card.Value.ACE) :
            self.value = 'A'
        elif (self.card.value == card.Value.TWO) :
            self.value = '2'
        elif (self.card.value == card.Value.THREE) :
            self.value = '3'
        elif (self.card.value == card.Value.FOUR) :
            self.value = '4'
        elif (self.card.value == card.Value.FIVE) :
            self.value = '5'
        elif (self.card.value == card.Value.SIX) :
            self.value = '6'
        elif (self.card.value == card.Value.SEVEN) :
            self.value = '7'
        elif (self.card.value == card.Value.EIGHT) :
            self.value = '8'
        elif (self.card.value == card.Value.NINE) :
            self.value = '9'
        elif (self.card.value == card.Value.TEN) :
            self.value = '10'
        elif (self.card.value == card.Value.JACK) :
            self.value = 'J'
        elif (self.card.value == card.Value.QUEEN) :
            self.value = 'Q'
        elif (self.card.value == card.Value.KING) :
            self.value = 'K'
        else :
            self.value = ''
        # The widget must be update in order to be shown
        self.update()

    def set_card(self, card):
        """ Set the card reference and update the object for
            a correct display """
        self.card = card
        # Update the value and color of the new card
        self.update_card()

    def set_pos(self, x, y):
        """ Set the position of the card displayed inside the Card Widget """
        self.x = x
        self.y = y

    def paintEvent(self, event):
        # Layout paramters of all the card component (color.png, text...) 
        value_offset_x = 5
        value_offset_y = 45
        color_offset_x = 25
        color_offset_y = 22
        color_height = 23
        color_width = 23

        painter = QtGui.QPainter(self)
        # Set black borders to all the drawn object
        painter.setPen(QtGui.Qt.black)

        # Draw the back of the card if the value or the color is undefined
        if self.value == '' or self.color == None:
            # Draw a border the border of the card
            painter.setBrush(QtGui.Qt.white)
            painter.drawRoundedRect(self.x, self.y, self.width, self.height, 5, 5)
            # Fill the inside of the card's back with a color
            painter.setBrush(QtGui.Qt.red)
            painter.drawRect(self.x+3, self.y+3, self.width-6, self.height-6)

        # Draw the card showing the value and the color
        else :
            # Draw the card's body
            painter.setBrush(QtGui.Qt.white)
            painter.drawRoundedRect(self.x, self.y, self.width, self.height, 5, 5)
            # Draw the card value
            painter.setFont(self.font)
            painter.drawText(QtCore.QPoint(self.x+value_offset_x, self.y+value_offset_y), self.value)
            # Draw the card color
            target = QtCore.QRect(self.x+color_offset_x, self.y+color_offset_y, color_height, color_width)
            painter.drawPixmap(target, self.color)
        return super().paintEvent(event)

