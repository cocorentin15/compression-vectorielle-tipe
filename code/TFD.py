import numpy as np


def TFD(complex_points, n_points):
    N = len(complex_points)

    # Definition de la fonction de Transformation de Fourier Discrète (TFD)
    def TFD(points_complexes, k):
        N = len(points_complexes)
        return sum(points_complexes[n] * np.exp(-1 * 1j *2* np.pi * (k / N) * n) for n in range(N))

    # Definition de la fonction inverse de la TFD
    def TFD_inv(pts_TFD, k):
        N = len(pts_TFD)
        return (1 / N) * sum(pts_TFD[n] * np.exp(1j * 2 * np.pi * (k / N) * n) for n in range(N))

    # Transformation des points en coefficients TFD
    coeff_TFD = []
    for i in range(N):
        coeff_TFD.append(TFD(complex_points, i))

    # Choix des points à garder en fonction du taux_TFD
    coeff_a_garder = sorted(coeff_TFD, key=lambda x: abs(x), reverse=True)[:int(n_points)]

    # Filtrage des coefficients TFD en gardant seulement ceux sélectionnés
    coeff_TFD2 = [x if x in coeff_a_garder else 0 for x in coeff_TFD]


    # Retour aux points d'origine en utilisant l'inverse de la TFD
    liste_final = []
    for i,_ in enumerate(coeff_TFD2):
        liste_final.append(TFD_inv(coeff_TFD2, i))

    # Extraction des parties réelles et imaginaires des points transformés
    x_TFD = [i.real for i in liste_final]
    y_TFD = [i.imag for i in liste_final]
    return x_TFD, y_TFD


def TFD_reparametre(complex_points, taux_TFD, num_points):

    x,y= TFD(complex_points, taux_TFD)
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