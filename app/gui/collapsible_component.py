import tkinter as tk


class CollapsibleInfo(tk.Frame):
    def __init__(self, parent, title="Info", text="", **kwargs):
        super().__init__(parent, **kwargs)
        self.title = title

        self.expanded = False

        self.button = tk.Button(
            self,
            text=f"▶ {self.title}",
            anchor="w",
            command=self.toggle,
            font=("Arial", 16)
        )
        self.button.pack(fill="x")

        self.info_frame = tk.Frame(self)

        self.label = tk.Label(
            self.info_frame,
            text=text,
            justify="left",
            anchor="w",
            wraplength=400,
            padx=10,
            pady=10,
            font=("Arial", 14)
        )
        self.label.pack(fill="both")

    def toggle(self):
        self.expanded = not self.expanded

        if self.expanded:
            self.button.config(text=f"▼ {self.title}")
            self.info_frame.pack(fill="x")
        else:
            self.button.config(text=f"▶ {self.title}")
            self.info_frame.pack_forget()
