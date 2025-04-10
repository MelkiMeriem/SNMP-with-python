from pysnmp.hlapi import *
import time
from datetime import datetime

# Configuration SNMP
COMMUNAUTE = 'com'
HOTE = 'localhost'
PORT = 161
OID_OCTETS = '1.3.6.1.2.1.2.2.1.10.1'  # ifInOctets pour l'interface 1

def obtenir_octets_reseau():
    """Récupère le nombre d'octets via SNMP"""
    erreur, etat, idx, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(COMMUNAUTE),
               UdpTransportTarget((HOTE, PORT)),
               ContextData(),
               ObjectType(ObjectIdentity(OID_OCTETS)))
    )

    if erreur:
        print(f"Erreur SNMP: {erreur}")
        return None
    else:
        return int(varBinds[0][1])

def enregistrer_volume_reel():
    """Enregistre le volume réseau réel"""
    dernier_octets = None

    while True:
        octets = obtenir_octets_reseau()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if octets is not None:
            with open("mesures_reelles.txt", "a") as f:
                if dernier_octets is not None:
                    volume = octets - dernier_octets
                    f.write(f"{timestamp},{volume}\n")
                dernier_octets = octets

        time.sleep(1)

# Utilisation
enregistrer_volume_reel()