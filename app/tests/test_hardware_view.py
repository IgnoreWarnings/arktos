import tkinter as tk

from arktos.hardware.mock_hardware import MockHardware
from gui.hardware_view import HardwareView
from .playingfields import fully_connected_hex

# Window
root = tk.Tk()
root.title("Arktos | HardwareView")
root.geometry("1920x1080")

# View
playingfield = fully_connected_hex(width=3)
view = HardwareView(root, playingfield.interface)
view.pack(side="left", fill="both", expand=True)

root.mainloop()
