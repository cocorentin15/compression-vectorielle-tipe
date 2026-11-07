import matplotlib.pyplot as plt
import numpy as np


def fourier(complex_points, pts_random, ens_pts_TF):
    N = len(complex_points)
    def coeff_de_fourrier(p):
        return (1/N)*sum(complex_points[k]*np.exp((-1)*1j*(2*np.pi)*p*k/N) for k in range(0,N))

    def point_de_fourrier(t):
        return sum(coeff_de_fourrier(p)*np.exp(1j*p*(2*np.pi)*t) for p in ens_pts_TF)

    #execution des fonctions
    TF = []
    for i in pts_random:
        TF.append(point_de_fourrier(i))

    #affichage des complexes dans R²
    x_TF = [i.real for i in TF]
    y_TF = [i.imag for i in TF]
    return x_TF,y_TF