import random
from typing import Optional

from .hexagon import Hexagon
from .playingfield import Playingfield

class Pathfinder:
    def __init__(self, playingfield: Playingfield, start: Hexagon, end: Hexagon, curviness=0.1):
        self.playingfield = playingfield
        self.start = start
        self.end = end
        self.curviness = curviness

        self.path: list[Hexagon] = [start]
        self.dead_ends: list[Hexagon] = []

    def get_path(self):
        return self.path

    def set_curviness(self, curviness):
        self.curviness = curviness

    def reset_path(self):
        self.path = [self.start]
        self.dead_ends = []

    def __touches_path(self, hexagon: Hexagon):
        touches_path = False
        for path_hexagon in self.path[0:-1]:
            if hexagon in path_hexagon.neighbors():
                touches_path = True
                break

        return touches_path
        
    def __next_hexagon(self, current_hexagon: Hexagon) -> Optional[Hexagon]:
        candidates = []
        for neighbor in current_hexagon.neighbors():

            # Already in path
            if neighbor in self.path:
                continue

            # Known dead end
            elif neighbor in self.dead_ends:
                continue

            # Touches path (except current)
            elif self.__touches_path(neighbor):
                continue

            candidates.append(neighbor)

        # No candidates found
        if not candidates:
            return None
        
        # Prevent straight lines
        def direction(origin: Hexagon, destination: Hexagon):
            orientation = None
            for socket in destination.sockets:
                if socket.peer:
                    if socket.peer.owner == origin:
                        orientation = socket.orientation
                        break

            return orientation

        # No previous WEIGHT on first connection
        if(len(self.path) < 2):
            return random.choice(candidates)

        # Build weights
        WEIGHT_NORMAL = 100
        WEIGHT_PUNISHMENT =  WEIGHT_NORMAL * self.curviness
        weights = []
        previous_direction = direction(self.path[-2], self.path[-1])
        for candidate in candidates:
            candidate_direction = direction(self.path[-1], candidate)

            if candidate_direction == previous_direction:
                weights.append(WEIGHT_PUNISHMENT)
            else:
                weights.append(WEIGHT_NORMAL)

        # Choose next_hexagon
        choice = random.choices(candidates, weights=weights, k=1)[0]
        return choice
    
    def finished(self):
        return self.path[-1] == self.end

    def step(self):
        if self.finished():
            return
        
        next_hexagon = self.__next_hexagon(self.path[-1])

        if not next_hexagon:
            popped = self.path.pop()
            self.dead_ends.append(popped)
            return

        self.path.append(next_hexagon)