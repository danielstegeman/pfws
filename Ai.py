#ai v2
import random, math
from deuces import Card, Deck, Evaluator
evaluator = Evaluator()
deck = Deck()
board = deck.draw(5)
def sigmoid(x):
    1/(1+math.exp(-x))

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

class Player():
    global board

    def __init__(self):
        self.hand = deck.draw(2)
        self.bank = 5000
        self.evaluate()

    def evaluate(self):
        self.score = evaluator.evaluate(board,self.hand)
        self.pclass = evaluator.get_rank_class(self.score)
        print "Player 1 hand rank = %d (%s)" % (self.score, evaluator.class_to_string(self.pclass))
        rank = evaluator.evaluate(board, self.hand)
        print "Rank for your hand is: %d" % rank
    def determineOuts(self):
        templist = []
        outs = []
        t = 0
        a = 46.0
        turn = "flop"
        ratio = 0
        for x in Deck.GetFullDeck():
            if x not in self.hand and x not in board:
                if turn == 'flop':
                    listx = board[:3]
                    listx.append(x)
                    #print "listx:"
                    #Card.print_pretty_cards(listx)
                    templist.append(evaluator.evaluate(self.hand,listx))
                    #print templist
                if turn == 'turn':
                    listx = board[:4]
                    a = 46.0
                    listx.append(x)
                    #print "listx:"
                    #Card.print_pretty_cards(listx)
                    templist.append(evaluator.evaluate(self.hand,listx))
                    #print templist


        for i in templist:
            if i < self.score and i < 6185:
                t += 1
            if i not in outs and i < self.score:
                outs.append(i)

        return t
    def turnriver(self):
        t = self.determineOuts()
        if 0<t<23:
            return sigmoid(10*breakevenamount[t]-10*(self.inzet/self.pot))
        elif t ==0:
            print "geen outs"
        elif t > 22:
            return sigmoid(10*0.5-10*(inzet/pot))






















