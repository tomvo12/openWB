import os
from pymodbus.client.sync import ModbusTcpClient, ConnectionException


def getPortNo(type, ipaddress):
    slaveid = 1
    file_path = '/var/www/html/openWB/ramdisk/solaredgeport_' + str(type)
    # ModBus is configured to listen on port 502 or 1502, actual port is autodetected and cache in ramdisk
    port = 0                    # port not defined
    ramdiskInitialized = False  # assume ramdisk cache is not set
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            try:
                data = f.read()
                (ipaddr, port) = data.split(':')
                if(ipaddress == ipaddr):
                    ramdiskInitialized = True
                    return port
                else:
                    print('changed ip addr, old: %s, new: %s' %
                          (ipaddr, ipaddress))
                    os.remove(file_path)
            except:
                pass    # ramdisk file does not exist, proceed with autodetection

    port = 502  # try port 502 first

    client = ModbusTcpClient(ipaddress, port=port)
    try:
        resp = client.read_holding_registers(40000, 1, unit=slaveid)
        if resp.registers[0] == 21365:
            if not ramdiskInitialized:  # if we reach this line, we were able to read ModBus registers
                # ramdisk is not set, so persist port value now for next time
                with open(file_path, 'w') as f:
                    f.write(ipaddress + ':' + str(port))
                return port
        # we were unable to read registers from port 502 so try 1502 next
    except ConnectionException:
        port = 1502
        client.port = port
        try:
            resp = client.read_holding_registers(40000, 1, unit=slaveid)
            if resp.registers[0] == 21365:
                # now it worked, persist port number in ramdisk
                if not ramdiskInitialized:
                    with open(file_path, 'w') as f:
                        f.write(ipaddress + ':' + str(port))
                    return port
        except:
            # no connection, remove cache file if any
            if os.path.isfile(file_path):
                os.remove(file_path)
    return port
