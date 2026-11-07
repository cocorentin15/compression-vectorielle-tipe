from __future__ import print_function
from numpy import *
import matplotlib.pyplot as plt

# Active le mode interactif de matplotlib
plt.ion()

# Durée d'attente par défaut (non utilisée ici, on attend l'appui sur 'y')
# PAUSE_TIME = 1.0

# Fonction d'affichage d'une étape qui attend que l'utilisateur appuie sur "y"
def plot_fit(points, bezCurve, parameters=None, error=None, splitPoint=None, splitU=None, iteration=None, extra_title=""):
    plt.clf()
    pts = array(points)
    # Affiche les points d'origine
    plt.plot(pts_origine[:, 0], pts_origine[:, 1], 'ko-', label='Points')
    # Trace la courbe de Bézier calculée
    t = linspace(0, 1, 100)
    bezier_points = array([q(bezCurve, ti) for ti in t])
    plt.plot(bezier_points[:, 0], bezier_points[:, 1], 'r-', label='Bézier')
    # Trace le polygone de contrôle
    ctrl_poly = array(bezCurve)
    plt.plot(ctrl_poly[:, 0], ctrl_poly[:, 1], 'b--', label='Polygone de contrôle')
    
    # Si un point de séparation est fourni, on le marque
    if splitPoint is not None and splitPoint < len(points):
        plt.scatter(points[splitPoint][0], points[splitPoint][1], color='m', s=100, label='Point de séparation')
        # Trace une ligne entre le point d'erreur et la position correspondante sur la courbe
        if splitU is not None:
            bez_split = q(bezCurve, splitU)
            plt.plot([points[splitPoint][0], bez_split[0]],
                     [points[splitPoint][1], bez_split[1]],
                     'g--', lw=2, label='Erreur max')
    
    # Titre détaillé de la figure
    title = extra_title
    if error is not None:
        title += " | Erreur = {:.4f}".format(error)
    if iteration is not None:
        title += " | Itération = {}".format(iteration)
    plt.title(title)
    #plt.legend()
    plt.draw()
    
    # Attendre que l'utilisateur appuie sur "y"
    rep = input("Appuyez sur 'y' pour continuer : ")
    while rep.strip().lower() != "y":
        rep = input("Appuyez sur 'y' pour continuer : ")

# Évalue la courbe de Bézier cubique en t et retourne le point
def q(ctrlPoly, t):
    point = (1.0-t)**3 * ctrlPoly[0] + 3*(1.0-t)**2 * t * ctrlPoly[1] + 3*(1.0-t)* t**2 * ctrlPoly[2] + t**3 * ctrlPoly[3]
    return point

# Évalue la dérivée première de la courbe de Bézier cubique en t
def qprime(ctrlPoly, t):
    return 3*(1.0-t)**2 * (ctrlPoly[1]-ctrlPoly[0]) + 6*(1.0-t)*t*(ctrlPoly[2]-ctrlPoly[1]) + 3*t**2*(ctrlPoly[3]-ctrlPoly[2])

# Évalue la dérivée seconde de la courbe de Bézier cubique en t
def qprimeprime(ctrlPoly, t):
    return 6*(1.0-t)*(ctrlPoly[2]-2*ctrlPoly[1]+ctrlPoly[0]) + 6*t*(ctrlPoly[3]-2*ctrlPoly[2]+ctrlPoly[1])

# Ajuste une (ou plusieurs) courbe(s) de Bézier aux points donnés
def fitCurve(points, maxError):
    print("fitCurve: Ajustement sur {} points avec maxError = {}".format(len(points), maxError))
    leftTangent = normalize(points[1] - points[0])
    rightTangent = normalize(points[-2] - points[-1])
    return fitCubic(points, leftTangent, rightTangent, maxError)

