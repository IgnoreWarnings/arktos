import tkinter as tk

from .layout import GeometricLayout, GeometricLayoutBuilder
from .layout_component import LayoutComponent
from .layout_control_component import LayoutControlComponent

class LayoutView(tk.Frame):
    def __init__(self, parent, geometric_layout: GeometricLayout):
        super().__init__(parent)

        # Container for playing field and controls
        playingfield_frame = tk.Frame(self)
        playingfield_frame.pack(side="left", fill="both", expand=True)

        # Playingfield UI
        self.layout_component = LayoutComponent(
            playingfield_frame,
            geometric_layout,
        )
        self.layout_component.pack(side="left", fill="both", expand=True)

        self.layout_control_component = LayoutControlComponent(
            playingfield_frame,
            self.layout_component
        )
        self.layout_control_component.pack(side="right", anchor="n")
