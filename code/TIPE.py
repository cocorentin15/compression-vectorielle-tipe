import math
import numpy as np
import matplotlib.pyplot as plt
"""
pts = [
    (0, 0), (0.5, 0.5), (1, 0.8), (1.5, 1), (2, 1.2), (2.5, 1.3), (3, 1.4), (3.5, 1.45), (4, 1.4), (4.5, 1.35), (5, 1.2),
    (5.5, 1), (6, 0.8), (6.5, 0.6), (7, 0.3), (7.5, 0), (8, -0.3), (8.5, -0.6), (9, -0.8), (9.5, -1), (10, -1.2),
    (9.5, -1.1), (9, -1), (8.5, -0.9), (8, -0.8), (7.5, -0.7), (7, -0.6), (6.5, -0.4), (6, -0.2), (5.5, 0), 
    (5, 0.2), (4.5, 0.4), (4, 0.5), (3.5, 0.6), (3, 0.7), (2.5, 0.75), (2, 0.8), (1.5, 0.7), (1, 0.6), (0.5, 0.3), (0, 0)]
"""
#conversion points du txt en points sous format correct
def read_click_coords(file_path):
    points = []
    
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip().replace("(", "").replace(")", "").replace(",", "")
            if line:
                x, y = map(float, line.split())
                points.append((x, y))

    return points



def do_split():
    #separation en deux listes differentes
    x_pts,y_pts  = [],[]
    for c in pts:
        x,y = c 
        x_pts.append(x)
        y_pts.append(y)
    return  x_pts,y_pts


