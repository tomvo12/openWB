import os.path
from pymodbus.client.sync import ModbusTcpClient, ConnectionException

def getPortNo(ipaddress):
    slaveid = 1
    # ModBus is configured to listen on port 502 or 1502, actual port is autodetected and cache in ramdisk
    port = 0                    # port not defined
    ramdiskInitialized = False  # assume ramdisk cache is not set
    if os.path.isfile('/var/www/html/openWB/ramdisk/solaredgeport'):
        with open('/var/www/html/openWB/ramdisk/solaredgeport', 'r') as f:
            try:
                port = int(f.read())
                ramdiskInitialized = True
                return port
            except:
                pass    # ramdisk file does not exist, proceed with autodetection

    port = 502  # try port 502 first

    client = ModbusTcpClient(ipaddress, port=port)
    try:
        resp= client.read_holding_registers(40206,5,unit=slaveid)
        if not ramdiskInitialized:  # if we reach this line, we were able to read ModBus registers
            # ramdisk is not set, so persist port value now for next time
            with open('/var/www/html/openWB/ramdisk/solaredgeport', 'w') as f:
                f.write(str(port))
            return port
        # we were unable to read registers from port 502 so try 1502 next
    except ConnectionException:
        port = 1502
        client.port = port
        resp= client.read_holding_registers(40206,5,unit=slaveid)
        # now it worked, persist port number in ramdisk
        if not ramdiskInitialized:
            with open('/var/www/html/openWB/ramdisk/solaredgeport', 'w') as f:
                f.write(str(port))
            return port
    return port
