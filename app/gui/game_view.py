import tkinter as tk

from arktos import Game
from arktos.hardware import MockHardware
from .hardware_component import HardwareComponent
from .hardware_emulator_component import HardwareEmulatorComponent

class GameView:

    def __init__(self, root, game: Game):
        self.root = root
        self.game = game

        if isinstance(game.playingfield.interface, MockHardware):
            #HardwareEmulatorComponent(self.root, game.playingfield.interface).pack(side="right", fill="both", expand=True)
            pass

        # Sidebar
        sidebar = tk.Frame(self.root)
        sidebar.pack(side="left", fill="y", padx=10, pady=10)

        label = tk.Label(sidebar, text="Game Control", font=("Arial", 14, "bold"))
        label.pack(fill="x", pady=4)

        self.error_var = tk.StringVar(value=f"Errors: {game.error_count}")
        label = tk.Label(sidebar, textvariable=self.error_var, font=("Arial", 10))
        label.pack(fill="x", pady=4)

        self.game_state_var = tk.StringVar(value=f"Gamestate: {game.running}")
        label = tk.Label(sidebar, textvariable=self.game_state_var, font=("Arial", 10))
        label.pack(fill="x", pady=4)

        # # Start Button
        # finish_button = tk.Button(
        #     sidebar,
        #     text="Start Game",
        #     command=self.start_game,
        #     font=("Arial", 14, "bold"),
        #     bg="#4CAF50",
        # )
        # finish_button.pack(side="bottom", pady=(0, 100))

        self.update_vars()
        self.game.start_thread()

    def update_vars(self):
        self.error_var.set(f"Errors: {self.game.error_count}")
        self.game_state_var.set(f"Gamestate: {self.game.running}")

        self.root.after(100, self.update_vars)
        