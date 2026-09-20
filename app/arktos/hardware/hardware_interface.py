from __future__ import annotations
from abc import ABC, abstractmethod

from ..hexagon import Hexagon

class RGBColor():
    def __init__(self, r: int, g: int, b:int):
        self.r = r
        self.g = g
        self.b = b
    
    def to_hex(self):
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
        
    def to_percent(self):
        return (self.r/255, self.g/255, self.b/255)

class RGBLedInterface(ABC):
    @abstractmethod
    def on(self) -> None:
        pass

    @abstractmethod
    def off(self) -> None:
        pass

    @abstractmethod
    def is_on(self) -> bool:
        pass

    @abstractmethod
    def set_color(self, color: RGBColor) -> None:
        pass

    @abstractmethod
    def get_color(self) -> RGBColor:
        pass


class ButtonInterface(ABC):
    @abstractmethod
    def is_pressed(self) -> bool:
        pass


class HexagonControllerInterface(ABC):
    @abstractmethod
    def get_hexagon(self) -> Hexagon:
        pass

    @abstractmethod
    def get_led(self) -> RGBLedInterface:
        pass

    @abstractmethod
    def get_button(self) -> ButtonInterface:
        pass


class HardwareInterface(ABC):
    # @abstractmethod
    # def discovery(cls) -> list[HardwareInterface]:
    #     pass

    @abstractmethod
    def get_controllers(self) -> list[HexagonControllerInterface]:
        pass

    @abstractmethod
    def get_start_button(self) -> ButtonInterface:
        pass
