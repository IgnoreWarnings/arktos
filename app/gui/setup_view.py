import tkinter as tk
from tkinter import messagebox

from arktos.hardware import HardwareInterface, RGBColor
from arktos.colors import COLORS
from arktos.hexagon import Orientations
from arktos.playingfield import Playingfield
from .hardware_component import HardwareComponent
from .layout import GeometricLayoutBuilder
from .layout_view import LayoutView
from .drawing import HexagonDrawer
from .cursor import Cursor
from .collapsible_component import CollapsibleInfo

class SetupView(tk.Frame):
    ###############################
    # Event Listeners
    ###############################

    def mouse_movement(self, event):
        if(self.selected is None):
            return

        self.cursor.clear()
        x = event.x_root - self.canvas.winfo_rootx()
        y = event.y_root - self.canvas.winfo_rooty()
        id = self.interface.get_controllers().index(self.selected)

        offset = 60
        self.cursor.set_position(x + offset, y + offset)
        self.cursor.set_id(id)
        self.cursor.draw()

    def on_enter(self, event):
        self.place()

    def on_socket_click(self, socket):
        # Find corresponding hardware controller
        for controller in self.interface.get_controllers():
            hexagon = controller.get_hexagon()
            if hexagon is not None:
                for s in hexagon.sockets:
                    if s == socket:
                        if not self.selected_socket:
                            self.select_socket(socket)
                            return
                        
                        if self.selected_socket == socket:
                            self.deselect_socket()
                            return

                        if not hexagon in self.layout_view.layout_component.layout.hexagon_map:
                            return

                        # TODO: BUG dont allow attachment to same sockets on one hexagon

                        # Attach
                        socket.connect(self.selected_socket)

                        # Rebuild Layout
                        self.rebuild_layout()

                        # Deselect
                        self.deselect_socket()

                        break

    def select_next(self, event):
        if not self.selected:
            self.select(self.interface.get_controllers()[0])
            return

        index = self.interface.get_controllers().index(self.selected)
        if index + 1 >= len(self.interface.get_controllers()):
            return

        selected = self.interface.get_controllers()[index + 1]
        self.select(selected)

    def select_prev(self, event):
        if not self.selected:
            self.select(self.interface.get_controllers()[0])
            return

        index = self.interface.get_controllers().index(self.selected)
        if index <= 0:
            return
        
        selected = self.interface.get_controllers()[index - 1]
        self.select(selected)

    def on_hexagon_click(self, hexagon):
        controller = next(
            (c for c in self.interface.get_controllers() if c.get_hexagon() == hexagon),
            None
        )

        led = controller.get_led()

        # Deselect
        if hexagon in self.playingfield.starts:
            self.playingfield.starts = []
            led.set_color(COLORS.GREEN)
            return

        if hexagon in self.playingfield.ends:
            self.playingfield.ends = []
            led.set_color(COLORS.GREEN)
            return 

        if self.playingfield.starts == []:
            self.playingfield.starts.append(hexagon)
            led.set_color(COLORS.LIGHT_BLUE)
            return
        
        if self.playingfield.ends == []:
            self.playingfield.ends.append(hexagon)
            led.set_color(COLORS.PURPLE)
            return
        
    def finish_setup(self):
        if self.playingfield.starts == []:
            messagebox.showinfo(
                "No START hexagon",
                "No START selected\nClick on a hexagon (not the connectors) to select a start."
            )
            return
        
        if self.playingfield.ends == []:
            messagebox.showinfo(
                "No END hexagon",
                "No END selected\nClick on a hexagon (not the connectors) to select an end."
            )
            return

        self.on_complete(self.playingfield)

    ###############################
    # UI Processing
    ###############################
    def update(self):
        for controller in self.interface.get_controllers():
            # On hw press
            if controller.get_button().is_pressed():
                # Change selected on hw press
                self.select(self.selected)

                color = led.get_color().to_hex()

            # Update hexagon color
            hexagon = controller.get_hexagon()
            color = controller.get_led().get_color().to_hex()
            try:
                self.layout_view.layout_component.set_hexagon_color(
                    hexagon,
                    color
                )
            except Exception as e:
                #print(f"Not placed {e}")
                pass

        # Schedule update
        self.root.after(50, self.update)

    def rebuild_layout(self):
        entrypoint = next(iter(self.layout_view.layout_component.layout.hexagon_map))
        hex_size = self.layout_view.layout_control_component.resize_slider.get()
        layout = GeometricLayoutBuilder.layout(entrypoint, hex_size=hex_size)
        self.layout_view.layout_component.replace_layout(layout)

    def is_placed(self, hexagon):
        return hexagon in self.layout_view.layout_component.layout.hexagon_map.keys()

    def select_socket(self, socket):
        # Deselect
        if self.selected_socket:
            deselect_socket()
        
        socket_item = self.layout_view.layout_component.socket_to_item[socket]
        self.canvas.itemconfig(socket_item, fill="white", outline="black")
        self.selected_socket = socket

    def deselect_socket(self):
        self.selected_socket = None

        # Rebuild Layout
        self.rebuild_layout()

    def select(self, controller):
        # Deselect last selected
        if self.selected:
            # Only if not already in layout
            led = self.selected.get_led()
            if self.selected.hexagon in self.playingfield.starts:
                led.set_color(COLORS.LIGHT_BLUE)
            elif self.selected.hexagon in self.playingfield.ends:
                led.set_color(COLORS.PURPLE)
            elif not self.is_placed(self.selected.hexagon):
                led.set_color(COLORS.RED)
            else:
                led.set_color(COLORS.GREEN)

            led.on()

        self.selected = controller
        led = controller.get_led()
        led.set_color(COLORS.YELLOW)
        led.on()

    def place(self):
        if self.selected is None:
            return
            
        placed_hexagon = self.selected.get_hexagon()
        controller = next(
                (c for c in self.interface.get_controllers() if c.get_hexagon() == placed_hexagon),
                None
            )

        if self.selected_socket:
            # Connect to selected Socket
            placed_hexagon.attach_oposing(self.selected_socket)
        elif self.layout_view.layout_component.layout.hexagon_map != {}:
            messagebox.showinfo(
                "No Socket Selected",
                "No socket selected to attach to.\nClick on a socket to attach to."
            )
            return

        if self.layout_view.layout_component.layout.hexagon_map == {}:
            hex_size = self.layout_view.layout_control_component.resize_slider.get()
            layout = GeometricLayoutBuilder.layout(placed_hexagon, hex_size=hex_size)
            self.layout_view.layout_component.replace_layout(layout)

        self.rebuild_layout()

        # Set Led to indicate placed
        controller.get_led().set_color(COLORS.GREEN)

        # Deselect
        self.deselect_socket()

    def __init__(
            self,
            root,
            interface: HardwareInterface,
            on_complete=lambda playingfield: None
        ):
        super().__init__(root)
        self.interface = interface
        self.root = root
        self.on_complete = on_complete

        # Hardware UI
        hwc = HardwareComponent(self, interface)
        hwc.pack(side="left", fill="both")

        # Main area
        main = tk.Frame(self)
        main.pack(side="left", fill="both", expand=True)

        # Header
        header = tk.Label(
            main,
            text="Setup",
            font=("Arial", 14, "bold")
        )
        header.pack(side="top")

        # Layout
        layout = GeometricLayoutBuilder.empty()

        # Layout UI
        self.layout_view = LayoutView(main, layout)
        self.layout_view.layout_component.set_socket_handler(
            self.on_socket_click
        )
        self.layout_view.layout_component.set_hexagon_handler(
            self.on_hexagon_click
        )
        self.layout_view.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Canvas
        self.canvas = self.layout_view.layout_component.canvas

        # Right Side Panel
        side_panel = tk.Frame(self)
        side_panel.pack(
            side="right",
            fill="y"
        )

        # Instructions
        info = CollapsibleInfo(
            side_panel,
            title="Instructions",
            text=(
                "1. Select a hexagon by pressing the hardware switch\n"
                "or use the arrow keys on the keyboard\n\n"
                "2. Click the connector you want to attach it to\n\n"
                "3. Press enter to place the hexagon.\n\n"
                "4. Connect hexagons by clicking 2 sockets\n\n"
                "5. Repeat until all hexagons are placed and connected\n\n"
                "6. Select Start and End by clicking on hexagons\n\n"
                "7. Click the finish button.\n"
            )
        )
        info.toggle()
        info.pack(side="top", fill="x", padx=10, pady=10)

        # Finish button
        finish_button = tk.Button(
            side_panel,
            text="Finish Setup",
            command=self.finish_setup,
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
        )
        finish_button.pack(side="bottom", pady=(0, 100))
        
        # Placement
        self.selected = None
        self.selected_socket = None

        # Playingfield
        self.playingfield = Playingfield(self.interface, [], [])

        # Cursor
        self.cursor = Cursor(self.canvas)
        self.cursor.set_size(60)
        self.cursor.set_position(400,400)

        # Events
        # Cant have cursor cause bad gpu performance on pi
        #self.canvas.bind("<Motion>", self.mouse_movement)
        self.bind("<Right>", self.select_next)
        self.bind("<Left>", self.select_prev)
        self.bind("<Return>", self.on_enter)
        self.focus_set()

        # Init
        # Turn all leds RED
        controllers = interface.get_controllers()
        for controller in controllers:
            led = controller.get_led()
            led.set_color(COLORS.RED)
            led.on()

        self.update()
