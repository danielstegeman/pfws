#GO.1

#==============================Variables&imports=============================#

from deuces import Card, Evaluator, Deck
from Ai import Player
import math

pot = 100
stages = ['flop','turn','river', 'final']
g_maxinzet = 0
gameprogress = True
blind = 25
dealerpos = 0
small = 1
big = 2
beurt = 0
turn= stages[0]
optafel = [0,0]
vorigoptafel = [0,0]
inzetten = [0,0] #voor iedere speler een waarde
participating = [0,1]
has_folded=[False,False]
has_raised=[False,False]
#===========================Initialize classes===============================#

deck = Deck()
evaluator = Evaluator()
Player1 = Player(0)
Player2 = Player(1)

playerlist = [Player1,Player2]



hands = [Player1.hand,Player2.hand]



#==============================Functies======================================#

def mininzet():
    global g_maxinzet
    for x in playerlist:
        if x.inzet > g_maxinzet:
            g_maxinzet = x.inzet
            return g_maxinzet

def myround(x, base=25):
    return int(base * round(float(x)/base))
def playermoney():
    for x in playerlist:
        if x.index == winner:
            print 'Player %d won $%d' % (winner+1, sum(optafel))
        else:
            print 'Player %d lost $%d' % (x.index+1,optafel[x.index])
def bettinground(stage):
    global has_folded, has_raised,beurt,vorigoptafel,optafel,inzetten, turn
    inzetten = [myround(playerlist[0].turns(stages[stage])),myround(playerlist[1].turns(stages[stage]))]
    has_raised=[False,False]
    print stages[stage]
    while turn == stages[stage]:
            try:
                mininzet()
                if False not in has_folded:
                    gameprogress = False
                    break
    ##            if has_folded[beurt] == True:
    ##                beurt += 1


                if has_raised[beurt] == False:
                    if has_folded[beurt] == False:
                        if inzetten[beurt] <0:
                            #fold
                            print '%d folding' % (beurt + 1)
                            has_folded[beurt] = True
                            has_raised[beurt] = True
                            vorigoptafel[beurt] = optafel[beurt]
                            beurt += 1


                        elif inzetten[beurt] < g_maxinzet:
                            vorigoptafel[beurt] = optafel[beurt]
                            playerlist[beurt].bank -= inzetten[beurt]
                            optafel[beurt] += inzetten[beurt]
                            has_raised[beurt] = True
                            print '%d inzetten' %(beurt+1)
                            print optafel[beurt]
                            beurt += 1

                        else:
                            vorigoptafel[beurt] = optafel[beurt]
                            playerlist[beurt].bank -= inzetten[beurt]
                            optafel[beurt] += inzetten[beurt]

                            has_raised[beurt] = True
                            print '%d inzetten' %(beurt+1)
                            print optafel[beurt]
                            beurt += 1


                else:
                    if has_folded[beurt] == True:
                        gameprogress = False
                        break

                if all(x == True for x in has_raised):
                    vorigoptafel = optafel
                    if optafel[beurt] != max(optafel):
                        optafel[beurt] = max(optafel) #Dit deel callt automatisch
                        playerlist[beurt].bank -= optafel[beurt]-vorigoptafel[beurt]


                    if any(x == True for x in has_folded):
                        gameprogress = False
                        break
                    if all(x==max(optafel) for x in optafel) and all(x == True for x in has_raised):
                        if stage == 3:
                            print "showdown:" #alle bedragen op tafel zijn gelijk aan het hoogste
                            break
                        else:
                            turn = stages[stage+1]
                            break
                    else:
                        beurt +=1


            except IndexError:


                beurt = 0

#=============================Hoofdloop======================================#


for x in range(15):
    board = deck.draw(5)
    for x in playerlist:
        x.evaluate()
        x.hand = deck.draw(2)
        x.board = board
    print "The board:"
    Card.print_pretty_cards(board)
    for x in playerlist:
        print "Player %d's cards: "% (x.index+1)
        Card.print_pretty_cards(x.hand)
    try:
        optafel[small] = 25
        optafel[big] = 50
    except IndexError:
        optafel[0] = 25
        optafel[1] = 50

    vorigoptafel = optafel


    bettinground(0)
    bettinground(1)
    bettinground(2)
    bettinground(3)
    winner = evaluator.hand_summary(board, hands)
    playermoney()
    try:
        for x in winner:
            playerlist[x].bank += sum(optafel)/len(winner)
    except:
        playerlist[winner].bank += sum(optafel)
    for x in playerlist:
        print 'Player %d has $%d in bank' % (x.index+1, x.bank)
    deck.shuffle()
