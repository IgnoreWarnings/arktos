import tkinter as tk
import random

from arktos import Playingfield, Pathfinder
from arktos.hardware import HardwareInterface
from .layout import GeometricLayout, GeometricLayoutBuilder
from .layout_component import LayoutComponent
from .pathfinding_component import PathfindingComponent
from .layout_control_component import LayoutControlComponent


class PathfinderView:

    def __init__(self, root, playingfield: Playingfield):
        self.root = root
        self.playingfield = playingfield

        start = random.choice(playingfield.starts)
        end = random.choice(playingfield.ends)
        self.pathfinder = Pathfinder(playingfield, start, end)

        # Container for playing field and controls
        playingfield_frame = tk.Frame(self.root)
        playingfield_frame.pack(side="right", fill="both", expand=True)

        # Layout
        layout = GeometricLayoutBuilder.layout(playingfield.interface.get_controllers()[0].get_hexagon())

        # Playingfield UI
        self.layout_component = LayoutComponent(
            playingfield_frame,
            layout
        )
        self.layout_component.pack(fill="both", expand=True)

        # Playingfield Control
        layout_control_component = LayoutControlComponent(
            playingfield_frame,
            self.layout_component
        )
        layout_control_component.pack(fill="x", side="bottom")

        # Sidebar
        sidebar = tk.Frame(self.root)
        sidebar.pack(side="left", fill="y")

        # Pathfinding UI
        PathfindingComponent(sidebar, self.pathfinder, self.color_path).pack(
            anchor="nw",
            padx=5,
            pady=5
        )

    def color_path(self):
        # ToDo: Proper Path removal
        self.layout_component.redraw()

        for hexagon in self.pathfinder.get_path():
            self.layout_component.set_hexagon_color(hexagon, "purple")


    def show(self):
        self.root.mainloop()
