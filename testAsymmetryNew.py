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

# Lower bound for A1 (equation 10)
def a1l(_m,_a2):
    top = deltah(_m) * ( 2 + deltah(_m)**2 ) - 4 *_a2 * (  6 + deltah(_m) * (deltah(_m)-2 )  )
    bottom = deltah(_m) * (  deltah(_m)**2 - 4 * _a2 * ( deltah(_m) - 2 )  )
    a1low = _a2 * (top / bottom)
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

##### alpha 1 from mathematica
def alpha1(_m,_a1,_a2,_alpha2,_pStar):
    top1 = 4 * _a2**2 * ( 6 + deltah(_m) * (deltah(_m) - 2) )
    top2 = 3 * _a1 * deltah(_m)**3
    top3 = _a2 * deltah(_m) * (   12 * _a1 * ( deltah(_m) - 2 ) + (  6 + deltah(_m) * ( 4 + deltah(_m) )  )   )
    bot1 = _a2 * (  6 + deltah(_m) * ( deltah(_m) - 2 )  ) - _a1 * deltah(_m)**2
    bot2 = 4 * _a2 * ( deltah(_m) - 2 ) - deltah(_m)**2
    top = top1 + top2 - top3
    bottom = bot1 * bot2
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

# Expected Profit Equations

##### Expected Profits with Advertising
def pia1(_p,_m,_a1,_alpha2,_pStar):

    _fa2 = fa2(_p,_m,_alpha2,_pStar)
    capt = (1+_m)**2 - _alpha2 * deltah(_m)
    shop = 2 * _alpha2 * (1-_fa2)
    f = 0.25*_p * (capt + shop) - _a1
    return f

def pia2(_p,_m,_a2,_alpha1,_pStar):

    capt = (1+_m)**2 - _alpha1 * deltah(_m)

    if _p < 1:
        _fa1 = fa1(_p,_m,_alpha1,_pStar)
        shop = 2 * _alpha1 * (1-_fa1)

    else:
        print ("price at v or above")
        return

    f = 0.25*_p * (capt + shop) - _a2
    return f

##### Expected Profits without Advertising
def pin1(_p,_m,_alpha2,_pStar,_pLow):
    capt = 1 - _alpha2 * _m*(2-_m)
    if _p < _pStar:
        _fn2 = fn2(_p,_m,_alpha2,_pStar,_pLow)
        shop = (2 * (1-_alpha2) * (1-_fn2)) + 2 * _alpha2 * (1-_m**2)
    elif _p == _pStar:
        print ("firm 1 would not charge pstar")
        return
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

            a1low = a1l(m, a2)
            a1hi = a2

            for a1 in A:
                a1 = round(a1, 2)

                if a1 > a1low and a1 < a1hi:

                    alpha_1 = alpha1(m,a1,a2,alpha_2,p_star)
                    p_low = plow(m,alpha_1,p_star)

                    beta_1 = beta1(m,alpha_2,alpha_1)
                    beta_2 = beta2(m,alpha_2,alpha_1)


                    fa_1b = fa1(p_star,m,alpha_1,p_star)
                    fa_1t = fa1(1,m,alpha_1,p_star)

                    fa_2b = fa2(p_star,m,alpha_2,p_star)
                    fa_2t = fa2(1,m,alpha_2,p_star)

                    pia_1t = pia1(1,m,a1,alpha_2,p_star)

                    pin_1b = pin1(p_low,m,alpha_2,p_star,p_low)

                    fn_1b = fn1(p_low,m,alpha_1,p_star,p_low)
                    fn_1t = fn1(p_star,m,alpha_1,p_star,p_low)

                    fn_2b = fn2(p_low,m,alpha_2,p_star,p_low)
                    fn_2t = fn2(p_star,m,alpha_2,p_star,p_low)

                    if m == 0.2:
                        print("\nFa2(v): " + str(fa_2t) + "\nFn1(p*): " + str(fn_1t))
                        print("m: " + str(m) + "\nA2: " + str(a2) + "\nA1: " + str(a1))
                        print("Ahi2: " + str(a2hi))

                    pia_2b = pia2(p_star,m,a2,alpha_1,p_star)

                    pin_2b = pin2(p_low,m,alpha_1,p_star,p_low)
                    pin_2t = pin2(p_star,m,alpha_1,p_star,p_low)

                    '''
                    print("pia1(v)= " + str(pia_1t) + \
                            ", pin1(plow)= " + str(pin_1b))


                    print("m: " + str(m) + ", a2: " + str(a2) + \
                          ", a1: " + str(a1) + ", beta1: " + str(beta_1) + \
                          ", alpha1: " + str(alpha_1) + ", pia2b: " + \
                          str(pia_2b) + ", pia2t: " + str(pia_2t) + ", pstar: " +\
                          str(p_star))
                    '''

                    if (alpha_1 <= 0) or (alpha_1 >= 1):
                        print("Error with alpha 1")

                    if (p_low > p_star):
                        print("error with p lower")


                    if (round(pia_1t,4) != round(pin_1b,4)):
                        print("error with pi_1")

                    if (round(pia_2b,4) != round(pin_2b,4)) or (round(pin_2b,4) != round(pin_2t,4)):
                        print("error with pi_2")


                    if (fa_1b != fn_1b):
                        print("Error with F1bs")

                    if  (fa_2b != fn_2b):
                        print("Error with F2bs")

                    '''
                    if (round(fa_2t,4) != 1) or (round(fn_1t,4) != 1):
                        print("\nError with tops")
                    '''

                    if (fa_1t != 1) or (fn_2t != 1):
                        print("Error with mass points")
