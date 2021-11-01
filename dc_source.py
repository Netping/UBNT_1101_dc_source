import minimalmodbus
from threading import Lock




class DC_SOURCE:
    mutex = Lock()

    def __init__(self, channel):
        self.__channels = {
                            'DPH5015_1' : {
                                            'path' : '/dev/dkst1101/@COM10',
                                            'baudrate' : 9600,
                                            'bytesize' : 8,
                                            'timeout' : 2
                                        },
                            'DPH5015_2' : {
                                            'path' : '/dev/dkst1101/@COM11',
                                            'baudrate' : 9600,
                                            'bytesize' : 8,
                                            'timeout' : 2
                                        },
                            'DPH5015_3' : {
                                            'path' : '/dev/dkst1101/@COM12',
                                            'baudrate' : 9600,
                                            'bytesize' : 8,
                                            'timeout' : 2
                                        },
                            'DPH5020_1' : {
                                            'path' : '/dev/dkst1101/@COM13',
                                            'baudrate' : 9600,
                                            'bytesize' : 8,
                                            'timeout' : 2
                                        },
                            'DPH5020_2' : {
                                            'path' : '/dev/dkst1101/@COM14',
                                            'baudrate' : 9600,
                                            'bytesize' : 8,
                                            'timeout' : 2
                                        }
                        }

        self.__config = self.__channels[channel]
        self.__device = None

        self.__initialize()

    def set(self, voltage, amperage):
        #TODO check limits
        if self.__device:
            DC_SOURCE.mutex.acquire()

            self.__device.write_register(0, voltage * 100)
            self.__device.write_register(1, voltage * 100)

            DC_SOURCE.mutex.release()

    def toggle(self, state):
        value = -1

        if state.uppercase() == 'ON':
            value = 1

        if state.uppercase() == 'OFF':
            value = 0

        if self.__device and value != -1:
            DC_SOURCE.mutex.acquire()

            self.__device.write_register(9, value)

            DC_SOURCE.mutex.release()

    def getPower(self):
        value = 0

        if self.__device:
            DC_SOURCE.mutex.acquire()

            value = self.__device.read_register(4)
            #value = self.__device.read_register(2) * self.__device.read_register(3)

            DC_SOURCE.mutex.release()

        return value

    def getInfo(self):
        value = []

        if self.__device:
            DC_SOURCE.mutex.acquire()

            value = self.__device.read_registers(0,11)

            DC_SOURCE.mutex.release()

        return value

    def __initialize(self):
        DC_SOURCE.mutex.acquire()

        #connect to device
        try:
            self.__device = minimalmodbus.Instrument(self.__config['path'], 1)
            self.__device.serial.baudrate = self.__config['serial_baudrate']
            self.__device.serial.bytesize = self.__config['serial_bytesize']
            self.__device.serial.timeout = self.__config['serial_timeout']
            self.__device.mode = minimalmodbus.MODE_RTU
        except Exception as exception:
            print('Failed to initialize DC_SOURCE module ' + self.__config['path'])
            print(exception)

        DC_SOURCE.mutex.release()

        #turn off power
        self.toggle('OFF')

    def __del__(self):
        if self.__device:
            DC_SOURCE.mutex.acquire()

            self.__device.write_register(0, 0)
            self.__device.write_register(1, 0)
            self.__device.write_register(9, 0)

            DC_SOURCE.mutex.release()
