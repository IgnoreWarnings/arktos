import can

from ..hardware_interface import RGBColor

class CanConnection():
    def __init__(self, channel='can0', interface='socketcan', baudrate=125_000):
        self.channel = channel
        self.interface = interface
        self.baudrate = baudrate

    def open(self):
        self.bus = can.interface.Bus(channel=self.channel, interface=self.interface , bitrate=self.baudrate)

    def close(self):
        self.bus.shutdown()

    def read(self, timeout = 0) -> can.Message | None :
        return self.bus.recv(timeout=timeout)

    def write(self, message):
        self.bus.send(message)
