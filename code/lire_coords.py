def lire_coords(file_name):
    """Lire les coordonnées dans un fichier texte de la forme [[66, 67, 215, 216],[216, 66, 66, 214]]"""
    with open(file_name, 'r') as file:
        data = file.read()
        coords = eval(data)  # Use eval to convert string representation of list to actual list
    return coords[0],coords[1]
import csv


def csv_lire_coords(file_name):
    with open(file_name, newline='') as fichier:
        lecteur = csv.reader(fichier)
        x, y = [], []
        next(lecteur)  # Ignorer l'en-tête
        for ligne in lecteur:
            # Vérifier que la ligne contient au moins 5 colonnes et que les champs sont valides
            if len(ligne) > 4 and ligne[3] != '' and ligne[4] != '':
                try:
                    y.append(float(ligne[3]))
                    x.append(float(ligne[4]))
                except ValueError:
                    print("Valeur invalide ignorée :", ligne)
                    continue
                # Arrêter après 3000 points valides
                if len(x) >= 300:
                    break
    return x, y
