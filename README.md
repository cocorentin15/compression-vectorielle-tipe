# TIPE — Compression vectorielle de contours

Projet Python qui compare deux façons de représenter un contour fermé avec peu de
données : l'ajustement de courbes de Bézier (algorithme de Schneider) et les
descripteurs de Fourier (TFD). L'écart avec le contour d'origine est mesuré pour
comparer les méthodes.

## Fonctionnement

1. Un contour est extrait d'une image, ou cliqué à la main, puis stocké dans un
   fichier `.txt` de points `(x, y)`.
2. Les points sont convertis en nombres complexes `x + i*y` et éventuellement
   rééchantillonnés à distance constante.
3. Deux méthodes approximent le contour :
   - **Schneider** : découpe le tracé en courbes de Bézier cubiques ;
   - **TFD / Fourier** : ne garde que les coefficients de Fourier les plus
     significatifs, puis reconstruit la courbe.
4. `mesurer_difference.distance_simple` calcule l'erreur moyenne entre les points
   d'origine et les points reconstruits.

## Fichiers importants

| Fichier | Rôle |
| --- | --- |
| `code/TIPE 2.py` | Script principal : lance les méthodes et affiche les courbes |
| `code/schneider.py` | Ajustement de Bézier (algorithme de Schneider) |
| `code/TFD.py` | Transformée de Fourier discrète et reconstruction |
| `code/fourier.py` | Version avec série de Fourier |
| `code/reparametrer.py` | Rééchantillonnage régulier d'un contour |
| `code/mesurer_difference.py` | Calcul de l'erreur entre deux contours |
| `code/uniformiser.py` | Passage à un nombre fixe de points |
| `code/extraire image.py` | Extraction automatique du contour d'une image |
| `code/faire les points.py` | Sélection manuelle des points au clic |
| `code/final_*.txt` | Contours déjà préparés (chat, dauphin, guitare…) |

## Lancer le projet

```sh
cd code
python "TIPE 2.py"
```

Dépendances : `numpy`, `matplotlib`, `scipy` et `opencv-python` (uniquement pour
les scripts d'extraction d'image).

La fin de `TIPE 2.py` lit `lead10_matrix.txt`, un fichier de données non fourni
dans le dépôt. Pour tester rapidement, utiliser le bloc commenté juste au-dessus :
il charge par exemple `final_dauphin.txt` et appelle `start_Schneider()`,
`start_Fourier()` ou `start_TFD()`.

## Note

Seul ce README a été rédigé par une IA. Le code, les données et le projet ont été
réalisés par son auteur.
