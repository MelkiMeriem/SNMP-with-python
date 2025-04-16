from pysnmp.hlapi import *

def get_active_interfaces():
    active_interfaces = []

    g = nextCmd(
        SnmpEngine(),
        CommunityData('public', mpModel=1),  # SNMPv2c
        UdpTransportTarget(('localhost', 161), timeout=5, retries=2),
        ContextData(),
        ObjectType(ObjectIdentity('IF-MIB', 'ifInOctets')),
        lexicographicMode=False,
        lookupMib=True
    )

    try:
        while True:
            errorIndication, errorStatus, errorIndex, varBinds = next(g)

            if errorIndication:
                print(f"SNMP Error: {errorIndication}")
                break

            if errorStatus:
                print(f"SNMP Error: {errorStatus.prettyPrint()}")
                break

            for varBind in varBinds:
                oid, value = varBind
                print(f"Received: {oid.prettyPrint()} = {value.prettyPrint()}")  # Debug output
                if int(value) > 0:
                    interface_index = oid[-1]
                    active_interfaces.append(interface_index)

    except StopIteration:
        pass  # Normal exit when generator is exhausted

    return active_interfaces

print("Active Interfaces:", get_active_interfaces())