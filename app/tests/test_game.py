import tkinter as tk

from gui.game_view import GameView
from arktos.game import Game
from .playingfields import fully_connected_hex
from gui.hardware_emulator_component import HardwareEmulatorComponent

playingfield = fully_connected_hex(width=6)
game = Game(playingfield)

# Window
root = tk.Tk()
root.title("Arktos | GameView")
root.geometry("1920x1080")

viewer = GameView(root, game)

hec = HardwareEmulatorComponent(root, playingfield.interface)
hec.pack(side="bottom", fill="both", expand=True)

root.mainloop()
