import serial as ser

class Com_Handler:
    def __init__(self, port, baudrate, timeout):
        com = ser.Serial(port, baudrate=baudrate, timeout=timeout)