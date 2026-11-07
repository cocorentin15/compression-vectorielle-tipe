import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat

# Dossier racine contenant tous les sous-dossiers
base_path = "C:/Users/CORENTIN/Desktop/a-large-scale-12-lead-electrocardiogram-database-for-arrhythmia-study-1.0.0/a-large-scale-12-lead-electrocardiogram-database-for-arrhythmia-study-1.0.0/WFDBRecords"

# Liste pour stocker toutes les dérivations 10
lead10_matrix = []
"""
i=1
# Parcours récursif
for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith(".mat"):
            print(i)
            i+=1
            mat_path = os.path.join(root, file)
            try:
                data = loadmat(mat_path)
                val = data['val']  # (12, N)
                lead10 = val[9]  # 10e dérivation (index 9)
                lead10_matrix.append(lead10.tolist())  # Conversion en liste Python
            except Exception as e:
                print(f"Erreur avec {mat_path} : {e}")

# Sauvegarde dans un fichier texte
output_path = os.path.join(base_path, "lead10_matrix.txt")
with open(output_path, "w") as f:
    for row in lead10_matrix:
        f.write(",".join(map(str, row)) + "\n")

print(f"✅ Sauvegarde terminée : {output_path}")"""