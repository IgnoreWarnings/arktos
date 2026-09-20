import tkinter as tk

from arktos.hardware import MockHardware
from .layout import GeometricLayoutBuilder
from .layout_view import LayoutView

class HardwareEmulatorComponent(tk.Frame):
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

    def simulate_button_press(self, button, hold_time=100):
        button.state = True
        self.after(hold_time, lambda: setattr(button, "state", False))

    def start_button_press(self):
        self.simulate_button_press(self.interface.get_start_button())

    def __init__(self, parent, interface: MockHardware):
        super().__init__(parent)
        self.interface = interface

        header = tk.Label(self, text="Hardware Emulator", font=("Arial", 14, "bold"))
        header.pack(anchor="n")

        # Assuming there is only one hexagon "island"
        entrypoint = interface.get_controllers()[0].get_hexagon()
        layout = GeometricLayoutBuilder.layout(entrypoint)

        self.layout_view = LayoutView(self, layout, click_handler=self.on_hex_click)
        self.layout_view.pack(
            side="right",
            fill="both",
            expand=True
        )

        button = tk.Button(self, text="Start Button", command=self.start_button_press)
        button.pack(fill="x", pady=4)

        # ToDo: smarter way to start update e.g. on pack
        self.start_updater()


    def on_hex_click(self, hexagon):
        # Find corresponding hardware controller
        for controller in self.interface.get_controllers():
            if controller.get_hexagon() == hexagon:
                button = controller.get_button()
                self.simulate_button_press(button)
                break
    