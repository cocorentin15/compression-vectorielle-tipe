import lire_coords as lc
import matplotlib.pyplot as plt

#couleur = ['#1f77b4','#1f77b4','#1f77b4']
couleur = ['#050396', '#ba7104', '#c72816' ]
Liste = ["dauphin.txt","guitare.txt","chat.txt"]
Liste_uniforme = ["carre.txt","final_dauphin.txt","final_guitare.txt"]
for k,mot in enumerate(Liste_uniforme):
    x,y = lc.lire_coords(mot)
    plt.figure(k)
    plt.scatter(x,y, color = couleur[k])
    plt.title(mot)
plt.show()

    
