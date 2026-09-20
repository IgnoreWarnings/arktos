import tkinter as tk

from arktos.hardware import HardwareInterface
from .hardware_component import HardwareComponent
from .layout import GeometricLayoutBuilder
from .layout_view import LayoutView

class HardwareView(tk.Frame):
    def start_updater(self):
        for controller in self.interface.get_controllers():
            hexagon = controller.get_hexagon()

            led = controller.get_led()
            color = led.get_color().to_hex() if led.is_on() else "grey"

            try:
                self.layout_view.layout_component.set_hexagon_color(
                    hexagon,
                    color
                )
            except Exception as e:
                #print(f"Error updating hexagon color: {e}")
                pass

        self.after(50, self.start_updater)

    def __init__(self, parent, interface: HardwareInterface):
        super().__init__(parent)

        self.interface = interface

        # Hardware Components
        self.hardware_component = HardwareComponent(self, interface)
        self.hardware_component.pack(
            side="left",
            fill="both"
        )

        # Hardware Viewer
        header = tk.Label(self, text="Hardware Interface Viewer", font=("Arial", 14, "bold"))
        header.pack()

        # Assuming there is only one hexagon "island"
        entrypoint = interface.get_controllers()[0].get_hexagon()
        layout = GeometricLayoutBuilder.layout(entrypoint)

        self.layout_view = LayoutView(self, layout)
        self.layout_view.pack(
            side="right",
            fill="both",
            expand=True
        )

        # ToDo: smarter way to start update e.g. on pack
        self.start_updater()
