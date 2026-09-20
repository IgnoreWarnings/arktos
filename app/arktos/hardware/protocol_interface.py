import json

from ..hexagon import Hexagon
from .hardware_interface import HardwareInterface, HexagonControllerInterface, ButtonInterface, RGBLedInterface, RGBColor

class RGBLedInterface(RGBLedInterface):
    def on(self) -> None:
        pass

    def off(self) -> None:
        pass

    def is_on(self) -> bool:
        pass

    def set_color(self, color: RGBColor) -> None:
        pass

    def get_color(self) -> RGBColor:
        pass


class ButtonInterface(ButtonInterface):
    def is_pressed(self) -> bool:
        pass


class HexagonControllerInterface(HexagonControllerInterface):
    def get_hexagon(self) -> Hexagon:
        pass

    def get_led(self) -> RGBLedInterface:
        pass

    def get_button(self) -> ButtonInterface:
        pass


class ProtocolInterface(HardwareInterface):
    def __init__(self, protocol, connection) -> None:
        super().__init__()
        self.protocol = protocol
        self.connection = connection

        connection.open()
        connection.write(protocol.handshake())
        handshake = connection.read()
        print(handshake)

    def get_controllers(self) -> list[HexagonControllerInterface]:
        connection.write(JSONProtocol.)
        decoder = json.decoder.JSONDecoder()
        decoder.decode()

    def get_start_button(self) -> ButtonInterface:
        pass

