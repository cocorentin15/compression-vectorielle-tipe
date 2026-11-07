import lire_coords

def symetrie_horizontale(file_name):
    x_pts, y_pts = lire_coords.lire_coords(file_name)

    max_x = max(x_pts)
    x_center = max_x // 2

    x_pts2 = [x + 2 * (x_center - x) for x in x_pts]

    with open(file_name, "w") as fichier:
        fichier.write(f"[[{','.join(map(str, x_pts2))}],[{','.join(map(str, y_pts))}]]\n")


def symetrie_verticale(file_name):
    x_pts, y_pts = lire_coords.lire_coords(file_name)

    max_y = max(y_pts)
    y_center = max_y // 2

    y_pts2 = [y + 2 * (y_center - y) for y in y_pts]

    with open(file_name, "w") as fichier:
        fichier.write(f"[[{','.join(map(str, x_pts))}],[{','.join(map(str, y_pts2))}]]\n")


symetrie_verticale("twitter.txt")
