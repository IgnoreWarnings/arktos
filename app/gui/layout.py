import math

from arktos import Orientations, Hexagon, Socket

"""
    Use GeometricLayoutBuilder to create objects
    Stores the position of hexagons and connectors in a 2D space.
"""
class GeometricLayout:
    """
        Use GeometricLayoutBuilder to create objects
    """
    def __init__(self, hexagon_map: dict[Hexagon, tuple], socket_map: dict[Socket, tuple], hex_size: int):
        self.hexagon_map: dict[Hexagon, tuple] = hexagon_map
        self.socket_map: dict[Socket, tuple] = socket_map
        self.hex_size: int = hex_size


class GeometricLayoutBuilder:
    @classmethod
    def __get_attach_position(cls, parent_x, parent_y, orientation: Orientations, size):
            dx, dy = {
                Orientations.TOP: (
                    0,
                    -math.sqrt(3) * size,
                ),
                Orientations.BOTTOM: (
                    0,
                    math.sqrt(3) * size,
                ),
                Orientations.TOP_RIGHT: (
                    1.5 * size,
                    -math.sqrt(3) * size / 2,
                ),
                Orientations.BOTTOM_RIGHT: (
                    1.5 * size,
                    math.sqrt(3) * size / 2,
                ),
                Orientations.TOP_LEFT: (
                    -1.5 * size,
                    -math.sqrt(3) * size / 2,
                ),
                Orientations.BOTTOM_LEFT: (
                    -1.5 * size,
                    math.sqrt(3) * size / 2,
                ),
            }[orientation]

            return parent_x + dx, parent_y + dy

    @classmethod
    def empty(cls) -> GeometricLayout:
        return GeometricLayout({}, {}, 100)

    @classmethod
    def layout(cls, start_hexagon: Hexagon, hex_size: int = 50) -> GeometricLayout:
        """
        This function places all hexagons which are connected via the start hexagon in a 2-dimensional space.
        One hexagon "island" will be generated.
            Implementation note: There might be a "simpler" recursive algorithm but the use of recusive functions is discouraged
        """
        placed_hexagons = {start_hexagon: (0, 0)}
        placed_connectors = {}
        unprocessed = [start_hexagon]
        while unprocessed:
            # Remove hexagon
            hexagon = unprocessed.pop(0)

            # For each hexagon side
            for socket in hexagon.sockets:
                # If there is a connected Hexagon
                if socket.peer:
                    # Get the neighbor
                    neighbor = socket.peer.owner

                    # Skip if already placed
                    if neighbor in placed_hexagons:
                        continue

                    # Determine position
                    parent_x, parent_y = placed_hexagons[hexagon]
                    x, y = GeometricLayoutBuilder.__get_attach_position(
                        parent_x, parent_y, socket.orientation, hex_size
                    )

                    # Save in placed with position
                    placed_hexagons[neighbor] = (x, y)

                    # Add the placed hexagon to the que to process its neighbors in the next iteration
                    unprocessed.append(neighbor)

        # Place sockets
        for hexagon, (parent_x, parent_y) in placed_hexagons.items():
            for socket in hexagon.sockets:
                x, y = GeometricLayoutBuilder.__get_attach_position(
                    parent_x, parent_y, socket.orientation, hex_size-hex_size/2
                )

                placed_connectors[socket] = (x,y)

        return GeometricLayout(placed_hexagons, placed_connectors, hex_size)

    @classmethod
    def resize(cls, layout: GeometricLayout, new_size):
        if not layout.hexagon_map:
            return GeometricLayoutBuilder.empty()

        return GeometricLayoutBuilder.layout(
            list(layout.hexagon_map.keys())[0],
            new_size
        )
