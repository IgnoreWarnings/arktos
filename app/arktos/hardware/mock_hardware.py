from ..hexagon import Hexagon
from .hardware_interface import HardwareInterface, HexagonControllerInterface, ButtonInterface, RGBLedInterface, RGBColor

class MockRGBLed(RGBLedInterface):
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


class MockButton(ButtonInterface):
    def __init__(self):
        self.state = False

    def is_pressed(self) -> bool:
        return self.state


class MockHexagonController(HexagonControllerInterface):
    def __init__(self, hexagon: Hexagon, led: RGBLedInterface, button: ButtonInterface) -> None:
        super().__init__()
        # Spawn fake hardware
        self.hexagon = hexagon
        self.led = led
        self.button = button

    @classmethod
    def mock(cls):
        # Spawn fake hardware
        hexagon = Hexagon()
        button = MockButton()
        led = MockRGBLed()
        return MockHexagonController(hexagon, led, button)

    def get_hexagon(self) -> Hexagon:
        return self.hexagon

    def get_led(self) -> RGBLedInterface:
        return self.led

    def get_button(self) -> ButtonInterface:
        return self.button


class MockHardware(HardwareInterface):
    def __init__(self, 
                controllers: list[HexagonControllerInterface], 
                start_button: ButtonInterface) -> None:
        super().__init__()

        self.controllers = controllers
        self.start_button = start_button

    @classmethod 
    def from_size(cls, number_of_controllers: int):
        controllers = []
        for _ in range(number_of_controllers):
            controller = MockHexagonController.mock()
            controllers.append(controller)

        start_button = MockButton()
        
        return MockHardware(controllers, start_button)

    @classmethod
    def from_list(cls, hexagon_list):
        controllers = []
        for hexagon in hexagon_list:
            led = MockRGBLed()
            button = MockButton()
            controller = MockHexagonController(hexagon, led, button)
            controllers.append(controller)
        
        start_button = MockButton()

        return MockHardware(controllers, start_button)

    def get_controllers(self) -> list[HexagonControllerInterface]:
        return self.controllers
    
    def get_start_button(self) -> ButtonInterface:
        return self.start_button
