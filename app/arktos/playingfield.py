from .hardware.hardware_interface import HardwareInterface
from .hexagon import Hexagon

class Playingfield:
    def __init__(self, interface, starts: list[Hexagon], ends: list[Hexagon]):
        self.interface: HardwareInterface = interface
        self.starts: list[Hexagon] = starts
        self.ends: list[Hexagon] = ends
