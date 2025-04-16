# snmpexp1.py (version corrigée)
from pysnmp.hlapi import *
import time
import signal
import sys

class TrafficMonitor:
    def __init__(self):
        self.running = True
        self.prev_octets = None
        self.prev_time = None

        # Gestion de l'interruption Ctrl+C
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        print("\nArrêt en cours...")
        self.running = False

    def calculate_rate(self, current_octets):
        if self.prev_octets is None:
            return 0.0

        delta_octets = current_octets - self.prev_octets
        delta_time = time.time() - self.prev_time

        # Gestion du wraparound des compteurs 32 bits
        if delta_octets < 0:
            delta_octets += 4294967296

        return delta_octets / delta_time if delta_time > 0 else 0.0

    def start_monitoring(self):
        print("Démarrage du monitoring (Ctrl+C pour arrêter)")

        while self.running:
            try:
                # Configuration SNMP
                error, status, index, var_binds = next(
                    getCmd(
                        SnmpEngine(),
                        CommunityData('com', mpModel=1),
                        UdpTransportTarget(('127.0.0.1', 161)),
                        ContextData(),
                        ObjectType(ObjectIdentity('.1.3.6.1.2.1.2.2.1.10.1'))
                    )
                )

                if error or status:
                    print("Erreur SNMP, réessai...")
                    time.sleep(2)
                    continue

                current_octets = int(var_binds[0][1])
                current_time = time.time()

                if self.prev_octets is not None:
                    debit = self.calculate_rate(current_octets)

                    # Écriture dans le fichier
                    with open("debit.txt", "a") as f:
                        f.write(f"{current_time},{debit:.2f}\n")
                        print(f"Débit: {debit:.2f} o/s")

                # Mise à jour de l'état
                self.prev_octets = current_octets
                self.prev_time = current_time

                # Attente dynamique
                time.sleep(max(1.0 - (time.time() - current_time), 0.1))

            except Exception as e:
                print(f"Erreur critique: {str(e)}")
                self.running = False

if __name__ == "__main__":
    monitor = TrafficMonitor()
    monitor.start_monitoring()
    sys.exit(0)