def do_Fourier():
    #tracé des points d'origine (1)
    plt.figure(1)
    plt.scatter(x_pts, y_pts, color = "red", s=10)
    
    #definition de fonctions de Fourrier
    def coeff_de_fourrier(p):
        return (1/N)*sum(pts_complexes[k]*np.exp( 1j*(-1)*p*2*k*np.pi/N) for k in range(-N//2,N//2))

    def point_de_fourrier(t):
        return sum(coeff_de_fourrier(p)*np.exp(1j*p*t) for p in ens_points_TF)

    #execution des fonctions
    TF = []
    for i in points_random_TF:
        TF.append(point_de_fourrier(i))
    #affichage des complexes dans R²
    x_TF = [i.real for i in TF]
    y_TF = [i.imag for i in TF]
    plt.title("transformée de fourrier")
    plt.plot(x_TF,y_TF)





def f_bezier(pts_b):
        #fonctions de Bezier
        def pt_bezier(t,pts_b):
            nbre_pts = len(pts_b) -1
            return  sum(   math.comb(nbre_pts, k)*( (1-t)**(nbre_pts-k) )*( t**(k) )*pts_b[k]     for k in range(nbre_pts+1))
        #execution des fonctions de bezier
        bezier = []

        for i in points_random_Bezier:
            bezier.append(pt_bezier(i,pts_b))
        return bezier

def do_Bezier_1():
    #tracé des points d'origine (2)
    plt.figure(2)
    plt.scatter(x_pts, y_pts, color = "red", s=10)
    plt.plot(x_pts,y_pts,color = "red")



    def inf_d(pts_b,P):
        temp = []
        for x in range(len(pts_b)):
            temp.append(abs(P-pts_b[x]))
            indice = x
        return [min(temp),indice] 

         
    

    bezier = f_bezier(pts_complexes)

    def point_loin(L,pts_a):
        max = L[0]
        inf = inf_d(pts_a,max)[0]
        for i in range(len(L)):
            if inf < inf_d(pts_a, L[i])[0]: 
                indice_pt_proche_max = inf_d(pts_a,L[i])[1]
                max = L[i]
                inf = inf_d(pts_a,max)[0]
        return [max, indice_pt_proche_max]
    
    for i in range(n_pts_conservees_b):
        bezier = f_bezier([pts_complexes[i] for i in range(point_loin(bezier,pts_complexes)[1])]) + f_bezier([pts_complexes[i] for i in range(point_loin(bezier,pts_complexes)[1],len(pts_complexes)-1)])



    #affichage des complexes dans R² 
    x_bezier = [i.real for i in bezier]
    y_bezier = [i.imag for i in bezier]

    plt.title("Courbe de Bézier")
    plt.plot(x_bezier,y_bezier)
    

def do_TFD():
    #tracé des points d'origine (3)
    plt.figure(3)
    plt.scatter(x_pts, y_pts, color = "red")

    #definition de fonctions de TFD
    def TFD(points_complexes,k):
        N = len(points_complexes)
        return sum(points_complexes[n]*np.exp(-1j*2*np.pi*(k/N)*n) for n in range(N))

    def TFD_inv(pts_TFD,n):
        N = len(pts_TFD)
        return (1/N)*sum(pts_TFD[k]*np.exp(1j*2*np.pi*(k/N)*n) for k in range(N))

    #transforme pts en coeff TFD
    coeff_TFD = []
    for i in range(N):
        coeff_TFD.append(TFD(pts_complexes,i))
    #choix des points a garder
    
    S_coeff_TFD = sorted([float(abs(x)) for x in coeff_TFD],reverse = True)
    coeff_a_garder = [S_coeff_TFD[i] for i in range(int(N*taux_TFD))]

    coeff_TFD2 = []
    for i in range(N):
        if float(abs(coeff_TFD[i])) in coeff_a_garder:
            coeff_TFD2.append(coeff_TFD[i])
        else : coeff_TFD2.append(0)


    #retour aux vrais pts
    liste_final = []
    for i in range(len(coeff_TFD)):
        liste_final.append(TFD_inv(coeff_TFD2,i))


    #affichage des complexes dans R²
    x_TFD = [i.real for i in liste_final]
    y_TFD = [i.imag for i in liste_final]
    plt.title("TFD")
    plt.plot(x_TFD,y_TFD)


#Liste = ["uniforme100_chat.txt","uniforme100_dauphin.txt","uniforme100_Grand_I.txt","uniforme_guitare1.txt","uniforme100_montagne.txt","uniforme100_papillon.txt"]

#DONNEES
pts = read_click_coords("uniforme100_chat.txt")
N = len(pts)
pts_complexes = [pts[i][0] + 1j*pts[i][1] for i in range(N)]

#donnees TF
ens_points_TF = range(-10,10)
points_random_TF = np.linspace(0,2*np.pi,len(pts)*5) #grand nombre de points pour s'approcher visuellement de la courbe de notre fonction

#RAPPORT BEZIER
points_random_Bezier = np.linspace(0,1,len(pts)*2)
n_pts_conservees_b = 50

#RAPPORT TFD
taux_TFD = 0.1
points_random_TFD = np.linspace(0,2*np.pi,len(pts)*5) #grand nombre de points pour s'approcher visuellement de la courbe de notre fonction

x_pts,y_pts = do_split()

#do_TFD()
#do_Bezier_1()
#do_Fourier()
#plt.show()

def approx_integr(f,L):
    return sum( f(x) for x in L)*(L[-1]- L[0])/(len(L)-1)

def norme1(f,L) :
    def abs_f(x) : return float(abs(f(x)))
    return approx_integr(abs_f,L)

def norme2(f,L):
    def f_abs_carre(x) : return float(abs(f(x))**2)
    return math.sqrt(approx_integr(f_abs_carre,L))

def norme_inf(f, L):
    return max(abs(f(x)) for x in L)

def f_moins_g(f, g):
    return lambda x: f(x) - g(x)

def normes(f,L):
    print("N1(f) =", norme1(f,L), "N2(f) =", norme2(f,L), "N_inf(f) =", norme_inf(f,L))





"""
A=np.array(sch.complex_fitcurve_perso(pts_complexes,20))
print(A, len(A)*2+2)
courbe = []

for i in range(len(A)):
    courbe=[]
    for t in np.linspace(0,1,10):
        courbe.append(sch.bezier(A[i],0,t))
        plt.plot([i[0] for i in courbe],[i[1] for i in courbe],color = "blue")

plt.scatter(x_pts, y_pts, color = "red")
plt.show()"""
