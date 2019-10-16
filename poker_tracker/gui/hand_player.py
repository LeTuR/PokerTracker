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


class Table(QtWidgets.QWidget):
    """"The Table widget display the table and the players

        The Table widget uses the Player widget in order to display all the player.
        The table is represented by an ellipse with a customizable size and color.
        Player widget are positionated around the table according to the max capacity
        of the table set by the game format (heads-up, spin and go, 6-max, etc).
        
        Attributes:
            number_max_players (int): define the maximum number of players at the table
            players (array): all the players widget on the table with the according
                coordinates
            a (int): the ellipse's half width representing the table
            b (int): the ellipse's half height representing the table
    """""
    def __init__(self):
        super().__init__()
        self.setObjectName('table')

        self.number_max_players = 2
        self.players = []
        for i in range(0, 2):
            self.players.append((Player(), QtCore.QPoint()))
        self.players[0][0].set_hand(card.Card(card.Value.EIGHT, card.Color.CLUBS), card.Card(card.Value.KING, card.Color.DIAMONDS))
        # for player, pos in self.players :
        #     player.setHand(card.Card(card.Value.EIGHT, card.Color.CLUBS), card.Card(card.Value.KING, card.Color.DIAMONDS))
        # Table size
        self.a = 300
        self.b = 175

        self.set_player_pos()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)

        painter.setPen(QtGui.Qt.black)
        painter.setBrush(QtGui.Qt.green)
        painter.drawEllipse(self.width()/2 - self.a, self.height()/2 - self.b, 2*self.a, 2*self.b)
        self.set_player_pos()
        k = 0
        for player, pos in self.players:
            player.render(painter, pos)
            k += 1
        return super().paintEvent(event)

    def set_player_pos(self):
        """ Set the all the Player widget coordinates
            
            Set the all the Player widget coordinates in order to be displayed around the
            table. An offset of PI/2 is added in order to set the players[0] on the bottom
            side of the table.
        """
        k = 0
        for player, pos in self.players:
            theta = 2*math.pi * k / self.number_max_players + math.pi / 2
            x = self.a * math.cos(theta) + self.a - player.width / 2 + self.width()/2 - self.a
            y = self.b * math.sin(theta) + self.b - player.height / 2 + self.height()/2 - self.b
            k += 1
            pos.setX(x)
            pos.setY(y)
        self.update()

    def add_player(self):
        return
    
    def remove_player(self):
        return




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

