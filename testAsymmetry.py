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
''' original lower bound for a1 (equ 21)

def a1l(_m,_a2):
    top = 3*_a2 - deltah(_m) * 0.25
    bottom = deltah(_m) * ( deltah(_m) * (deltah(_m) * .25 - _a2) + 2*_a2 )
    frac = top / bottom
    a1low = max(0,(1-frac) * _a2)
    return a1low
'''

# New lower bound for A1
# derived by setting alpha1<1 using equ 20
def a1l(_m,_a2,_alpha2,_pStar):
    a1low = _a2 - 0.25*_pStar*(1-_alpha2)
    a1low = max(0, a1low)
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

def beta1(_m,_alpha2,_alpha1):
    top = (1+_m)**2
    bottom = top - _alpha2 * (deltah(_m) - 2)
    betaOne = ((_alpha1 - _alpha2)/_alpha1)*(top/bottom)
    return betaOne

def beta2(_m,_alpha2,_alpha1):
    top = 3 - deltah(_m)
    bottom = 3 - _alpha1 * deltah(_m)
    betaTwo = ((_alpha1 - _alpha2)/(1-_alpha2))*(top/bottom)
    return betaTwo

def plow(_m,_alpha1,_pStar):
    top = 1 - _alpha1 * (deltah(_m)-2)
    bottom = 3 - _alpha1*deltah(_m)
    pLow = _pStar * top / bottom
    return pLow

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

            alpha_2 = alpha2(m,a2)
            p_star = pStar(m,alpha_2)

            a1low = a1l(m, a2, alpha_2, p_star)
            a1hi = a2

            for a1 in A:
                if a1 > a1low and a1 < a1hi:

                    alpha_1 = alpha1(m,a2,a1,alpha_2,p_star)
                    beta_1 = beta1(m,alpha_2,alpha_1)
                    beta_2 = beta2(m,alpha_2,alpha_1)
                    p_low = plow(m,alpha_1,p_star)

                    if (beta_1 < 0 or beta_1 > 1):
                        print("error with beta_1")

                    if (beta_2 < 0 or beta_2 > 1):
                        print("error with beta_2")

                    if (p_low > p_star):
                        print("error with p lower")

                    '''
                    print ("mu = " + str(m) + ", A1Low = " + str(a1low) + ", A1 = " + str(a1) +\
                            ", A2 = " + str(a1hi)+ ", alpha1 = " + str(alpha_1))
                    '''
