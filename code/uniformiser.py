import numpy as np
import matplotlib.pyplot as plt

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


def uniform_points(x, y, num_points):
    """
    Génère des points uniformément espacés à partir d'un contour défini par (x, y).
    Fonctionne pour des formes fermées ou ouvertes.
    """
    # Convertir les coordonnées en distances cumulées
    points = np.column_stack((x, y))
    distances = np.sqrt(np.sum(np.diff(points, axis=0)**2, axis=1))
    cumulative_distances = np.insert(np.cumsum(distances), 0, 0)
    
    # Distance totale
    total_distance = cumulative_distances[-1]
    
    # Créer des distances uniformes
    uniform_distances = np.linspace(0, total_distance, num_points)
    
    # Interpolation pour les nouvelles coordonnées
    x_interp = np.interp(uniform_distances, cumulative_distances, x)
    y_interp = np.interp(uniform_distances, cumulative_distances, y)
    
    return x_interp, y_interp




file_name = "Grand_I.txt"

pts = read_click_coords(file_name)
    #separation en deux listes differentes
N = len(pts)
x_pts = []
y_pts = []
for c in pts:
    x,y = c 
    x_pts.append(x)
    y_pts.append(y)
# Générer des points uniformément espacés

num_points = 100
x_uniform, y_uniform = uniform_points(x_pts, y_pts, num_points)

# 1=Afficher le résultat, 0=l'écrire
ne_pas_modif = 0

if ne_pas_modif == 1:
    plt.figure(figsize=(8, 8))
    plt.scatter(x_pts, y_pts, label="Points originaux", color="blue")
    plt.scatter(x_uniform, y_uniform,color = "red") 
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis("equal")
    plt.show()

if ne_pas_modif == 0:
    with open("uniforme100_" + file_name, "w") as file:
         for x, y in zip(x_uniform, y_uniform):
            file.write(f"({x}, {y})\n")
