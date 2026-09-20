from arktos import Playingfield, Hexagon, Orientations
from arktos.hardware import MockHardware

def snake(width=9, height=10):
    playingfield = Playingfield()

    # Create Hexagons
    for y in range(0, width):
        row_start = Hexagon()

        if playingfield.entrypoints:
            # Determine appending direction
            direction = (
                Orientations.TOP_LEFT if y % 2 == 0 else Orientations.BOTTOM_LEFT
            )

            # Connect to end of previous row
            last_hexagon = playingfield.entrypoints[-1]
            last_hexagon.attach_oposing(row_start.socket_by_orientation(direction))

        playingfield.entrypoints.append(row_start)

        # Substract row start hexagon
        for x in range(0, height - 1):
            # Determine appending direction
            direction = Orientations.TOP if y % 2 == 0 else Orientations.BOTTOM

            # Add new hexagon
            hexagon = Hexagon()

            # Connect to previous Hexagon
            last_hexagon = playingfield.entrypoints[-1]
            last_hexagon.attach_oposing(hexagon.socket_by_orientation(direction))

            # Last of row is start or end
            if x == height - 2:
                at_bottom = y % 2 == 0
                if at_bottom:
                    playingfield.starts.append(hexagon)
                else:
                    playingfield.ends.append(hexagon)

            # Add to playingfield
            playingfield.entrypoints.append(hexagon)

    return playingfield

def basic():
    playingfield = Playingfield()

    # Start
    hexagon_start = Hexagon()
    playingfield.entrypoints.append(hexagon_start)

    # Top
    hexagon_top = Hexagon()
    hexagon_start.attach_oposing(hexagon_top.socket_by_orientation(Orientations.BOTTOM))
    playingfield.entrypoints.append(hexagon_top)

    # 1-Bottom
    hexagon_bottom = Hexagon()
    hexagon_start.attach_oposing(hexagon_bottom.socket_by_orientation(Orientations.TOP))
    playingfield.entrypoints.append(hexagon_bottom)

    # BOTTOM_RIGHT
    hexagon_bottom_right = Hexagon()
    hexagon_start.attach_oposing(
        hexagon_bottom_right.socket_by_orientation(Orientations.TOP_LEFT)
    )
    playingfield.entrypoints.append(hexagon_bottom_right)

    # TOP_LEFT
    hexagon_top_left = Hexagon()
    hexagon_start.attach_oposing(
        hexagon_top_left.socket_by_orientation(Orientations.BOTTOM_RIGHT)
    )
    playingfield.entrypoints.append(hexagon_top_left)

    # 2-Bottom
    hexagon_bottom2 = Hexagon()
    hexagon_bottom.attach_oposing(hexagon_bottom2.socket_by_orientation(Orientations.TOP))
    playingfield.entrypoints.append(hexagon_bottom2)

    return Playingfield

def fully_connected_hex(width=6):
    hexes = {}

    radius = width - 1

    for q in range(-radius, radius + 1):
        for r in range(-radius, radius + 1):

            s = -q - r

            if abs(s) <= radius:
                hexes[(q, r)] = Hexagon()

    directions = [
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, 0),
        (-1, 1),
        (0, 1),
    ]

    DIRECTION_TO_ORIENTATION = {
        (0, -1): Orientations.TOP,
        (1, -1): Orientations.TOP_RIGHT,
        (1, 0): Orientations.BOTTOM_RIGHT,
        (0, 1): Orientations.BOTTOM,
        (-1, 1): Orientations.BOTTOM_LEFT,
        (-1, 0): Orientations.TOP_LEFT,
    }

    for (q, r), hexagon in hexes.items():

        for dq, dr in directions:

            neighbour = hexes.get((q + dq, r + dr))

            if neighbour:
                direction = DIRECTION_TO_ORIENTATION[(dq, dr)]
                socket = neighbour.socket_by_orientation(Orientations.opposite(direction))
                hexagon.attach_oposing(socket)

    hexagon_list = []
    for (q, r), hexagon in hexes.items():
        hexagon_list.append(hexagon)

    interface = MockHardware.from_list(hexagon_list)
    playingfield = Playingfield(interface, starts=[hexagon_list[0]], ends=[hexagon_list[-1]])

    return playingfield
