from deuces import Card, Evaluator, Deck
from Ai import Player, board

import math

#------------------Eigen variabelen-----------------
breakevenamount = {1:0.021,
    2:0.043,
    3:0.064,
    4:0.085,
    5:0.106,
    6:0.128,
    7:0.149,
    8:0.17,
    9:0.191,
    10:0.213,
    11:0.234,
    12:0.255,
    13:0.277,
    14:0.298,
    15:0.319,
    16:0.34,
    17:0.362,
    18:0.383,
    19:0.404,
    20:0.426,
    21:0.447,
    22:0.468}

pot = 100
inzet = 21.3
stages = ['flop','turn','river', 'final']
g_maxinzet = 0

#---------------------------------------------------

def mininzet():
    global g_maxinzet
    for x in playerlist:
        if x.inzet > g_maxinzet:
            g_maxinzet = x.inzet
            return g_maxinzet



deck = Deck()
# create a card
card = Card.new('Qh')

# create a board and hole cards
"""
board = [
    Card.new('Ah'),
    Card.new('2h'),
    Card.new('Jh'),
    Card.new('6c'),
    Card.new('9c')
]
hand = [
    Card.new('8c'),
    Card.new('Qs')
]
"""
evaluator = Evaluator()

#=====================================AI integratie=========================
#uiteindelijk moet in dit blok het verloop van het spel komen
Player1 = Player(0)
Player2 = Player(1)

playerlist = [Player1,Player2]

hands = [Player1.hand,Player2.hand]

player1_hand = Player1.hand
hand = Player1.hand
player2_hand = Player2.hand

print "The board:"
Card.print_pretty_cards(board)

print "Player 1's cards:"
Card.print_pretty_cards(player1_hand)

print "Player 2's cards:"
Card.print_pretty_cards(player2_hand)
evaluator.hand_summary(board, hands)

for x in stages:
    print x
    print 'p1:'
    print Player1.turns(x)
    print 'p2:'
    print Player2.turns(x)
mininzet()
for x in playerlist:
    x.maxinzet = g_maxinzet

#----------------------------------------------------------------------------


# pretty print cards to console
#Card.print_pretty_cards(board + hand)

# create an evaluator


# and rank your han
#rank = evaluator.evaluate(board, hand)
#print "Rank for your hand is: %d" % rank

# or for random cards or games, create a deck






#p1_score = evaluator.evaluate(board, player1_hand)
#p2_score = evaluator.evaluate(board, player2_hand)

# bin the scores into classes
#p1_class = evaluator.get_rank_class(p1_score)
#p2_class = evaluator.get_rank_class(p2_score)

# or get a human-friendly string to describe the score
#print "Player 1 hand rank = %d (%s)" % (p1_score, evaluator.class_to_string(p1_class))
#print "Player 2 hand rank = %d (%s)" % (p2_score, evaluator.class_to_string(p2_class))

# or just a summary of the entire hand



def sigmoid(x):
    return 1/(1+math.exp(-x))


def inzetander():
    return sigmoid(Player2.inzet/10-Player1.inzet/10)

print inzetander()

"""
#=====================================================================#
#------------------------------TEST-----------------------------------#
# dit deel bevat de volgende dingen
#   *Een 'functie' die de outs checkt.
#   * Een sigmoid functie:
#       - kijkt welk breakeven percentage(van internet gehaald) gebruikt moet worden
#       - als de inzet/pot < breakeven is: output <0.5
#        - als die groter is, output >0.5
# Dit is dus de voornaamste schakel die bepaald of er ingezet, gepast word of verhoogd
#=====================================================================#




templist = []
outs = []
t = 0
a = 46.0
turn = "flop"
ratio = 0
for x in deck.GetFullDeck():
    if x not in player1_hand and x not in board:
        if turn == 'flop':
            listx = board[:3]
            listx.append(x)
            #print "listx:"
            #Card.print_pretty_cards(listx)
            templist.append(evaluator.evaluate(player1_hand,listx))
            #print templist
        if turn == 'turn':
            listx = board[:4]
            listx.append(x)
            #print "listx:"
            #Card.print_pretty_cards(listx)
            templist.append(evaluator.evaluate(player1_hand,listx))
            #print templist


for i in templist:
    if i < p1_score and i < 6185:
        t += 1
    if i not in outs and i < p1_score:
        outs.append(i)

if t ==0:
    print "geen outs"

if 0<t<23:
    sigmoid(10*breakevenamount[t]-10*(inzet/pot))

print t
print outs


#==================================================================


#-------------------------------------------------------------------
#--------------------------Preflop----------------------------------
#-------------------------------------------------------------------

def checksuited(hand):

     card1 = Card.int_to_binary(hand[0])
     card2 = Card.int_to_binary(hand[1])
     print card1
     print card2
     for x in range(20,25):
            if card1[x] == '1' and card2[x] == '1':
                return True


startinghands = [
    ['AA','KK','QQ', 'JJ', 'TT', '99','88','77'
    ,'AK','AQ','AJ','AT','KQ','KJ','KT', 'QJ','QT','JT','J9','T9','98'], #preflop aggresief

    ['66','55','44','33','22', 'A9','A8','A7', 'A6','A5','A4','A3','A2',
    'K9','K8','K7','K6','K5','K4','K3','K2','Q9','Q8','J8','T8','87']#Alleen spelen als de kaarten suited zijn

    ]
a = Card.get_rank_int(hand[0])
b = Card.get_rank_int(hand[1])
if checksuited(player1_hand) == True or a == b:
    if Card.STR_RANKS[a]+Card.STR_RANKS[b] in startinghands[0]:
        print 'true'
        sigmoid(a+b-14)
else:
    print 'garbage'
    sigmoid(a+b-14)


pot = 100
inzetp1 = 50
inzetp2 = 100

templist2 = []
for x in deck.GetFullDeck():
    if x not in player1_hand and x not in board:


"""





#24 25 26 27




