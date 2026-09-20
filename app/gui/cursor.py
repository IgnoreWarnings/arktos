from .drawing import HexagonDrawer

class Cursor:
    def __init__(self, canvas):
        self.canvas = canvas
        self.hexagon = None
        self.x = 0
        self.y = 0
        self.size = 0
        self.id = 0
        self.color = "yellow"
        
    def clear(self):
        try:
            polygon_id, label_id = self.hexagon
            self.canvas.delete(polygon_id)
            self.canvas.delete(label_id)

        except:
            print("No element to be deleted on canvas")

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_size(self, size):
        self.size = size

    def set_id(self, id):
        self.id = id
    
    def set_color(self, color):
        self.color = color

    def draw(self):
        self.hexagon = HexagonDrawer(self.canvas).draw(self.x, self.y, self.size, self.id, color=self.color)
