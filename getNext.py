from pysnmp.hlapi import *
g = nextCmd(SnmpEngine()
            , CommunityData('com', mpModel=1)
            , UdpTransportTarget(('localhost', 161))
            , ContextData()
            , ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysObjectID', 0)))
errorIndication, errorStatus, errorIndex, varBinds = next(g)
if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint()
                    , errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
                    )
      )
else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))