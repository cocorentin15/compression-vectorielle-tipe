import lire_coords
import matplotlib.pyplot as plt

def split_complepts_x(pts):
    #separation en deux listes differentes, passage de [x1+j*y1,x2+j*y2] à [x1,x2],[y1,y2]

    x = [i.real for i in pts]
    y = [i.imag for i in pts]
    return x,y


def reparametre(x,y, num_points):

    # Calculate cumulative distances
    distances = []
    distances_cumulees = [0]
    for i in range(1, len(x)):
        dx = x[i] - x[i - 1]
        dy = y[i] - y[i - 1]
        distance = (dx**2 + dy**2)**0.5  # Distance euclidienne
        distances.append(distance)
        distances_cumulees.append(distances_cumulees[-1] + distance)
    
    total_distance = distances_cumulees[-1]
    
    uniform_distances = [(total_distance * i) / (num_points - 1) for i in range(num_points)]
    # Interpolation for new coordinates
    def interpolate(new_distance, distances_cumulees, coordinates):
        for i in range(1, len(distances_cumulees)):
            if distances_cumulees[i] >= new_distance:
                # Linear interpolation
                t = ((new_distance - distances_cumulees[i - 1]) /
                     (distances_cumulees[i] - distances_cumulees[i - 1]))
                return coordinates[i - 1] + t * (coordinates[i] - coordinates[i - 1])
        return coordinates[-1]  # Edge case for the last point

    x_interp = [interpolate(d, distances_cumulees, x) for d in uniform_distances]
    y_interp = [interpolate(d, distances_cumulees, y) for d in uniform_distances]
    
    return x_interp, y_interp



def reparametre_pas_et_nombre_points_scalable(x, y, num_points, pas):
    # Étape 1 : Calcul des distances cumulées de la courbe d'origine
    distances_cumulees = [0]
    for i in range(1, len(x)):
        dx = x[i] - x[i - 1]
        dy = y[i] - y[i - 1]
        distance = (dx**2 + dy**2)**0.5
        distances_cumulees.append(distances_cumulees[-1] + distance)
    total_distance = distances_cumulees[-1]
    
    # Étape 2 : Définir la distance totale cible selon le pas choisi
    nouvelle_distance_totale = (num_points - 1) * pas
    facteur = nouvelle_distance_totale / total_distance  # Facteur d'échelle

    # Étape 3 : Mettre à l'échelle les coordonnées originales
    x_scaled = [xi * facteur for xi in x]
    y_scaled = [yi * facteur for yi in y]
    
    # On applique le même facteur aux distances cumulées
    distances_cumulees = [d * facteur for d in distances_cumulees]
    
    # Étape 4 : Génération des nouvelles distances équidistantes
    uniform_distances = [i * pas for i in range(num_points)]
    
    # Étape 5 : Interpolation linéaire sur la courbe mise à l'échelle
    def interpolate(new_distance, distances_cumulees, coordinates):
        for i in range(1, len(distances_cumulees)):
            if distances_cumulees[i] >= new_distance:
                t = ((new_distance - distances_cumulees[i - 1]) /
                     (distances_cumulees[i] - distances_cumulees[i - 1]))
                return coordinates[i - 1] + t * (coordinates[i] - coordinates[i - 1])
        return coordinates[-1]
    
    x_interp = [interpolate(d, distances_cumulees, x_scaled) for d in uniform_distances]
    y_interp = [interpolate(d, distances_cumulees, y_scaled) for d in uniform_distances]
    
    return x_interp, y_interp



file_name = "points.txt"

pts_x,pts_y = lire_coords.lire_coords(file_name)
    #separation en deux listes differentes
N = len(pts_x)

x_interp, y_interp = reparametre_pas_et_nombre_points_scalable(pts_x, pts_y, 100,1)

creer_txt = 1

if creer_txt ==0:
    plt.figure(figsize=(8, 8))
    plt.scatter(pts_x, pts_y, label="Points originaux", marker = "+" ,color="blue", s = 200)
    plt.scatter(x_interp, y_interp,color = "red") 
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis("equal")
    plt.show()

elif creer_txt == 1:
    with open("final_" + file_name, "w") as file:
        file.write(f"[{x_interp},{y_interp}]\n")
