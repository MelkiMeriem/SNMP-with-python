from pysnmp.hlapi import *
data = (
    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysLocation', 0)),
    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)),
    ObjectType(ObjectIdentity('.1.3.6.1.2.1.1.1.0')),
    #the last two arguments reffer to the same object (we identify it whether through hierarchy or through its OID)
)
g = getCmd(SnmpEngine(), CommunityData('public', mpModel=1)
           , UdpTransportTarget(('localhost', 161))
           , ContextData() , *data)
errorIndication, errorStatus, errorIndex, varBinds = next(g)
if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))