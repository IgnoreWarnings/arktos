import tkinter as tk

from arktos.hardware import HardwareInterface, HexagonControllerInterface, RGBColor

class ControllerRow:
    def __init__(self, parent, hexagon_id, controller: HexagonControllerInterface):
        self.controller = controller
        self.hexagon_id = hexagon_id

        self.frame = tk.Frame(parent)

        self.button_state = tk.StringVar(value="Released")
        self.led_state = tk.BooleanVar(value=False)

        tk.Label(
            self.frame,
            text=str(hexagon_id),
            width=20,
            anchor="w"
        ).grid(row=0, column=0, padx=5, pady=2)

        tk.Label(
            self.frame,
            textvariable=self.button_state,
            width=10,
            anchor="w"
        ).grid(row=0, column=1, padx=5)

        self.led_color_label = tk.Label(
            self.frame,
            width=10,
            text="NOT INITIALIZED",
        )
        
        self.led_color_label.grid(row=0, column=2, padx=5)

    def update_state(self):
        # Button
        if self.controller.get_button().is_pressed():
            self.button_state.set("Pressed")
        else:
            self.button_state.set("Released")

        # LED
        if self.controller.get_led().get_color() != RGBColor(0,0,0):
            color = self.controller.get_led().get_color()
            self.led_color_label.config(text=color.to_hex(), background=color.to_hex())
        else:
            self.led_color_label.config(text="OFF", background="grey")


class HardwareComponent(tk.Frame):
    def __init__(self, parent, interface: HardwareInterface):
        super().__init__(parent)
        self.interface = interface

        self.start_button_state = tk.StringVar(value="Released")

        # Group
        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10, anchor="n")

        # Labels
        label = tk.Label(frame, text="Hardware Connector", font=("Arial", 14, "bold"))
        label.pack(fill="x", pady=4)

        # Dropdown
        interface_options = ["Mock Interface"]  
        self.interface_type = tk.StringVar(value="Mock Interface")
        option_menu = tk.OptionMenu(frame, self.interface_type, *interface_options)
        option_menu.pack(side="left")

        label = tk.Label(frame, text="Status: CONNECTED", font=("Arial", 10), fg="black", bg="green")
        label.pack(side="right")

        # Group
        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10, anchor="n")

        # Labels
        label = tk.Label(frame, text="Hardware Status", font=("Arial", 14, "bold"))
        label.pack(fill="x", pady=4)

        label = tk.Label(frame, text="Start Button", font=("Arial", 12, "bold"))
        label.pack(fill="x", pady=4)
        
        label = tk.Label(frame, textvariable=self.start_button_state)
        label.pack(fill="x", pady=4)

        label = tk.Label(frame, text="Hexagon Controllers", font=("Arial", 12, "bold"))
        label.pack(fill="x", pady=4)

        header = tk.Frame(frame)
        header.pack(fill="x", padx=30, pady=(10, 0))

        tk.Label(header, text="Hexagon", width=10, font=("Arial", 10, "bold")).grid(row=0, column=0)
        tk.Label(header, text="Button", width=10, font=("Arial", 10, "bold")).grid(row=0, column=1)
        tk.Label(header, text="LED", width=10, font=("Arial", 10, "bold")).grid(row=0, column=2)

        self.rows = {}

        body = tk.Frame(frame)
        body.pack(fill="both", expand=True, padx=10)

        for controller in interface.get_controllers():
            _id = id(controller.get_hexagon())
            row = ControllerRow(
                body,
                _id,
                controller
            )

            row.frame.pack(fill="x", pady=1)

            self.rows[_id] = row

        self.poll()

    def poll(self):
        # Button
        if self.interface.get_start_button().is_pressed():
            self.start_button_state.set("Pressed")
        else:
            self.start_button_state.set("Released")

        for row in self.rows.values():
            row.update_state()

        self.after(100, self.poll)