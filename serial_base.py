#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import serial
import logging
import binascii
import threading
from serial.tools import list_ports

logging.getLogger('')


class Serial(object):
    def __init__(self, port="COM5", baud_rate="115200", byte_size="8", parity="N", stop_bits="1"):
        self.port = port
        self.baudrate = baud_rate
        self.bytesize = byte_size
        self.parity = parity
        self.stopbits = stop_bits

        self._serial = None
        self.is_connected = False
        self.except_flag = False

    def connect(self, timeout=2):
        self._serial = serial.Serial()
        self._serial.port = self.port
        self._serial.baudrate = self.baudrate
        self._serial.bytesize = int(self.bytesize)
        self._serial.parity = self.parity
        self._serial.stopbits = int(self.stopbits)
        self._serial.timeout = timeout

        try:
            self._serial.open()
            if self._serial.isOpen():
                self.is_connected = True
                logging.info('[%s]%s connect, baudrate %d' %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),self._serial.port, self._serial.baudrate))
        except Exception as e:
            self.is_connected = False
            logging.exception('[%s][ERR_EXCEPTION] %s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), e))

    def disconnect(self):
        if self._serial:
            self.is_connected = False
            self._serial.close()
            logging.info('[%s]%s disconnect' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),self._serial.port))

    def write(self, data):
        if self.is_connected:
            temp = binascii.a2b_hex(data)
            self._serial.write(temp)

    def on_connected_changed(self, func):
        tConnected = threading.Thread(target=self._on_connected_changed, args=(func, ))
        tConnected.setDaemon(True)
        tConnected.start()

    def _on_connected_changed(self, func):
        self._is_connected_temp = False
        while True:
            if self._serial:
                if self._is_connected_temp != self.is_connected:
                    func(self.is_connected)
                self._is_connected_temp = self.is_connected
            elif self._serial == None and self.is_connected == False and self.except_flag == True:
                self.except_flag = False
                func(self.is_connected)
            time.sleep(0.5)

    def on_data_received(self, func):
        tDataReceived = threading.Thread(target=self._on_data_received, args=(func, ))
        tDataReceived.setDaemon(True)
        tDataReceived.start()
    
    def _on_data_received(self, func):
        while True:
            if self.is_connected:
                try:
                    number = self._serial.inWaiting()
                    if number > 0:
                        data = self._serial.read(number).decode('utf-8')
                        if data:
                            func(data)
                except Exception as e:
                    self.is_connected = False
                    self._serial = None
                    self.except_flag = True
                    logging.exception('[%s][ERR_EXCEPTION] %s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), e))
                    break
            time.sleep(0.15)
                
class testHelper(object):
    def __init__(self):
        self.myserial = Serial(Port="COM5", BaudRate="115200")
        self.myserial.connect()
        self.myserial.on_connected_changed(self.myserial_on_connected_changed)

    def write(self, data):
        self.myserial.write(data)

    def myserial_on_connected_changed(self, is_connected):
        if is_connected:
            print('[%s]Connected.' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))
            self.myserial.on_data_received(self.myserial_on_data_received)
        else:
            print('[%s]DisConnected.' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))

    def myserial_on_data_received(self, data):
        print(data)

if __name__ == '__main__':
    myserial = testHelper()
    time.sleep(1)
    myserial.write("5a30000913000411093A2000002Cca")#5a30000913000411093A2000002Cca     #5A3600010037CA
    count = 0
    while count < 3:
        print("Count: %s"%count)
        time.sleep(1)
        count += 1
