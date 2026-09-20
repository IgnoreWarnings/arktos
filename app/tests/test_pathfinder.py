import tkinter as tk

from gui.pathfinder_view import PathfinderView
from .playingfields import fully_connected_hex

playingfield = fully_connected_hex(width=5)

# Window
root = tk.Tk()
root.title("Arktos | PathfinderView")
root.geometry("1920x1080")

viewer = PathfinderView(root, playingfield)
viewer.show()
