######################
# IMPORTS
######################
import csv
import os
import numpy as np

######################
# FUNCTIONS
######################
# common patterns
def deltah(m):
    dh = m*(2+m)
    return dh

# Bounds for A2: A2 in (A2L,A2H)
def a2l(m):
    a2low = deltah(m) / 12.0
    return a2low

def a2h(m):
    a2hi =  deltah(m) / 4.0
    return a2hi

# Bounds for A1: A1 in (A1L,A2)
def a1l(m,a2):
    top = 3*a2 - deltah(m) * 0.25
    bottom = deltah(m) * ( deltah(m) * (deltah(m) * .25 - a2) + 2*a2 )
    frac = top / bottom
    a1low = max(0,(1-frac) * a2)
    return a1low

# Endogenous variables
def alpha2(m,a2):
    top = (1+m)**2 * (deltah(m)*0.25 - a2)
    bottom = deltah(m) * ( (deltah(m)*0.25 - a2) + 2*a2 )
    alphaTwo = top / bottom
    return alphaTwo

#########################
# VARIABLES / PARAMETERS
#########################

# set up array for mu in (0,1)
MU = np.arange(0.01,1,.01)
A = np.arange(0.01,1,.01)

########################
# FINAL PROGRAM
########################

# generate mu x A2 grid
for m in MU:

    a2low = a2l(m)
    a2hi = a2h(m)

    for a2 in A:
        if a2 > a2low and a2 < a2hi:

            a1low = a1l(m,a2)
            a1hi = a2

            alphaTwo = alpha2(m,a2)

            print ("mu=" + str(m) + ", A1L=" + str(a1low) + ", A2=" + str(a1hi)+ "alpha2=" + str(alphaTwo))
