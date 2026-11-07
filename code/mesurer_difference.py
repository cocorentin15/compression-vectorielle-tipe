import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad


#x^2 - x
f = [( (k/10) + 1j*(k/10) ) for k in range(101)]
g = [( (k/10) + 1j*((k/10)**2) ) for k in range(101)]

def distance_simple(f,g):
    somme = 0
    for x,y in zip(f,g): #parcours les deux listes en meme temps
        somme += abs(x-y) #rajoute la distance entre les deux points a la valeur totale
        #plt.plot([x.real,y.real],[x.imag,y.imag], color = "green", alpha = 0.5) #trace la ligne dont la valeur viens d'etre ajouté a somme
    return somme/len(f)
