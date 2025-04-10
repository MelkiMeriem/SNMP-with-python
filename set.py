from pysnmp.hlapi import *

def show_item():
    g = getCmd(SnmpEngine(),
               UsmUserData("usr-sha-des",
                           authProtocol=usmHMACSHAAuthProtocol,
                           authKey="authkey1",
                           privProtocol=usmDESPrivProtocol,
                           privKey="privkey1"),
               UdpTransportTarget(('localhost', 161)),
               ContextData(),
               ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0)))
    errorIndication, errorStatus, errorIndex, varBinds = next(g)
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print(f'Error: {errorStatus.prettyPrint()}')
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))

# Show initial value
show_item()

# Setting new value
g = setCmd(SnmpEngine(),
           UsmUserData("usr-sha-des",
                       authProtocol=usmHMACSHAAuthProtocol,
                       authKey="authkey1",
                       privProtocol=usmDESPrivProtocol,
                       privKey="privkey1"),
           UdpTransportTarget(('localhost', 161)),
           ContextData(),
           ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0), 'Hello from Lannion using Kalray processor on Linux'))

errorIndication, errorStatus, errorIndex, varBinds = next(g)

if errorIndication:
    print(errorIndication)
elif errorStatus:
    print(f'Error during set: {errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex)-1][0] or "?"}')
else:
    print("Set successful:")
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))

# Show updated value
show_item()