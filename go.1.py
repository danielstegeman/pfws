#GO.1
import sys
f = open("test.txt", 'w')
sys.stdout = f
#==============================Variables&imports=============================#

from deuces import Card, Evaluator, Deck
from Ai import Player, countmatherrors
import math

pot = 0
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
def changeobjVars(variable, new_value):
    for x in playerlist:
        x.variable = new_value
def mininzet():
    global g_maxinzet
    for x in playerlist:
        if x.inzet > g_maxinzet:
            g_maxinzet = x.inzet
            return g_maxinzet

def myround(x, base=5):
    return int(base * round(float(x)/base))
def playermoney():
    for x in playerlist:
        if x.index == winner:
            print 'Player %d won $%d' % (winner+1, sum(optafel))
        else:
            print 'Player %d lost $%d' % (x.index+1,optafel[x.index])
def bettinground(stage):
    global has_folded, has_raised,beurt,vorigoptafel,optafel,inzetten, turn, g_maxinzet, pot

    has_raised = [False, False]

    print stages[stage]
    while turn == stages[stage]:
        pot = sum(optafel)
        inzetten = [myround(playerlist[0].turns(stages[stage])),myround(playerlist[1].turns(stages[stage]))]

        try:
            if False not in has_folded:
                gameprogress = False
                break
##            if has_folded[beurt] == True:
##                beurt += 1


            if has_raised[beurt] == False:
                print "Player %d's cards: "% (playerlist[beurt].index+1)
                Card.print_pretty_cards(playerlist[beurt].hand)
                if has_folded[beurt] == False:
                    if inzetten[beurt]== 0:
                        #checking
                        print 'Player %d checking' %(beurt +1)
                        has_raised[beurt] = True
                        vorigoptafel[beurt] = optafel[beurt]
                        beurt += 1

                    if inzetten[beurt] <0:
                        #fold
                        print '%d folding' % (beurt + 1)
                        print ''
                        has_folded[beurt] = True
                        has_raised[beurt] = True
                        vorigoptafel[beurt] = optafel[beurt]
                        beurt += 1


                    elif inzetten[beurt] < g_maxinzet:
                        vorigoptafel[beurt] = optafel[beurt]

                        playerlist[beurt].bank -= inzetten[beurt]
                        optafel[beurt] += inzetten[beurt]
                        has_raised[beurt] = True
                        print 'Player %d raises with %d$' %(beurt+1, inzetten[beurt])
                        print 'Player %d has %d$ on table'%(beurt+1, optafel[beurt])
                        print ''
                        beurt += 1

                    else:
                        vorigoptafel[beurt] = optafel[beurt]
                        if inzetten[beurt] > g_maxinzet:
                            g_maxinzet = inzetten[beurt]
                            for x in playerlist:
                                x.maxinzet = g_maxinzet
                        playerlist[beurt].bank -= inzetten[beurt]
                        optafel[beurt] += inzetten[beurt]

                        has_raised[beurt] = True
                        print 'Player %d raises with %d$' %(beurt+1, inzetten[beurt])
                        print 'Player %d has %d$ on table'%(beurt+1, optafel[beurt])
                        print ''
                        beurt += 1


            else:
                if has_folded[beurt] == True:
                    beurt +=1

            if all(x == True for x in has_raised):
                vorigoptafel = optafel
                if optafel[beurt] != max(optafel):
                    if playerlist[beurt].willcall()>=0:

                        optafel[beurt] = max(optafel) #Dit deel callt automatisch
                        playerlist[beurt].bank -= optafel[beurt]-vorigoptafel[beurt]
                        print 'Player %d Calling'% (beurt + 1)

                    else:
                        #fold
                        print 'Player %d folding' % (beurt + 1)
                        has_folded[beurt] = True
                        has_raised[beurt] = True
                        vorigoptafel[beurt] = optafel[beurt]
                        beurt += 1



                if any(x == True for x in has_folded):
                    if stage == 3:
                        print "showdown:" #alle bedragen op tafel zijn gelijk aan het hoogste
                        break
                    else:
                        print 'The pot is now %d$' %(pot)
                        print ''
                        turn = stages[stage+1]
                        break
                if all(x==max(optafel) for x in optafel) and all(x == True for x in has_raised):
                    if stage == 3:
                        print "showdown:" #alle bedragen op tafel zijn gelijk aan het hoogste
                        break
                    else:
                        print 'The pot is now %d$' %(pot)
                        print ''
                        turn = stages[stage+1]
                        break
                else:
                    beurt +=1
            elif has_folded[beurt] == True and has_raised[beurt] == False:
                has_raised[beurt] = True


        except IndexError:


            beurt = 0

#=============================Hoofdloop======================================#

#"""

#debugging vars
countUnknownkeyerrors = 0
countmathoverflowerrors = 0
countraiseoverflow = 0

#------------
for x in range(1000):
    print 'round %d' %(x)
    global has_folded,has_raised, g_maxinzet

    deck.shuffle()
    has_folded = [False, False]
    turn = stages[0]

    board = deck.draw(5)
    for x in playerlist:
        x.evaluate()
        x.hand = deck.draw(2)
        x.board = board
        x.pot = pot
    hands = [Player1.hand,Player2.hand]

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

    try:
        bettinground(0)
        g_maxinzet = 0
        for x in playerlist:
            x.maxinzet = g_maxinzet
        print "The board:"
        Card.print_pretty_cards(board[:3])

        bettinground(1)
        g_maxinzet = 0
        for x in playerlist:
            x.maxinzet = g_maxinzet
        print "The board:"
        Card.print_pretty_cards(board[:4])

        bettinground(2)
        g_maxinzet = 0
        for x in playerlist:
            x.maxinzet = g_maxinzet

        print "The board:"
        Card.print_pretty_cards(board)
        bettinground(3)

        winner = evaluator.hand_summary(board, hands)
        if pot > 2000:
            print 'Unknown bug causes the raise to be absolutely bonkers, skipping this round'
            countraiseoverflow+=1
            continue
        playermoney()
    except KeyError:
        print "KeyError, Skipping round"
        countUnknownkeyerrors +=1
        #oorzaak van de keyerror onbekend
        continue
    try:
        for x in winner:
            if has_folded[x] == False:
                playerlist[x].bank += sum(optafel)/len(winner)
    except:
        playerlist[winner].bank += sum(optafel)
    for x in playerlist:
        print 'Player %d has $%d in bank' % (x.index+1, x.bank)

print countmatherrors
print countraiseoverflow
print countUnknownkeyerrors

f.close()