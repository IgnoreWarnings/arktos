import math

class HexagonDrawer():
    def __init__(self, canvas) -> None:
        self.canvas = canvas

    @classmethod
    def hexagon_points(cls, cx, cy, radius):
        points = []

        for i in range(6):
            angle = math.radians(60 * i)
            points.extend(
                [cx + radius * math.cos(angle), cy + radius * math.sin(angle)]
            )

        return points

    def draw_hexagon(self, x, y, size, color):
        points = HexagonDrawer.hexagon_points(x, y, size)
        hex_id = self.canvas.create_polygon(
            points, fill=color, outline="black", width=4, tags=("hex")
        )
        return hex_id

    def draw_hex_label(self, x, y, id):
        text_id = self.canvas.create_text(x, y, text=f"ID: {id}", tags=("hex"))
        return text_id
    
    def draw(self, x, y, size, id, color="grey"):
        polygon_id = self.draw_hexagon(x, y, size, color)
        label_id = self.draw_hex_label(x, y, id)
        return polygon_id, label_id # TODO: refactor this to not return, then just use members

    def draw_socket(self, x, y, angle, length, width, color="grey", inset=10):
        # Unit vector along the edge
        dx = math.cos(angle)
        dy = math.sin(angle)

        # Perpendicular vector
        px = -dy
        py = dx

        # Move socket inward
        x += px * inset
        y += py * inset

        hl = length / 2
        hw = width / 2

        points = [
            x - dx*hw - px*hl, y - dy*hw - py*hl,
            x + dx*hw - px*hl, y + dy*hw - py*hl,
            x + dx*hw + px*hl, y + dy*hw + py*hl,
            x - dx*hw + px*hl, y - dy*hw + py*hl,
        ]

        socket_id = self.canvas.create_polygon(
            points,
            fill=color,
            outline="",
            tags=("socket")
        )
        return socket_id