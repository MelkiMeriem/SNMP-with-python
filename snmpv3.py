from pysnmp.hlapi import *

# Define OIDs to retrieve
data = (
    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysLocation', 0)),
    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)),
    ObjectType(ObjectIdentity('.1.3.6.1.2.1.1.1.0')),
)

# Execute SNMPv3 query
g = getCmd(
    SnmpEngine(),
    UsmUserData(
        "usr-sha-des",  # Username
        authProtocol=usmHMACSHAAuthProtocol,  # Authentication protocol (SHA)
        authKey="authkey1",  # Authentication key
        privProtocol=usmDESPrivProtocol,  # Privacy protocol (DES)
        privKey="privkey1"  # Privacy key
    ),
    UdpTransportTarget(('localhost', 161)),
    ContextData(),
    *data
)

# Retrieve results
errorIndication, errorStatus, errorIndex, varBinds = next(g)

# Handle errors
if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
    # Display the results
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))
