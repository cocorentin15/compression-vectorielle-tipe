import numpy as np
import matplotlib.pyplot as plt



import lire_coords
import TFD
import fourier
#import mesurer_difference
import schneider
import mesurer_difference



"""
pts = [
    (0, 0), (0.5, 0.5), (1, 0.8), (1.5, 1), (2, 1.2), (2.5, 1.3), (3, 1.4), (3.5, 1.45), (4, 1.4), (4.5, 1.35), (5, 1.2),
    (5.5, 1), (6, 0.8), (6.5, 0.6), (7, 0.3), (7.5, 0), (8, -0.3), (8.5, -0.6), (9, -0.8), (9.5, -1), (10, -1.2),
    (9.5, -1.1), (9, -1), (8.5, -0.9), (8, -0.8), (7.5, -0.7), (7, -0.6), (6.5, -0.4), (6, -0.2), (5.5, 0), 
    (5, 0.2), (4.5, 0.4), (4, 0.5), (3.5, 0.6), (3, 0.7), (2.5, 0.75), (2, 0.8), (1.5, 0.7), (1, 0.6), (0.5, 0.3), (0, 0)]
"""



def scatter_default():
    plt.scatter([x.real for x in pts_complexes],[y.imag for y in pts_complexes])
    plt.plot([x.real for x in pts_complexes],[y.imag for y in pts_complexes])



"""
def reparametre_fonction(f,complex_pts):
    x_f,y_f = f(complex_pts)
    x_repa,y_repa = reparametrer.reparametre(x_f,y_f,len(pts_complexes))
    return x_repa,y_repa
"""



def start_Schneider():
    plt.figure(1)
    scatter_default()

    erreur_max, erreur_min = 1e15, 0
    erreur = (erreur_max + erreur_min) / 2  
    A = schneider.complex_fitCurve(pts_complexes, erreur)
    
        #algorithme de dichotomie pour faire correspondre le nombre de points avec l'erreur max necessaire
    while len(A)*2+2 not in range(int(n_pt_desiree*0.9),int(n_pt_desiree*1.1)):
        if len(A)*2+2 > n_pt_desiree:
            erreur_min = erreur
        elif len(A)*2+2 < n_pt_desiree: 
            erreur_max = erreur
        erreur = (erreur_max + erreur_min)/2
        A = schneider.complex_fitCurve(pts_complexes, erreur)
        print(len(A)*2+2,erreur)
    
    #tracer les points de schneider utilisés
    for i in schneider.complex_fitCurve(pts_complexes, erreur):
        x_schneider, y_schneider = [],[]
        for j in i:
            x_schneider.append(j[0])
            y_schneider.append(j[1])
            plt.plot(x_schneider,y_schneider, "o-")

    
    
    plt.title("Schneider")
    x,y = schneider.complex_schneider_reparametre(pts_complexes,erreur,nb_points_approx)
    print("n points =",len(x))
    #plt.scatter(x,y)
    plt.plot(x,y,color = "orange")
    #mesurer_difference.distance_simple(pts_complexes, [x[i] + 1j*y[i] for i in range(len(x))])
    print(mesurer_difference.distance_simple(pts_complexes, [x[i] + 1j*y[i] for i in range(len(x))]))



def start_TFD():
    plt.figure(2)
    plt.title("TFD")
    scatter_default()
    x,y = TFD.TFD(pts_complexes,n_pts_taux_TFD)
    plt.scatter(x,y)
    plt.plot(x+[x[0]],y+[y[0]], color = "orange")
    print(mesurer_difference.distance_simple(pts_complexes, [x[i] + 1j*y[i] for i in range(len(x))]))


def start_TFD_reparametre_1():
    plt.figure(4)
    plt.title("TFD_repara")
    scatter_default()
    x,y = TFD.TFD_reparametre(pts_complexes,n_pts_taux_TFD,n_pts_TFD)
    plt.scatter(x,y)
    print(mesurer_difference.distance_simple(pts_complexes, [x[i] + 1j*y[i] for i in range(len(x))]))



def start_Fourier():
    plt.figure(3)
    plt.title("Fourier")
    scatter_default()
    x,y = fourier.fourier(pts_complexes,points_random_TF,ens_points_TF)
    plt.scatter(x,y)
    plt.plot(x,y, color = "orange")
    print(mesurer_difference.distance_simple(pts_complexes, [x[i] + 1j*y[i] for i in range(len(x))]))





#Fourrier
ens_points_TF = range(-250,251)
#grand nombre de points pour s'approcher visuellement de la courbe de notre fonction
points_random_TF = np.linspace(0,1,100)

# TFD
n_pts_taux_TFD = 500
#n_pts_TFD = 10000

#Bezier
n_pt_desiree = 500
nb_points_approx = 100  #int(79              *3/n_pt_desiree)
"""
#DONNEES
pts_x,pts_y = lire_coords.lire_coords("final_dauphin.txt") 
pts_complexes = [pts_x[i] + 1j*pts_y[i] for i in range(len(pts_x))] 

#start_TFD_reparametre_1()

start_Schneider()
#start_Fourier()
#start_TFD()
"""

with open('lead10_matrix.txt', 'r') as file:
    for line in file:
        line_2 = valeurs_numeriques = list(map(float, line.split(',')))
        y = line_2
        pts_complexes = [i+1 + 1j*y[i] for i in range(len(y))]
        start_Schneider()
        start_Fourier()
        start_TFD()
        plt.show()




