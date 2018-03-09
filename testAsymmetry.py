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
def deltah(_m):
    dh = _m*(2+_m)
    return dh

# Bounds for A2: A2 in (A2L,A2H)
def a2l(_m):
    a2low = deltah(_m) / 12.0
    return a2low

def a2h(_m):
    a2hi =  deltah(_m) / 4.0
    return a2hi

# Bounds for A1: A1 in (A1L,A2)
def a1l(_m,_a2):
    top = 3*_a2 - deltah(_m) * 0.25
    bottom = deltah(_m) * ( deltah(_m) * (deltah(_m) * .25 - _a2) + 2*_a2 )
    frac = top / bottom
    a1low = max(0,(1-frac) * _a2)
    return a1low

# Endogenous variables
def alpha2(_m,_a2):
    top = (1+_m)**2 * (deltah(_m)*0.25 - _a2)
    bottom = deltah(_m) * ( (deltah(_m)*0.25 - _a2) + 2*_a2 )
    alphaTwo = top / bottom
    return alphaTwo

def pStar(_m,_alpha2):
    top = (1+_m)**2 - _alpha2*deltah(_m)
    bottom = top + 2*_alpha2
    p = top / bottom
    return p

def alpha1(_m,_a2,_a1,_alpha2,_pStar):
    top = _alpha2 * (3 - deltah(_m))*0.25*_pStar + 3*(_a2-_a1)
    bottom = (3 - deltah(_m))*0.25*_pStar + deltah(_m)*(_a2-_a1)
    alphaOne = top / bottom
    return alphaOne

#########################
# VARIABLES / PARAMETERS
#########################

# set up array for mu in (0,1)
MU = np.arange(0.01,1,.01)
A = np.arange(0.01,1,.01)

########################
# FINAL PROGRAM
########################

# generate mu x A2 x A1 grid
for m in MU:

    a2low = a2l(m)
    a2hi = a2h(m)

    for a2 in A:
        if a2 > a2low and a2 < a2hi:

            a1low = a1l(m,a2)
            a1hi = a2

            for a1 in A:
                if a1 > a1low and a1 < a1hi:

                    alpha_2 = alpha2(m,a2)
                    p_star = pStar(m,alpha_2)
                    alpha_1 = alpha1(m,a2,a1,alpha_2,p_star)

                    print ("mu=" + str(m) + ", A1=" + str(a1) +\
                            ", A2=" + str(a1hi)+ "alpha1 =" + str(alpha_1))
