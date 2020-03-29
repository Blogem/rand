
"""
# https://www.youtube.com/watch?v=k6nLfCbAzgo

Drie groepen: S(usceptible), I(nfected), R(ecovered)
Hoe snel loopt bakje I vol vanuit S (S=>I)
Hoe snel loop bakje I leeg naar R (I=>R)

Hangt af van de transmission (S=>I) en recovery rate (I=>R)


dy(t)/dt = -k y(t)


I'(t,S,I,R) = 2SI-0.3I

r_0 = trans/recov

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


def rate_of_change(t,S,I,R,trans_r,recov_r):
    return trans_r*S*I
    ##
    ## nog fixen voor negatieve rate of change!
    ##
    """
    # ordinary differential equation
    S' = -trans_r*S*I # -(S=>I)
    I' = trans_r*S*I-recov_r*I # S=>I, -(I=>R)
    R' = recov_r*I # I=>R

    list_of_derivates = [Sd,Id,Rd]
    initial_x_coordinate = 0
    initial_y_coordinates = [S,R,I]
    final_x_coordinate  = t

    NSolveODE(list_of_derivatives,intial_x_coordinate,initial_y_coordinates,final_x_coordinate) 
    """


def trans_r():
    """
    transmission rate
    
    Aantal mensen dat een nieuw persoon infect, geloof ik.
    stond iets in de krant
    """
    #return 3.2
    return 1.15

def recov_r():
    """
    recovery rate
    GEEN IDEE
    """
    #return 0.23
    return 0.23

def rhs(s,v,trans_r,recov_r):
    # S' = -trans_r*S*I # -(S=>I)
    # I' = trans_r*S*I-recov_r*I # S=>I, -(I=>R)
    # R' = recov_r*I # I=>R
    S = v[0]
    I = v[1]
    return [-trans_r*S*I,
            trans_r*S*I-recov_r*I,
            recov_r*I]



trans_r = trans_r() # transmission rate, die uit de krant?
recov_r = recov_r() # ...

maxT = 50
S = 0.98
I = 0.02
R = 0


t = np.linspace(0,maxT) # maxT
r = solve_ivp(rhs,(0,maxT),[S,I,R],method='RK45',t_eval=t,args=(trans_r,recov_r))


t = r.t.tolist()
y = r.y.tolist()

print(y)

plt.plot(t,y[0],label='S')
plt.plot(t,y[1],label='I')
plt.plot(t,y[2],label='R')
plt.legend(loc='upper right')
plt.show()
