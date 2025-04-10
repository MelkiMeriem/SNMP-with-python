import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

# Variables globales pour garder le suivi entre les appels
previous_volume = None
previous_time = None

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

def calculate_transfer_rate(current_volume, current_time):
    """Calcule le débit en octets/seconde"""
    global previous_volume, previous_time

    if previous_volume is None or previous_time is None:
        return None

    time_diff = (current_time - previous_time).total_seconds()
    if time_diff == 0:  # Éviter la division par zéro
        return None

    return (current_volume - previous_volume) / time_diff

def animate(i):
    global previous_volume, previous_time

    try:
        with open("mesures.txt", "r") as f:
            lines = f.readlines()

        # Traitement de la dernière ligne seulement
        if lines:
            last_line = lines[-1].strip()

            if ',' in last_line:
                timestamp_str, volume_str = last_line.split(',')
                current_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                current_volume = float(volume_str)

                # Calcul du débit
                debit = calculate_transfer_rate(current_volume, current_time)

                if debit is not None:
                    # Enregistrement du débit dans debit.txt
                    with open("debit.txt", "a") as debit_file:
                        debit_file.write(f"{current_time.strftime('%Y-%m-%d %H:%M:%S')},{debit:.2f}\n")

                # Mise à jour des valeurs précédentes
                previous_volume = current_volume
                previous_time = current_time

        # Lecture des données pour le graphique
        with open("debit.txt", "r") as f:
            data = [line.strip().split(',') for line in f if line.strip()]

        xar = []
        yar = []
        for line in data[-50:]:  # Afficher les 50 dernières mesures
            try:
                dt = datetime.strptime(line[0], "%Y-%m-%d %H:%M:%S")
                xar.append(dt)
                yar.append(float(line[1]))
            except (ValueError, IndexError):
                continue

        if xar and yar:
            ax1.clear()
            ax1.plot(xar, yar, 'b-', marker='o')
            ax1.set_title("Débit réseau en temps réel")
            ax1.set_ylabel("Débit (octets/s)")
            ax1.set_xlabel("Temps")
            plt.xticks(rotation=45)
            fig.tight_layout()

    except FileNotFoundError:
        print("Fichier non trouvé")
    except Exception as e:
        print(f"Erreur: {str(e)}")

ani = animation.FuncAnimation(fig, animate, interval=1000, cache_frame_data=False)
plt.show()