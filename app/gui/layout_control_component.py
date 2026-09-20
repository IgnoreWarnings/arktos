import tkinter as tk

from .layout_component import LayoutComponent

class LayoutControlComponent(tk.Frame):
    def __init__(self, parent, layout_component: LayoutComponent):
        super().__init__(parent)

        self.layout_component = layout_component

        # Group
        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10, anchor="n")

        # Label
        label = tk.Label(frame, text="Layout Control", font=("Arial", 14, "bold"))
        label.pack(fill="x", pady=4)

        # Resizer
        self.resize_slider = tk.Scale(
            frame,
            from_=1,
            to=100,
            resolution=1,
            orient="horizontal",
            length=100,         # total slider length
            width=25,           # thickness of the trough
            sliderlength=30,    # draggable handle size
            label="Hexagon size",
            command=self.layout_component.resize
        )
        self.resize_slider.set(self.layout_component.layout.hex_size)
        self.resize_slider.pack(fill="x", pady=2)

        # Padding X
        padding_slider = tk.Scale(
            frame,
            from_=0,
            to=1000,
            resolution=10,
            orient="horizontal",
            length=100,         # total slider length
            width=25,           # thickness of the trough
            sliderlength=30,    # draggable handle size
            label="Padding X",
            command=self.layout_component.set_padding_x
        )
        padding_slider.set(self.layout_component.padding_x)
        padding_slider.pack(fill="x", pady=2)

        # Padding Y
        padding_slider = tk.Scale(
            frame,
            from_=0,
            to=1000,
            resolution=10,
            orient="horizontal",
            length=100,         # total slider length
            width=25,           # thickness of the trough
            sliderlength=30,    # draggable handle size
            label="Padding Y",
            command=self.layout_component.set_padding_y
        )
        padding_slider.set(self.layout_component.padding_y)
        padding_slider.pack(fill="x", pady=2)
