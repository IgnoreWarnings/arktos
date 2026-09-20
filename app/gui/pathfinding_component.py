import tkinter as tk
import time

class PathfindingComponent(tk.Frame):
    def __init__(self, parent, pathfinder, callback_path_update):
        super().__init__(parent)

        self.pathfinder = pathfinder
        self.callback_path_update = callback_path_update
        
        # Group
        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10, anchor="n")

        # Label
        label = tk.Label(frame, text="Pathfinding", font=("Arial", 12, "bold"))
        label.pack(fill="x", pady=4)
        
        # Slider
        slider_curvy = tk.Scale(
            frame,
            from_=0.05,
            to=10,
            resolution=0.05,
            orient="horizontal",
            length=300,         # total slider length
            width=25,           # thickness of the trough
            sliderlength=30,    # draggable handle size
            label="Algorithm curviness",
            command=self.on_slider_change
        )

        slider_curvy.pack(fill="x", pady=2)
        
        # Buttons
        button_step = tk.Button(frame, text="Step", font=("Arial", 16), anchor="nw", command=self.on_button_path_step)
        button_step.pack(fill="x", pady=2)

        button_path_visual = tk.Button(frame, text="Visual algorithm", font=("Arial", 16), anchor="nw", command=self.on_button_pathfinding_visual)
        button_path_visual.pack(fill="x", pady=2)

        button_path = tk.Button(frame, text="Non-visual", font=("Arial", 16), anchor="nw", command=self.on_button_pathfinding)
        button_path.pack(fill="x", pady=2)

    def on_slider_change(self, value):
        self.pathfinder.set_curviness(float(value))

    def on_button_path_step(self):
        if self.pathfinder.finished():
            self.pathfinder.reset_path()

        self.pathfinder.step()
        self.callback_path_update()

    def on_button_pathfinding_visual(self):
        self.pathfinder.reset_path()
        while not self.pathfinder.finished():
            self.pathfinder.step()
            self.callback_path_update()
            self.update_idletasks()  # Update the GUI to reflect changes
            time.sleep(0.1) # ToDo: This is bad because it blocks the main thread

    def on_button_pathfinding(self):
        self.pathfinder.reset_path()

        while not self.pathfinder.finished():
            self.pathfinder.step()

        self.callback_path_update()
