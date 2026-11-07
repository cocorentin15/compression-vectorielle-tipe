import cv2

# Chemin de l'image de silhouette (à adapter)
image_path = 'Twitter.png'

# Chargement de l'image en niveaux de gris
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
if img is None:
    raise FileNotFoundError(f"L'image '{image_path}' n'a pas été trouvée.")

# Récupération de la hauteur de l'image pour la symétrie verticale
hauteur = img.shape[0]

# Seuillage pour obtenir une image binaire (adaptable selon l'image)
ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Extraction des contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
if not contours:
    raise ValueError("Aucun contour trouvé dans l'image.")

# Choisir le plus grand contour (supposé être la silhouette)
largest_contour = max(contours, key=cv2.contourArea)

# Initialisation des listes pour les coordonnées
x_points = []
y_points = []

# Parcours des points du contour, conversion en entiers standards et application de la symétrie verticale
for point in largest_contour:
    x, y = point[0]
    x_points.append(int(x))
    # Appliquer la symétrie verticale : inversion de y par rapport à la hauteur de l'image
    y_points.append(int(hauteur - 1 - y))

# Résultat sous forme de liste imbriquée
result = [x_points, y_points]

# Écriture du résultat dans un fichier texte
output_filename = "output_points.txt"
with open(output_filename, "w") as file:
    file.write(str(result))

print(f"Les points du contour ont été enregistrés dans '{output_filename}' avec une symétrie verticale appliquée.")
