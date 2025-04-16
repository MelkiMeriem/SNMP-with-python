from pysnmp.hlapi import *

# Exemple pour activer ifIndex 2 (wlp3s0 par exemple)
interface_id = 5
oid = f'1.3.6.1.2.1.2.2.1.7.{interface_id}'  # ifAdminStatus.X

set_cmd = setCmd(
    SnmpEngine(),
    CommunityData('public', mpModel=1),
    UdpTransportTarget(('localhost', 161)),
    ContextData(),
    ObjectType(ObjectIdentity(oid), Integer(1))  # 1 = up, 2 = down
)

errorIndication, errorStatus, errorIndex, varBinds = next(set_cmd)

if errorIndication:
    print(f"Erreur : {errorIndication}")
elif errorStatus:
    print(f"Statut erreur: {errorStatus.prettyPrint()} at {varBinds[int(errorIndex)-1][0]}")
else:
    print("Interface activée avec succès !")
