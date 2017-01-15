#ai v2
import random, math
from deuces import Card, Deck, Evaluator

evaluator = Evaluator()
deck = Deck()



def sigmoid(x):
    return 1/(1+math.exp(-x))

startinghands = [
    ['AA','KK','QQ', 'JJ', 'TT', '99','88','77'
    ,'AK','AQ','AJ','AT','KQ','KJ','KT', 'QJ','QT','JT','J9','T9','98'], #preflop aggresief

    ['66','55','44','33','22', 'A9','A8','A7', 'A6','A5','A4','A3','A2',
    'K9','K8','K7','K6','K5','K4','K3','K2','Q9','Q8','J8','T8','87']#Alleen spelen als de kaarten suited zijn

    ]

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
blind = 25
inzet = 70

class Player():
    board = deck.draw(5)
    maxinzet = 0
    outs = []
    inzet = 0
    def __init__(self,index):
        self.hand = deck.draw(2)
        self.index = index
        self.bank = 5000


    def evaluate(self):
        self.score = evaluator.evaluate(self.board,self.hand)
        self.scoreflop = evaluator.evaluate(self.board[:3], self.hand)
        self.scoreturn = evaluator.evaluate(self.board[:4], self.hand)
        self.pclass = evaluator.get_rank_class(self.score)
        print "Player %d hand rank = %d (%s)" % (self.index+1,self.score, evaluator.class_to_string(self.pclass))
        rank = evaluator.evaluate(self.board, self.hand)
        print "Rank for your hand is: %d" % rank


    def determineOuts(self, turn):
        templist = []
        outs = []
        t = 0
        a = 46.0
        turn = 'turn'
        ratio = 0
        for x in Deck.GetFullDeck():
            if x not in self.hand and x not in self.board:
                if turn == 'turn':
                    listx = self.board[:3]
                    listx.append(x)
                    #print "listx:"
                    #Card.print_pretty_cards(listx)
                    templist.append(evaluator.evaluate(self.hand,listx))
                    #print templist
                if turn == 'river':
                    listx = self.board[:4]
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
                self.outs.append(i)

        return t
    def turnriver(self, turn):
        t = self.determineOuts(turn)
        if 0<t<23:
            return  sigmoid(10*breakevenamount[t]-10*(inzet/pot)) #PLACEHOLDERS VERVANGEN
        elif t ==0:
            print "geen outs"
            return 1
        elif t > 22:
            return sigmoid(10*0.5-10*(inzet/pot))

    def turns(self, turn):
        if turn == 'flop':
            #print 'flop'
            self.inzet = blind *2 / self.flop()
            return self.inzet
        if turn == 'turn':
            self.inzet = (100-self.scoreflop/100.0) /self.turnriver(turn)
            return self.inzet
        if turn == 'river':
            #print 'turn'
            self.inzet = (100-self.scoreturn/100.0) /self.turnriver(turn)
            return self.inzet
        if turn == 'final':
            #print 'final bets'
            self.inzet = (100-self.scoreturn/100.0)
            return self.inzet

    def checksuited(self,hand):

     card1 = Card.int_to_binary(self.hand[0])
     card2 = Card.int_to_binary(self.hand[1])
     for x in range(20,25):
            if card1[x] == '1' and card2[x] == '1':
                return True


    def flop(self):
        a = Card.get_rank_int(self.hand[0])
        b = Card.get_rank_int(self.hand[1])

        if Card.STR_RANKS[a]+Card.STR_RANKS[b] in startinghands[0] and (self.checksuited(self.hand) == True or a == b):
                return sigmoid((a/10+b/10)- 12/10)

        elif Card.STR_RANKS[a]+Card.STR_RANKS[b] in startinghands[1] and (self.checksuited(self.hand) == True or a == b) or (round(sigmoid((a/10)+(b/10)-(16/10))) and random.randint(1,2) ==1):
            return sigmoid((a/10)+(b/10)-(16/10))
            #print 'ok'


        else:
            #print 'garbage'
            c1 = random.randint(9,13)
            c2 = random.randint(9,13)
            if random.randint(1,5) == 1:
            #print 'bluffing'
                return sigmoid((c1/10+c2/10)- 12/10)
            else:
                return -1
            #return sigmoid(a+b-14)

    def inzetander(self):
        return sigmoid(self.inzet/10 - self.maxinzet/10)



















