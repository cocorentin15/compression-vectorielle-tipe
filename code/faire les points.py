import cv2
import numpy as np

# Listes pour stocker les coordonnées des clics
x_coords = []
y_coords = []

# Facteur de zoom initial
zoom_factor = 1.0

# Charger l'image (assure-toi que le chemin est correct)
image = cv2.imread('omega.jpg')  # Remplace 'M.jpg' par le chemin de ton image
if image is None:
    raise ValueError("Impossible de charger l'image. Vérifiez le chemin.")

# Dimensions originales de l'image
h, w = image.shape[:2]

def update_display():
    """Redimensionne et affiche l'image en fonction du zoom_factor."""
    global image, zoom_factor, w, h
    resized = cv2.resize(image, (int(w * zoom_factor), int(h * zoom_factor)))
    cv2.imshow("Image", resized)

def mouse_callback(event, x, y, flags, param):
    global x_coords, y_coords, zoom_factor, h
    if event == cv2.EVENT_LBUTTONDOWN:
        # Conversion des coordonnées du clic en coordonnées de l'image d'origine
        x_orig = int(x / zoom_factor)
        y_orig = int(y / zoom_factor)
        # Correction de la symétrie verticale : inversion par rapport à la hauteur de l'image
        y_orig_corrected = h - 1 - y_orig
        x_coords.append(x_orig)
        y_coords.append(y_orig_corrected)
        print(f"Coordonnées enregistrées : ({x_orig}, {y_orig_corrected})")
    elif event == cv2.EVENT_MOUSEWHEEL:
        # Gestion du zoom avec la molette
        if flags > 0:  # Zoom avant
            zoom_factor *= 1.1
        else:          # Zoom arrière
            zoom_factor /= 1.1
        zoom_factor = max(1.0, min(zoom_factor, 5.0))  # Limiter le zoom entre 1.0 et 5.0
        update_display()

# Création de la fenêtre et association de la fonction callback unique
cv2.namedWindow("Image", cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback("Image", mouse_callback)

update_display()
print("Cliquez sur l'image pour enregistrer les coordonnées.")
print("Utilisez la molette de la souris pour zoomer/dézoomer.")
print("Appuyez sur 'Échap' pour quitter.")

# Boucle principale
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Touche Échap pour quitter
        break

cv2.destroyAllWindows()

# Écriture des coordonnées dans un fichier texte sous la forme [x_coords, y_coords]
with open("points.txt", "w") as f:
    f.write(f"[{x_coords}, {y_coords}]")

print("Coordonnées finales enregistrées :")
print("X :", x_coords)
print("Y :", y_coords)
print("Les points ont été sauvegardés dans le fichier 'points.txt'")
