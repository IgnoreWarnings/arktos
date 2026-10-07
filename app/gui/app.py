import tkinter as tk

from .setup_view import SetupView
from .game_view import GameView

from arktos.hardware.mock_hardware import MockHardware, MockButton
from arktos.hardware.can.can_hardware import CanHardware
from arktos.hardware.can.can_connection import CanConnection
from arktos.game import Game

class App:

    def run(self):
        root = tk.Tk()
        root.title("Arktos")
        root.geometry("1920x1080")

        can_connection = CanConnection()
        start_button = MockButton()
        interface = CanHardware.from_discovery(can_connection, start_button)
        #interface = MockHardware.from_size(15)

        def on_setup_complete(playingfield):
            self.setup_view.destroy()
            game = Game(playingfield)
            game_view = GameView(root, game)

        self.setup_view = SetupView(
            root,
            interface,
            on_complete=on_setup_complete,
        )

        self.setup_view.pack(fill="both", expand=True)

        root.mainloop()
