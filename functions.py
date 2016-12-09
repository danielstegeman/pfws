#-------------------------------------------------------------------------------
# Name:        Function tests
# Purpose:
#
# Author:      5350
#
# Created:     01-12-2016
# Copyright:   (c) 5350 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import math
som = 0
pot = 5
ph_kaartcombinaties = [[1,47],[2,8],[3,7],[4,2],[5,1],[6,0],[7,0],[8,1],[9,0],[10,0]]
def breakeven():

    for entry in range(0,len(ph_kaartcombinaties)):
        som = (ph_kaartcombinaties[entry][1]/kans_outs)/(callamount/pot)
    x = som/outputlink1

    return 1/(1 + math.exp(-x))