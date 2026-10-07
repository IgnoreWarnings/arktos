import tkinter as tk

from arktos.hardware.mock_hardware import MockHardware

from gui.setup_view import SetupView

# Window
root = tk.Tk()
root.title("Arktos | HardwareSetupView")
root.geometry("1920x1080")

# Interface
mock_interface = MockHardware.from_size(15)

viewer = SetupView(root, mock_interface)
viewer.pack(fill="both", expand=True)

root.mainloop()
