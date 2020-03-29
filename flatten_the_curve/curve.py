
"""#SIR model
https://www.youtube.com/watch?v=k6nLfCbAzgo
https://nl.wikipedia.org/wiki/Ziektecompartimentenmodel

Drie groepen: S(usceptible), I(nfected), R(ecovered)
Hoe snel loopt bakje I vol vanuit S (S=>I)
Hoe snel loop bakje I leeg naar R (I=>R)

Hangt af van de transmission rate (S=>I) en recovery rate (I=>R)

Recovery rate (δ):
    Omgekeerde van infectieduur D = 1/δ

Transmission rate (λ):
    Ook wel infectiekracht


r_0 = trans/recov

DV:
    -(S=>I)
    S'(t,S,I,R)

    S=>I, -(I=>R)
    I'(t,S,I,R)

    I=>R
    R'(t,S,I,R)

"""


import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

def trans_r():
    """transmission rate. Flatten The Curve!
    
    Aantal mensen dat een nieuw persoon infect, geloof ik.
    stond iets in de krant
    """
    #return 3.2
    return 1.15

def recov_r():
    """recovery rate
        recovered
        dead
        vaccinated
    """
    #return 0.23
    return 0.33

def rhs(s,v,trans_r,recov_r):
    """RHS equations for SIR model with trans_r and recov_r
    
    Solves these three ordinary differential equations:
    S' = -trans_r*S*I # -(S=>I)
    I' = trans_r*S*I-recov_r*I # S=>I, -(I=>R)
    R' = recov_r*I # I=>R
    """
    S = v[0]
    I = v[1]
    return [-trans_r*S*I,
            trans_r*S*I-recov_r*I,
            recov_r*I]

def sir_model(S,I,R,trans_r,recov_r,t_max,t_num=None):
    """Calculates S(uceptible), I(nfected) and R(ecovered) for 0 to t_max.
    
    Args:

        S (float): initial suceptible
        I (float): initial infected
        R (float): initial recovered
        trans_r (float): transmission rate, see trans_r()
        recov_r (float): recovery rate, see recov_r()
        t_max (float): time point to calculate to
        t_num (float): number of time points

    Returns:

        x (list): list of time points
        y (list): list of values of the solution for S, I and R at t


    """

    if(t_num == None):
        t_num = t_max

    t = np.linspace(0,t_max,t_num)
    r = solve_ivp(rhs,(0,t_max),[S,I,R],method='RK45',t_eval=t,args=(trans_r,recov_r))

    x = r.t.tolist()
    y = r.y.tolist()

    return x,y

def brn(trans_r,recov_r):
    """Calculates basic reproduction number (R0): transmission rate / recovery rate
    
    Args:

        trans_r (float): transmission rate, see trans_r()
        recov_r (float): recovery rate, see recov_r()

    Returns:

        float: the basic reproduction number

    """
    return trans_r/recov_r



# calculate the transmission rate and recovery rate
trans_r = trans_r()
recov_r = recov_r()


# t_max = number of time points to calculate for (e.g. days)
t_max = 20

# initial values for S,I,R
S = 0.98
I = 0.02
R = 0

# calculate x and y
x,y = sir_model(S,I,R,trans_r,recov_r,t_max)

# plot x and y
plt.plot(x,y[0],label='S')
plt.plot(x,y[1],label='I')
plt.plot(x,y[2],label='R')
plt.legend(loc='upper right')
plt.show()

# calculate basic reproduction number
print('r_0: {}'.format(brn(trans_r,recov_r))) # about 3.5 IRL?