    #test voor ann
    #ph voor var: placeholder

    #som van kansen op hand

totale_pot = 1000.0
call_amount = 10
current_turn = "flop"
breakevenamount = {1:0.022222222,2:0.045454545, 3:0.06993007,4:0.095238095,5:0.12195122,6:0.149253731,7:0.178571429,8:0.210526316,9:0.243902439,
10:0.277777778, 11:0.3125,12:0.357142857,13:0.4}
import random, math

class Ann:
    import random, math

    ph_kaartcombinaties = [[1,47],[2,8],[3,7],[4,2],[5,1],[6,0],[7,0],[8,1],[9,0],[10,0]]#moet up to date blijven op basis van het spel


    ph_inzet_ander = 0
    mutator_link_2 = 0.1
    kans_outs = 0
    output_link_1 = 0.0
    output_link_2 = 0.0
    done = False

    #alle input data in een list
    ann_vars = [mutator_link_2,ph_inzet_ander]
    #link 1 af
    #link 1 op basis van kansen
    # link 1 is het uitgangspunt voor de inzet. Works as intended
    def link_1(self):
        kans = 0
        self.output_link_1 = 0.0
        for entry in range(0,len(self.ph_kaartcombinaties)):
            if self.ph_kaartcombinaties[entry][1] > 0:
                kans = self.kans_outs(entry)
                self.output_link_1 = self.output_link_1 + ph_kaartcombinaties[entry][0]/kans





        #return output_link_1
        print self.output_link_1

    #link 2 neemt uitkomst link 1 en geeft nieuwe waarde door op basis van de inzet van een andere speler
    #outdated
    def link_2(self,ph_inzet_ander, output_link_1,mutator_link_2):

        self.output_link_2 = -mutator_link_2 * ph_inzet_ander + output_link_1
        print self.output_link_2



    def kans_outs(self,entry):
        #anders bij een leeg bord
        global current_turn
        if current_turn == "flop":
            if self.ph_kaartcombinaties[entry][1] > 0:
                return 1-(
                    (


                    (
                        (47-int(self.ph_kaartcombinaties[entry][1])
                        )
                            /47.0 #placeholder: kaarten in deck
                    )*
                    (
                        (46-int(self.ph_kaartcombinaties[entry][1])
                        )
                            /46.0 #idem
                    )
                    )
                    )


        elif current_turn == "turn":
            if self.ph_kaartcombinaties[entry][1] > 0:
                return self.ph_kaartcombinaties/ 46.0

    def break_even(self):
        global call_amount, totale_pot, breakevenamount
        cumul_odds = 0
        avg = 0
        count = 0
        #gemiddelde opruimen
        for entry in range(0,len(self.ph_kaartcombinaties)):
            if 0 < self.ph_kaartcombinaties[entry][1] <14:
                cumul_odds = cumul_odds + self.ph_kaartcombinaties[entry][0]* breakevenamount[self.ph_kaartcombinaties[entry][1]]
                print "cumulodds"+ str(cumul_odds)
                avg = avg + breakevenamount[self.ph_kaartcombinaties[entry][1]]
                count = count + 1
                print 'avg' + str(avg)
                print 'count'+str(count)


        avg = avg/ count
        print 'avg'+str(avg)
        pot_odds = call_amount / totale_pot * avg
        print 'count'+ str(pot_odds)
        x = cumul_odds - pot_odds
        print 'x'+ str(x)
        return 1/(1+ 0.1*math.exp(-x))

    #def bluff(self):



#Execute ANN
p = Ann()

