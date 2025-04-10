import matplotlib
matplotlib.use('Qt5Agg')  # Utiliser le backend Qt5
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import os

# Configuration
FICHIER_DONNEES = "mesures_reelles.txt"
NOMBRE_POINTS = 50  # Nombre de points à afficher

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

def initialiser_graphique():
    """Configure les paramètres de base du graphique"""
    ax.set_title("Évolution du Volume de Données")
    ax.set_ylabel("Volume (octets)")
    ax.set_xlabel("Temps")
    plt.xticks(rotation=45)
    plt.tight_layout()

def lire_et_trier_donnees():
    """Lit et traite les données du fichier"""
    if not os.path.exists(FICHIER_DONNEES):
        return [], []

    with open(FICHIER_DONNEES, "r") as f:
        lignes = f.readlines()

    x = []
    y = []
    for ligne in lignes:
        try:
            temps, volume = ligne.strip().split(',')
            dt = datetime.strptime(temps, "%Y-%m-%d %H:%M:%S")
            x.append(dt)
            y.append(float(volume))
        except (ValueError, IndexError):
            continue

    return x, y

def mettre_a_jour_graphique(i):
    """Fonction d'animation pour la mise à jour du graphique"""
    x, y = lire_et_trier_donnees()

    ax.clear()
    initialiser_graphique()

    if len(x) > 0:
        # Afficher seulement les N derniers points
        x_affichage = x[-NOMBRE_POINTS:]
        y_affichage = y[-NOMBRE_POINTS:]

        ax.plot(x_affichage, y_affichage, 'b-', marker='o', markersize=4)
        ax.fill_between(x_affichage, y_affichage, alpha=0.2)

        # Mise à jour des limites de l'axe Y
        y_min = min(y_affichage) * 0.9 if min(y_affichage) > 0 else 0
        y_max = max(y_affichage) * 1.1
        ax.set_ylim(y_min, y_max)

initialiser_graphique()
ani = animation.FuncAnimation(fig, mettre_a_jour_graphique, interval=1000, cache_frame_data=False)

plt.show()