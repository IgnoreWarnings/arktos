
from ...hexagon import Hexagon
from ..hardware_interface import HardwareInterface, HexagonControllerInterface, ButtonInterface, RGBLedInterface, RGBColor
from .can_connection import CanConnection
from .can_protocol import CanProtocol
from arktos.colors import COLORS
from dataclasses import dataclass, field
import threading

@dataclass
class HexagonState:
    color: RGBColor = RGBColor(0, 0, 0)


class CanController:
    def __init__(self, can_connection, can_id):
        self.can_connection = can_connection
        self.can_id = can_id

        self.states = [
            HexagonState(),
            HexagonState(),
            HexagonState(),
        ]

        self.hexagon_controllers = [
            CanHexagonController(
                Hexagon(),
                CanRGBLed(self, 0),
                CanButton()
            ),
            CanHexagonController(
                Hexagon(),
                CanRGBLed(self, 1),
                CanButton()
            ),
            CanHexagonController(
                Hexagon(),
                CanRGBLed(self, 2),
                CanButton()
            ),
        ]

    def get_hexagon_controllers(self) -> list[HexagonControllerInterface]:
        return self.hexagon_controllers

    def get_color(self, index: int) -> RGBColor:
        return self.states[index].color

    def set_led(self, index: int, color: RGBColor) -> None:
        self.states[index].color = color

        self.__send_led_state()

    def __send_led_state(self) -> None:
        colors = [
            state.color for state in self.states
        ]

        message = CanProtocol.set_leds(
            self.can_id,
            colors
        )

        self.can_connection.write(message)


class CanRGBLed(RGBLedInterface):
    def __init__(self, can_controller: CanController, index: int):
        self.can_controller = can_controller
        self.index = index

    def set_color(self, color: RGBColor) -> None:
        self.can_controller.set_led(
            self.index,
            color
        )

    def get_color(self) -> RGBColor:
        return self.can_controller.get_color(self.index)


class CanButton(ButtonInterface):
    def __init__(self):
        self.state = False

    def is_pressed(self) -> bool:
        return self.state


class Updater:
    def __init__(self, can_connection: CanConnection, can_controllers: [CanController]):
        self.can_connection = can_connection
        self.can_controllers = can_controllers

    def listen(self):
        while True:
            message = self.can_connection.read()

            if message:
                parsed = CanProtocol.parse_arbitration_id(message.arbitration_id)
                # TODO: Refactor to a Filter
                if parsed["message_type"] == CanProtocol.MessageType.SCHOLLE:
                    if parsed["protocol_header"] == CanProtocol.ScholleCommand.BUTTON_STATE:
                        for controller in self.can_controllers:
                            if controller.can_id == parsed["source_id"]:
                                value = message.data[0]

                                controller.hexagon_controllers[0].get_button().state = bool(value & (1 << 0))
                                controller.hexagon_controllers[1].get_button().state = bool(value & (1 << 1))
                                controller.hexagon_controllers[2].get_button().state = bool(value & (1 << 2))

    def start(self):
        thread = threading.Thread(target=self.listen, daemon=True)
        thread.start()


class CanHexagonController(HexagonControllerInterface):
    def __init__(self, hexagon: Hexagon, led: RGBLedInterface, button: ButtonInterface) -> None:
        super().__init__()
        self.hexagon = hexagon
        self.led = led
        self.button = button

    def get_hexagon(self) -> Hexagon:
        return self.hexagon

    def get_led(self) -> RGBLedInterface:
        return self.led

    def get_button(self) -> ButtonInterface:
        return self.button

class CanHardware(HardwareInterface):
    def __init__(self, 
                controllers: list[CanHexagonController], 
                start_button: ButtonInterface) -> None:
        super().__init__()

        self.controllers = controllers
        self.start_button = start_button
                
    @classmethod
    def from_discovery(cls, can_connection: CanConnection, start_button):
        can_connection.open()

        can_connection.write(
            CanProtocol.ping(CanProtocol.BROADCAST_ADDRESS)
        )

        ids = set()

        while True:
            message = can_connection.read(timeout=2)

            # All processed
            if message is None:
                break

            parsed = CanProtocol.parse_arbitration_id(
                message.arbitration_id
            )

            if parsed["protocol_header"] != CanProtocol.BusControlMessage.PING_RESPONSE:
                print("Warning: Other message during ping processing recieved")
                continue

            ids.add(parsed["source_id"])

        controllers = []
        can_controllers = []
        for can_id in ids:
            can_controller = CanController(
                can_connection,
                can_id
            )

            controllers.extend(can_controller.get_hexagon_controllers())
            can_controllers.append(can_controller) 

        Updater(can_connection, can_controllers).start()

        return CanHardware(
            controllers,
            start_button
        )

    def get_controllers(self) -> list[HexagonControllerInterface]:
        return self.controllers
    
    def get_start_button(self) -> ButtonInterface:
        return self.start_button