def fitCubic(points, leftTangent, rightTangent, error):
    print("\nfitCubic: Ajustement sur {} points".format(len(points)))
    # Affichage initial des points
    plot_fit(points, [points[0], points[0], points[-1], points[-1]], extra_title="Points initiaux")
    
    # Cas particulier : si seulement deux points
    if len(points) == 2:
        dist = linalg.norm(points[0] - points[1]) / 3.0
        bezCurve = [points[0], points[0] + leftTangent * dist, points[1] + rightTangent * dist, points[1]]
        print("fitCubic: Seulement 2 points -> contrôle simple:", bezCurve)
        plot_fit(points, bezCurve, extra_title="Cas 2 points")
        return [bezCurve]

    # Paramétrisation par longueur de chord
    u = chordLengthParameterize(points)
    print("fitCubic: Paramétrisation (u) =", u)
    # Génération de la courbe de Bézier
    bezCurve = generateBezier(points, u, leftTangent, rightTangent)
    print("fitCubic: Courbe de Bézier générée =", bezCurve)
    plot_fit(points, bezCurve, extra_title="Génération initiale")
    
    # Calcul de l'erreur maximale, on récupère aussi le paramètre associé au point d'erreur
    maxError, splitPoint, splitU = computeMaxError(points, bezCurve, u)
    print("fitCubic: Erreur max =", maxError, "au point index =", splitPoint, "avec paramètre =", splitU)
    plot_fit(points, bezCurve, error=maxError, splitPoint=splitPoint, splitU=splitU, extra_title="Erreur maximale")
    
    if maxError < error:
        print("fitCubic: Erreur acceptable. Retour de la courbe.")
        return [bezCurve]

    # Tentative de reparamétrisation si l'erreur est modérée
    if maxError < error**2:
        print("fitCubic: Tentative de reparamétrisation...")
        for i in range(20):
            uPrime = reparameterize(bezCurve, points, u)
            bezCurve = generateBezier(points, uPrime, leftTangent, rightTangent)
            maxError, splitPoint, splitU = computeMaxError(points, bezCurve, uPrime)
            print("fitCubic: Itération", i, "-> erreur =", maxError)
            plot_fit(points, bezCurve, error=maxError, splitPoint=splitPoint, splitU=splitU,
                     iteration=i, extra_title="Reparamétrisation")
            if maxError < error:
                print("fitCubic: Erreur acceptable après reparamétrisation.")
                return [bezCurve]
            u = uPrime

    # Subdivision en cas d'erreur trop importante
    print("fitCubic: Erreur trop importante, subdivision en deux segments...")
    centerTangent = normalize(points[splitPoint-1] - points[splitPoint+1])
    plot_fit(points, bezCurve, error=maxError, splitPoint=splitPoint, splitU=splitU, extra_title="Subdivision")
    beziers = []
    beziers += fitCubic(points[:splitPoint+1], leftTangent, centerTangent, error)
    beziers += fitCubic(points[splitPoint:], -centerTangent, rightTangent, error)
    return beziers

def generateBezier(points, parameters, leftTangent, rightTangent):
    print("\ngenerateBezier: Génération de la courbe de Bézier pour {} points".format(len(points)))
    bezCurve = [points[0], None, None, points[-1]]
    A = zeros((len(parameters), 2, 2))
    for i, u in enumerate(parameters):
        A[i][0] = leftTangent  * 3*(1-u)**2 * u
        A[i][1] = rightTangent * 3*(1-u)    * u**2
        print("generateBezier: A[{}] =".format(i), A[i])
    
    C = zeros((2, 2))
    X = zeros(2)
    for i, (point, u) in enumerate(zip(points, parameters)):
        C[0][0] += dot(A[i][0], A[i][0])
        C[0][1] += dot(A[i][0], A[i][1])
        C[1][0] += dot(A[i][0], A[i][1])
        C[1][1] += dot(A[i][1], A[i][1])
        tmp = point - q([points[0], points[0], points[-1], points[-1]], u)
        X[0] += dot(A[i][0], tmp)
        X[1] += dot(A[i][1], tmp)

    det_C0_C1 = C[0][0] * C[1][1] - C[1][0] * C[0][1]
    det_C0_X  = C[0][0] * X[1] - C[1][0] * X[0]
    det_X_C1  = X[0] * C[1][1] - X[1] * C[0][1]

    alpha_l = 0.0 if det_C0_C1 == 0 else det_X_C1 / det_C0_C1
    alpha_r = 0.0 if det_C0_C1 == 0 else det_C0_X / det_C0_C1

    segLength = linalg.norm(points[0] - points[-1])
    epsilon = 1.0e-6 * segLength
    if alpha_l < epsilon or alpha_r < epsilon:
        bezCurve[1] = points[0] + leftTangent * (segLength / 3.0)
        bezCurve[2] = points[-1] + rightTangent * (segLength / 3.0)
        print("generateBezier: Heuristique appliquée, alpha insuffisants.")
    else:
        bezCurve[1] = points[0] + leftTangent * alpha_l
        bezCurve[2] = points[-1] + rightTangent * alpha_r

    print("generateBezier: Courbe générée =", bezCurve)
    return bezCurve

