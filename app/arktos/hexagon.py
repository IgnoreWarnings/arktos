from __future__ import annotations
from typing import Optional

from enum import Enum

class Orientations(Enum):
    TOP = 0
    TOP_RIGHT = 1
    BOTTOM_RIGHT = 2
    BOTTOM = 3
    BOTTOM_LEFT = 4
    TOP_LEFT = 5

    @classmethod
    def opposite(cls, orientation):
        return {
            cls.TOP: cls.BOTTOM,
            cls.BOTTOM: cls.TOP,
            cls.TOP_RIGHT: cls.BOTTOM_LEFT,
            cls.BOTTOM_RIGHT: cls.TOP_LEFT,
            cls.TOP_LEFT: cls.BOTTOM_RIGHT,
            cls.BOTTOM_LEFT: cls.TOP_RIGHT,
        }[orientation]

class Socket:
    def __init__(
        self, owner: Hexagon, orientation: Orientations, peer: Optional[Socket] = None
    ):
        self.owner = owner
        self.orientation = orientation
        self.peer = peer

    def connect(self, peer: Socket):
        self.peer = peer
        # Add this socket in the peer
        peer.peer = self

    def disconnect(self):
        # Remove this socket in other socket
        self.peer = None

        # Remove other socket
        self.peer = None

    def __str__(self):
        return f"Socket {self.orientation} connected to { self.peer.orientation if self.peer is not None else None }"


class Hexagon:

    def __init__(self):
        self.sockets: list[Socket] = []
        for orientation in Orientations:
            self.sockets.append(Socket(self, orientation))

    def neighbors(self) -> list[Hexagon]:
        neighbors: list[Hexagon] = []
        for socket in self.sockets:
            if socket.peer:
                neighbors.append(socket.peer.owner)

        return neighbors

    def socket_by_orientation(self, orientation: Orientations) -> Socket | None:
        for socket in self.sockets:
            if socket.orientation == orientation:
                return socket
    
    '''
        Find next free socket starting from top going clockwise
    '''
    def find_free_socket_clockwise(self) -> Optional[Hexagon]:
        for socket in self.sockets:
            if not socket.peer:
                return socket.peer
        return None

    def attach_oposing(self, socket: Socket):
        orientation = Orientations.opposite(socket.orientation)
        self.socket_by_orientation(orientation).connect(socket)
