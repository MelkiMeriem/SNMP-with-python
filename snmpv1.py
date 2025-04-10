from pysnmp.hlapi import CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, getCmd
from pysnmp.entity.engine import SnmpEngine

# Define the SNMP data to fetch
data = (
    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysLocation', 0)),
    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)),
    ObjectType(ObjectIdentity('.1.3.6.1.2.1.1.1.0')),
)

# Send the SNMP GET request
g = getCmd(
    SnmpEngine(),
    CommunityData('com', mpModel=0),
    UdpTransportTarget(('localhost', 161)),
    ContextData(),
    *data
)

# Process the response
errorIndication, errorStatus, errorIndex, varBinds = next(g)

# Check if there's an error
if errorIndication:
    print(f"Error: {errorIndication}")
elif errorStatus:
    print(f'{errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or "?"}')
else:
    # Output the SNMP response data
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))