def reparameterize(bezier, points, parameters):
    return [newtonRaphsonRootFind(bezier, point, u) for point, u in zip(points, parameters)]

def newtonRaphsonRootFind(bez, point, u):
    d = q(bez, u) - point
    numerator = (d * qprime(bez, u)).sum()
    denominator = (qprime(bez, u)**2 + d * qprimeprime(bez, u)).sum()
    if denominator == 0.0:
        return u
    else:
        return u - numerator/denominator

def chordLengthParameterize(points):
    u = [0.0]
    for i in range(1, len(points)):
        u.append(u[i-1] + linalg.norm(points[i] - points[i-1]))
    u = [ui / u[-1] for ui in u]
    return u

def computeMaxError(points, bez, parameters):
    maxDist = 0.0
    splitPoint = int(len(points)/2)
    splitU = parameters[splitPoint]  # paramètre par défaut
    for i, (point, u) in enumerate(zip(points, parameters)):
        dist = linalg.norm(q(bez, u) - point)**2
        if dist > maxDist:
            maxDist = dist
            splitPoint = i
            splitU = u
    return maxDist, splitPoint, splitU

def normalize(v):
    norm_val = linalg.norm(v)
    if norm_val == 0:
        return v
    return v / norm_val


# Exemple d'utilisation
if __name__ == "__main__":
    # Définition de quelques points à ajuster (exemple)
    x,y = [0.9835209334493186, 1.4206327654253694, 1.5020820485315856, 2.00408594528103, 2.6830460402989345, 2.638215682500323, 2.4588023336232965, 3.2690819916510447, 3.6968415137802926, 4.278976662100807, 5.068459569669932, 5.841728196437489, 6.522342744803566, 6.967417253924184, 7.373450392420089, 7.675824729934294, 8.253326471879733, 9.077139287154623, 9.962089624776668, 10.92508651761736, 11.85158540842202, 12.540559189167402, 13.13335522423984, 13.615827496248514, 14.114626810619129, 14.353513127107815, 14.507733693832844, 14.608687505217855, 14.542168494694081, 14.613840975688673, 14.6825625064934, 14.54205951600064, 14.887191797223592, 15.835912903842544, 16.834317656849034, 17.811273802792748, 18.78835363487316, 19.603701242670073, 19.953196856928137, 19.937685398480237, 19.44170758788109, 18.938830454777918, 18.52878444889383, 18.294021696938636, 18.054634278319636, 18.143144048675204, 18.428696546025396, 19.042329921938496, 19.837076055154593, 20.80416158434675, 21.78649279402166, 22.361514822171664, 22.059177479515306, 21.146188314588056, 20.288923474827996, 19.881173154725513, 19.730797511898043, 19.86550056830844, 20.393368337358922, 20.801776496200688, 21.24099379740707, 21.57906299943742, 21.84821502162415, 21.6171806835242, 21.1027328426166, 20.39562606143006, 19.60594569448957, 18.618947891940813, 17.623910701730818, 16.624565510707512, 15.62456551070751, 14.624565510707514, 13.624565510707509, 12.624565510707516, 11.624565510707518, 10.62456551070752, 9.625654437414914, 8.627448035223356, 7.628659822145999, 6.629930235506424, 5.632163659106084, 4.632163659106085, 4.013241716371545, 4.6178099896474, 4.915787474955653, 5.090157984362123, 5.2087639537479005, 5.339113638724872, 5.2990906281465655, 5.056555003110231, 4.826688690354742, 4.5478689408677555, 4.353614359205163, 4.049732113490669, 3.9660962704074496, 3.876112111994891, 3.3112713005614416, 2.393538486012409, 1.5101674448497042, 0.9132694382029487],[15.033819982725298, 15.868997872426561, 16.857108984778815, 17.714556152442537, 18.438301733591327, 19.397514034909754, 20.367843028486824, 19.80526036829187, 19.941065553901147, 19.83007567027282, 19.238557785577513, 18.605792149302715, 17.896753792621997, 17.006427843563856, 16.095476700620463, 15.150459413852161, 14.355538341723562, 13.788903423130613, 13.389899360723343, 13.164738606449479, 12.806689423057325, 12.091538153516698, 11.303054331917648, 10.429419209682361, 9.566050821314128, 8.600144926319526, 7.613488054222889, 6.619539457968635, 5.621754300112023, 4.624358970727842, 3.628637418495371, 2.648315557050629, 1.829601473910351, 1.5868351162149752, 1.551848651558106, 1.7569593165822825, 1.9614637110191149, 2.465870471483456, 3.393338255301185, 4.36907275046919, 5.2368640831283875, 6.099775114677982, 7.011213039201998, 7.977375851300884, 8.946782280472156, 9.930732398281943, 10.872553821656446, 11.62210213985296, 12.194951864799519, 12.419983103156524, 12.264205216489152, 11.532512207961936, 10.748478772696124, 11.09941075197622, 10.650709974698158, 9.879331489201892, 8.89346486818951, 7.948283115259208, 7.113295714924612, 6.216742739725287, 5.339246881570295, 4.398184963324757, 3.4459670972905587, 2.480707182508645, 1.6430686593693693, 0.9359618781828265, 0.339535117232481, 0.18288405280560158, 0.08338033378460209, 0.0702514952463799, 0.0702514952463799, 0.0702514952463799, 0.0702514952463799, 0.0702514952463799, 0.0702514952463799, 0.0702514952463799, 0.0375474367087938, 0.021749742577982543, 0.0702514952463799, 0.09572312511026056, 0.1405029904927598, 0.1405029904927598, 0.6401695411685646, 1.1240239239420784, 1.8877044101975606, 2.871733100409608, 3.864653881915027, 4.8553902150263495, 5.85046315727, 6.820605657415339, 7.793793399150038, 8.753676849717062, 9.727554972667917, 10.670622015257242, 11.667094206445064, 12.662973400401176, 13.451813631650111, 13.76929306829046, 14.167704478616564, 14.963568487478907]
    points_chat = [[x[i],y[i]] for i in range(len(x))]
    pts_origine = array(points_chat)
    max_error = 2.0

    # Exécute l'algorithme et récupère la liste des courbes de Bézier obtenues
    beziers = fitCurve(pts_origine, max_error)
    
    # Affichage final : on trace toutes les courbes obtenues
    plt.clf()
    plt.plot(pts_origine[:,0], pts_origine[:,1], 'ko-', label='Points')
    for bez in beziers:
        t = linspace(0,1,100)
        bezier_points = array([q(bez, ti) for ti in t])
        plt.plot(bezier_points[:,0], bezier_points[:,1], 'r-', lw=2, label='Bezier')
        ctrl_poly = array(bez)
        plt.plot(ctrl_poly[:,0], ctrl_poly[:,1], 'b--', lw=1, label='Contrôle')
    plt.title("Ajustement final")
    plt.legend()
    plt.draw()
    plt.pause(5)
    plt.ioff()
    plt.show()
