from abc import ABC, abstractmethod
import colorsys

from .hardware.hardware_interface import HardwareInterface, RGBColor, HexagonControllerInterface

class Animation(ABC):
    @abstractmethod
    def next_frame(self) -> bool:
        """Advance one frame.
        Returns False when the animation has finished.
        """
        pass

    @abstractmethod
    def reset(self) -> None:
        pass
    # @abstractmethod
    # def set_frame(self, frame) -> None:
    #     pass

class AnimationPath(Animation):
    def __init__(self, controllers: list[HexagonControllerInterface]) -> None:
        self.controllers = controllers
        self.path_index = 0

    def next_frame(self) -> bool:
        for controller in self.controllers:
            led = controller.get_led()
            led.set_color(RGBColor(0,150,0))

        led = self.controllers[self.path_index].get_led()
        led.set_color(RGBColor(0,255,0))

        self.path_index += 1

        return self.path_index < len(self.controllers)

    def reset(self) -> None:
        self.path_index = 0


class AnimationFadeAll(Animation):
    def __init__(
        self,
        interface: HardwareInterface,
        start: RGBColor,
        end: RGBColor,
        frames: int = 100,
    ):
        self.leds = []

        for controller in interface.get_controllers():
            led = controller.get_led()
            self.leds.append(led)

        self.start = start
        self.end = end
        self.frames = max(1, frames)
        self.frame = 0

    def next_frame(self) -> bool:
        if self.frame > self.frames:
            return False

        t = self.frame / self.frames

        color = RGBColor(
            int(self.start.r + (self.end.r - self.start.r) * t),
            int(self.start.g + (self.end.g - self.start.g) * t),
            int(self.start.b + (self.end.b - self.start.b) * t),
        )

        for led in self.leds:
            led.set_color(color)

        self.frame += 1
        return True
    
    def set_frame(self, frame) -> None:
        self.frame = frame

    def reset(self) -> None:
        self.frame = 0


class AnimationRainbow(Animation):
    def __init__(
        self,
        interface: HardwareInterface,
        step: float = 0.001,
        brightness: float = 1.0,
    ):
        self.leds = []

        for controller in interface.get_controllers():
            led = controller.get_led()
            self.leds.append(led)

        self.hue = 0.0
        self.step = step
        self.brightness = brightness

    def next_frame(self) -> bool:
        count = len(self.leds)

        for i, led in enumerate(self.leds):
            hue = (self.hue + i / count) % 1.0
            r, g, b = colorsys.hsv_to_rgb(hue, 1.0, self.brightness)

            led.set_color(
                RGBColor(
                    int(r * 255),
                    int(g * 255),
                    int(b * 255),
                )
            )

        self.hue = (self.hue + self.step) % 1.0

        # Rainbow animations never finish on their own.
        return True

    def reset(self) -> None:
        self.hue = 0.0


class AnimationPulse(Animation):
    def __init__(self, interface: HardwareInterface, source: HexagonControllerInterface, radius=None) -> None:
        self.interface = interface
        self.source = source
        self.radius = radius

        self.illuminated: list[HexagonControllerInterface] = []

    def reset(self) -> None:
        self.illuminated = []

    def next_frame(self) -> bool:
        if self.illuminated == []:
            led = self.source.get_led()
            led.set_color(RGBColor(255,0,0))
            self.illuminated.append(self.source)
            return True
        
        controllers = self.interface.get_controllers()
        illumination_layer = []
        for illuminate in self.illuminated:
            for controller in controllers:
                if illuminate.get_hexagon() in controller.get_hexagon().neighbors():
                    led = controller.get_led()
                    led.set_color(RGBColor(255,0,0))
                    illumination_layer.append(controller)
        
        self.illuminated += illumination_layer

        return len(self.illuminated) == len(controllers)
        