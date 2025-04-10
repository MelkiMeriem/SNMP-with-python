from pysnmp.hlapi import *
import time

# Configuration SNMP
COMMUNITY = 'com'  # 
IP_ADDRESS = '127.0.0.1'
PORT = 161
OID_IN_OCTETS = ObjectType(ObjectIdentity('.1.3.6.1.2.1.2.2.1.10.1'))  # Interface 1

def collect_traffic_data():
    while True:
        try:
            # Création de la requête SNMP
            cmd_generator = getCmd(
                SnmpEngine(),
                CommunityData(COMMUNITY, mpModel=1),  # SNMPv2c
                UdpTransportTarget((IP_ADDRESS, PORT), timeout=5, retries=2),
                ContextData(),
                OID_IN_OCTETS
            )

            # Exécution de la requête
            error_indication, error_status, error_index, var_binds = next(cmd_generator)

            # Gestion des erreurs
            if error_indication:
                print(f"Erreur: {error_indication}")
            elif error_status:
                print(f"Statut d'erreur: {error_status.prettyPrint()}")
            else:
                # Extraction et sauvegarde de la valeur
                value = var_binds[0][1].prettyPrint()
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

                print(f"[{timestamp}] Débit: {value} octets")

                with open("debit.txt", "a") as f:
                    f.write(f"{timestamp},{value}\n")

        except Exception as e:
            print(f"Erreur générale: {str(e)}")

        time.sleep(5)

if __name__ == "__main__":
    collect_traffic_data()