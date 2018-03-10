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
    dh = _m * (2 + _m)
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
    a1low = _a2 - 0.25 * _pStar * (1 - _alpha2)
    a1low = max(0, a1low)
    return a1low

# Endogenous variables
def alpha2(_m,_a2):
    top = (1 + _m)**2 * (deltah(_m) * 0.25 - _a2)
    bottom = deltah(_m) * (deltah(_m) * 0.25 - _a2) + 2 * _a2
    alphaTwo = top / bottom
    return alphaTwo

def pStar(_m,_alpha2):
    top = (1 + _m)**2 - _alpha2 * deltah(_m)
    bottom = top + 2 * _alpha2
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
    betaOne = ((_alpha1 - _alpha2) / _alpha1) * (top/bottom)
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

# Firm price distributions
def fa1(_p,_m,_alpha1,_pStar):
    if _p < _pStar:
        f = 0
    elif _p < 1:
        top = (1-_alpha1) * (1+_m)**2 + 3*_alpha1
        frac = top / (2*_alpha1)
        f = frac * (1-(_pStar/_p))
    else:
        f = 1
    return f

def fa2(_p,_m,_alpha2,_pStar):
    if _p < _pStar:
        f = 0
    elif _p <= 1:
        top = (1-_alpha2) * (1+_m)**2 + 3*_alpha2
        frac = top / (2*_alpha2)
        f = frac * (1-(_pStar/_p))
    else:
        f = 1
    return f

'''
def fn1(_p,_m,_alpha1,_pStar,_pLow):
    if _p < _pLow:
        f = 0
    elif _p <= _pStar:
        top = 3 - _alpha1 * deltah(_m)
        frac = top / (2*(1 - _alpha1))
        f = frac * (1-(_pLow/_p))
    else:
        f = 1
    return f

def fn2(_p,_m,_alpha2,_pStar,_pLow):
    if _p < _pLow:
        f = 0
    elif _p < _pStar:
        top = 3 - _alpha2 * deltah(_m)
        frac = top / (2*(1 - _alpha2))
        f = frac * (1-(_pLow/_p))
    else:
        f = 1
    return f
'''

# Expected Profit Equations
def pia1(_p,_m,_a1,_alpha2,_pStar):
    _fa2 = fa2(_p,_m,_alpha2,_pStar)
    capt = (1+_m)**2 - _alpha2 * deltah(_m)
    shop = 2 * _alpha2 * (1-_fa2)
    f = 0.25*_p * (capt + shop) - _a1
    return f

def pia2(_p,_m,_a2,_alpha1,_pStar,_beta1):

    capt = (1+_m)**2 - _alpha1 * deltah(_m)

    if _p < 1:
        _fa1 = fa1(_p,_m,_alpha1,_pStar)
        shop = 2 * _alpha1 * (1-_fa1)

    elif _p == 1:
        shop = _alpha1 * _beta1

    else:
        print ("price above v")
        return

    f = 0.25*_p * (capt + shop) - _a2
    return f

'''
def pin1(_p,_m,_alpha2,_pStar,_pLow,_beta2):
    capt = 1 - _alpha2 * _m*(2-_m)
    if _p < _pStar:
        _fn2 = fn2(_p,_m,_alpha2,_pStar,_pLow)
        shop = (2 * (1-_alpha2) * (1-_fn2)) + 2 * _alpha2 * (1-_m**2)
    elif _p == _pStar:
        shop = (1-_alpha2) * _beta2 + 2 * _alpha2 * (1-_m**2)
    else:
        print ("price above v")
        return
    f = 0.25*_p * (capt + shop)
    return f

def pin2(_p,_m,_alpha1,_pStar,_pLow):
    _fn1 = fn1(_p,_m,_alpha1,_pStar,_pLow)
    capt = 1 - _alpha1 * _m*(2-_m)
    shop = (2 * (1-_alpha1) * (1-_fn1)) + 2 * _alpha1 * (1-_m**2)
    f = 0.25*_p * (capt + shop)
    return f
'''

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
    m = round(m, 2)

    a2low = a2l(m)
    a2hi = a2h(m)

    for a2 in A:
        a2 = round(a2, 2)

        if a2 > a2low and a2 < a2hi:

            alpha_2 = alpha2(m,a2)
            p_star = pStar(m,alpha_2)

            a1low = a1l(m, a2, alpha_2, p_star)
            a1hi = a2

            for a1 in A:
                a1 = round(a1, 2)

                if a1 > a1low and a1 < a1hi:

                    alpha_1 = alpha1(m,a2,a1,alpha_2,p_star)
                    p_low = plow(m,alpha_1,p_star)

                    beta_1 = beta1(m,alpha_2,alpha_1)
                    beta_2 = beta2(m,alpha_2,alpha_1)

                    pia_1b = pia1(p_star,m,a1,alpha_2,p_star)
                    pia_1t = pia1(1,m,a1,alpha_2,p_star)

                    pia_2b = pia2(p_star,m,a2,alpha_1,p_star,beta_1)
                    pia_2t = pia2(1,m,a2,alpha_1,p_star,beta_1)

                    print("m: " + str(m) + ", a2: " + str(a2) + \
                          ", a1: " + str(a1) + ", beta1: " + str(beta_1) + \
                          ", alpha1: " + str(alpha_1) + ", pia2b: " + \
                          str(pia_2b) + ", pia2t: " + str(pia_2t) + ", pstar: " +\
                          str(p_star))

                    fa_1b = fa1(p_star,m,alpha_1,p_star)
                    fa_1t = fa1(1,m,alpha_1,p_star)

                    fa_2b = fa2(p_star,m,alpha_2,p_star)
                    fa_2t = fa2(1,m,alpha_2,p_star)

                    '''
                    fn_1b = fn1(p_low,m,alpha_1,p_star,p_low)
                    fn_1t = fn1(p_star,m,alpha_1,p_star,p_low)

                    fn_2b = fn2(p_low,m,alpha_2,p_star,p_low)
                    fn_2t = fn2(p_star,m,alpha_2,p_star,p_low)

                    pin_1b = pin1(p_low,m,alpha_2,p_star,p_low,beta_2)
                    pin_1t = pin1(p_star,m,alpha_2,p_star,p_low,beta_2)

                    pin_2b = pin2(p_low,m,alpha_1,p_star,p_low)
                    pin_2t = pin2(p_star,m,alpha_1,p_star,p_low)
                    '''

                    if (p_low > p_star):
                        print("error with p lower")

                    if (round(pia_1b,4) != round(pia_1t,4)):
                        print("error with pia_1")
