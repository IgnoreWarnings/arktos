
from ...hexagon import Hexagon
from ..hardware_interface import HardwareInterface, HexagonControllerInterface, ButtonInterface, RGBLedInterface, RGBColor
from .can_connection import CanConnection
from .can_protocol import CanProtocol
from arktos.colors import COLORS


class CanRGBLed(RGBLedInterface):
    def __init__(self) -> None:
        super().__init__()
        self.state = False
        self.color = RGBColor(0,0,0)

    def on(self) -> None:
        self.state = True

    def off(self) -> None:
        self.state = False

    def is_on(self) -> bool:
        return self.state

    def set_color(self, color: RGBColor) -> None:
        self.color = color

    def get_color(self) -> RGBColor:
        return self.color


class CanButton(ButtonInterface):
    def __init__(self):
        self.state = False

    def is_pressed(self) -> bool:
        return self.state


class CanHexagonController(HexagonControllerInterface):
    def __init__(self, hexagon: Hexagon, led: RGBLedInterface, button: ButtonInterface) -> None:
        super().__init__()
        # Spawn fake hardware
        self.hexagon = hexagon
        self.led = led
        self.button = button

    @classmethod
    def Can(cls):
        # Spawn fake hardware
        hexagon = Hexagon()
        button = CanButton()
        led = CanRGBLed()
        return CanHexagonController(hexagon, led, button)

    def get_hexagon(self) -> Hexagon:
        return self.hexagon

    def get_led(self) -> RGBLedInterface:
        return self.led

    def get_button(self) -> ButtonInterface:
        return self.button


class CanHardware(HardwareInterface):
    def __init__(self, 
                controllers: list[HexagonControllerInterface], 
                start_button: ButtonInterface) -> None:
        super().__init__()

        self.controllers = controllers
        self.start_button = start_button

    @classmethod 
    def from_discovery(cls, can_connection: CanConnection):
        can_connection.open()

        message = CanProtocol.ping(CanProtocol.BROADCAST_ADDRESS)
        can_connection.write(message)

        ids = []
        while(True):
            message = can_connection.read(timeout=2)
            if message:
                parsed = CanProtocol.parse_arbitration_id(message.arbitration_id)
                ids.append(parsed["source_id"])
            else:
                break
        
        print(ids)
        for _id in ids:
            message = CanProtocol.set_leds(_id, 1, COLORS.YELLOW)
            can_connection.write(message)

        return CanHardware(controllers, start_button)

    def get_controllers(self) -> list[HexagonControllerInterface]:
        return self.controllers
    
    def get_start_button(self) -> ButtonInterface:
        return self.start_button
