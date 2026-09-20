import json

from .hardware_interface import HardwareInterface

class JSONProtocol:
    VERSION="2026.1"

    def command(self, command: str, args: str = ""):
        return f"{{\"command\": {command}, \"args\": {args}}}"

    def info(self):
        return self.command("info", Protocol.VERSION)
    
    def buttons(self):
        return self.command("buttons")
    
    def leds(self):
        return self.command("leds")
    
    def set_led(self):

