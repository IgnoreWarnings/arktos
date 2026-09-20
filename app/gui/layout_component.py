import math
import tkinter as tk

from .layout import GeometricLayout, GeometricLayoutBuilder
from .drawing import HexagonDrawer

class LayoutComponent(tk.Frame):
    def __init__(self, parent, layout: GeometricLayout, hexagon_handler=lambda hexagon: None, socket_handler=lambda socket: None):
        super().__init__(parent)

        self.layout = layout
        self.hexagon_handler = hexagon_handler
        self.socket_handler = socket_handler
        self.hexagon_to_polygon = {}
        self.item_to_hexagon = {}
        self.item_to_socket = {}
        self.socket_to_item = {}

        self.padding_x = 150
        self.padding_y = 250
        self.x_offset = self.layout.hex_size + self.padding_x
        self.y_offset = self.layout.hex_size + self.padding_y

        # Canvas
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(side="bottom", fill="both", expand=True)

        # Click handlers
        self.canvas.tag_bind("hex", "<Button-1>", self._on_hex_click)
        self.canvas.tag_bind("socket", "<Button-1>", self._on_socket_click)

        self.draw_hexmap()
    
    def set_hexagon_handler(self, handler):
        self.hexagon_handler = handler

    def set_socket_handler(self, handler):
        self.socket_handler = handler

    def _on_hex_click(self, event):
        item = self.canvas.find_withtag("current")[0]
        hexagon = None
        if item in self.item_to_hexagon:
            hexagon = self.item_to_hexagon[item]

        self.hexagon_handler(hexagon)
    
    def _on_socket_click(self, event):
        item = self.canvas.find_withtag("current")[0]
        socket = None
        if item in self.item_to_socket:
            socket = self.item_to_socket[item]

        self.socket_handler(socket)

    def replace_layout(self, layout: GeometricLayout):
        self.layout = layout
        self.x_offset = self.layout.hex_size + self.padding_x
        self.y_offset = self.layout.hex_size + self.padding_y

        self.redraw()

    def set_padding_x(self, value):
        self.padding_x = int(value)
        self.x_offset = self.layout.hex_size + self.padding_x
        self.redraw()

    def set_padding_y(self, value):
        self.padding_y = int(value)
        self.y_offset = self.layout.hex_size + self.padding_y
        self.redraw()

    def resize(self, value):
        self.hexagon_size = int(value)
        self.layout = GeometricLayoutBuilder.resize(
            self.layout, self.hexagon_size
        )

        self.x_offset = self.layout.hex_size + self.padding_x
        self.y_offset = self.layout.hex_size + self.padding_y

        self.redraw()

    def set_hexagon_color(self, hexagon, color):
        item = self.hexagon_to_polygon[hexagon]
        self.canvas.itemconfigure(item, fill=color)

    def redraw(self):
        self.canvas.delete("all")
        self.draw_hexmap()
        self.update_idletasks()

    def draw_hexmap(self):
        # Draw hexagons
        drawer = HexagonDrawer(self.canvas)
        for hexagon, position in self.layout.hexagon_map.items():
            x, y = position
            x += self.x_offset
            y += self.y_offset
            color = "grey"

            # TODO: Fix id to match everywhere
            polygon_id, text_id = drawer.draw(x, y, self.layout.hex_size, id(hexagon), color)

            # Lookup tables
            self.item_to_hexagon[polygon_id] = hexagon
            self.item_to_hexagon[text_id] = hexagon

            self.hexagon_to_polygon[hexagon] = polygon_id 

        for socket, position in self.layout.socket_map.items():

            edge_angles = [
                math.radians(0),
                math.radians(60),
                math.radians(120),
                math.radians(180),
                math.radians(240),
                math.radians(300),
            ]
            
            # Determine position with offsets
            x,y = position
            x += self.x_offset
            y += self.y_offset

            socket_length = self.layout.hex_size * 0.5
            socket_width = self.layout.hex_size * 0.4

            color = "green" if socket.peer else "grey"

            socket_id = drawer.draw_socket(
                x,
                y,
                edge_angles[socket.orientation.value],
                length=socket_length,
                width=socket_width,
                color=color,
                inset=socket_length / 2
            )

            # Lookup tables
            self.item_to_socket[socket_id] = socket
            self.socket_to_item[socket] = socket_id
    