import bluetooth

def to_byte(value):
    return value.to_bytes(1, 'big')


def parameter(servoID, servoAngle, runTime, frameDelay):
    return message(b'\x22', [to_byte(servoID), to_byte(servoAngle), to_byte(runTime), to_byte(frameDelay)])

def main():
    msg4 = parameter(4, 0, 0, 0)
    bd_addr = discover()
    if bd_addr:
        port = 6
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((bd_addr, port))
        print('Connected')
        sock.settimeout(60.0)
        sock.send(msg4)
        print('Sent data')
        sock.close()

def message(command, parameters):
    header = b'\xFB\xBF'
    end = b'\xED'
    parameter = b''.join(parameters)
    length = bytearray([len(parameters) + 5])
    data = [command, length]
    data.extend(parameters)
    total = 0;
    for x in data:
        total += ord(x)
        total %= 256
    check = bytes([total])
    return header + length + command + parameter + check + end


def discover():
    print("searching ...")
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print("found %d devices" % len(nearby_devices))
    print(nearby_devices)
    for addr, name in nearby_devices:
        if name == "Alpha1_C5C4":
            print(addr)
            return addr

if __name__ == '__main__':
    main()