import threading
import random
import time

from .hardware.hardware_interface import RGBColor
from .playingfield import Playingfield
from .pathfinder import Pathfinder
from .animation_player import AnimationPlayer, AnimationQueue
from .animation import AnimationRainbow, AnimationFadeAll, AnimationPulse, AnimationPath, AnimationWater, AnimationWaves
from .colors import COLORS

class Game():
    def __init__(self, playingfield: Playingfield) -> None:
        self.playingfield = playingfield
        self.error_count = 0
        self.running = False

        # Pathfinder
        start = random.choice(playingfield.starts)
        end = random.choice(playingfield.ends)
        self.pathfinder = Pathfinder(playingfield, start, end)

    def reset(self):
        self.error_count = 0
        self.pathfinder.reset_path()

    def game_loop(self):
        while(True):
            self.wait_for_start()
            self.play()
            self.reset()
    
    def wait_for_start(self):
        interface = self.playingfield.interface

        # Animation
        animation_player = AnimationPlayer()
        animation_queue = AnimationQueue(animation_player)

        animation_queue.queue.append(AnimationWaves(interface.get_controllers()))

        animation_queue.queue.append(AnimationRainbow(interface))

        animation_queue.queue.append(AnimationWater(interface.get_controllers()))
        animation_queue.queue.append(AnimationWater(interface.get_controllers()))

        animation_queue.queue.append(AnimationFadeAll(interface, RGBColor(0,0,0), RGBColor(255,255,0), 400))
        animation_queue.queue.append(AnimationFadeAll(interface, RGBColor(255,255,0), RGBColor(0,255,255), 200))
        animation_queue.queue.append(AnimationFadeAll(interface, RGBColor(0,255,255), RGBColor(255,0,255), 200))
        animation_queue.queue.append(AnimationFadeAll(interface, RGBColor(255,0,255), RGBColor(0,255,255), 200))
        animation_queue.queue.append(AnimationFadeAll(interface, RGBColor(0,255,255), RGBColor(255,255,0), 200))
        animation_queue.queue.append(AnimationFadeAll(interface, RGBColor(255,255,0), RGBColor(0,255,255), 200))
        animation_queue.queue.append(AnimationFadeAll(interface, RGBColor(0,255,255), RGBColor(255,0,255), 200))
        animation_queue.queue.append(AnimationFadeAll(interface, RGBColor(255,0,255), RGBColor(0,255,255), 200))
        animation_queue.queue.append(AnimationFadeAll(interface, RGBColor(0,255,255), RGBColor(255,255,0), 200))
        animation_queue.queue.append(AnimationFadeAll(interface, RGBColor(255,255,0), RGBColor(255,255,255), 400))

        animation_queue.play(looping=True, max_animation_duration=10.0)
        
        # Wait for start
        while(not interface.get_start_button().is_pressed()):
            time.sleep(0.01)

        animation_queue.stop()
        self.play()

    def play(self):
        self.running = True

        # Determine path
        while not self.pathfinder.finished():
            self.pathfinder.step()

        # Turn all off
        controllers = self.playingfield.interface.get_controllers()
        for controller in controllers:
            controller.get_led().set_color(RGBColor(0,0,0))

        controllers = []
        for hexagon in self.pathfinder.get_path():
            for controller in self.playingfield.interface.get_controllers():
                if controller.hexagon == hexagon:
                    controllers.append(controller)
                    break

        for controller in self.playingfield.interface.get_controllers():
            controller.get_led().set_color(COLORS.BLUE)

        animation_player = AnimationPlayer()
        animation_player.set_animation(AnimationPath(controllers))
        animation_player.play(frame_delay=0.3, looping=True)

        # Await button press
        initiator = None
        while(initiator == None):
            for controller in controllers:
                if controller.get_button().is_pressed():
                    initiator = controller
            time.sleep(0.01)

        animation_player.stop()

        animation_player = AnimationPlayer()
        animation_player.set_animation(AnimationWaves(self.playingfield.interface.get_controllers()))
        animation_player.play(looping=True)

        # Move Detection
        abort = False
        current_position = None
        controllers = self.playingfield.interface.get_controllers()
        correct = []
        while not abort and current_position != self.pathfinder.end:
            # Await button press
            initiator = None
            while(initiator == None):
                for controller in controllers:
                    if controller.get_button().is_pressed():
                        initiator = controller
                time.sleep(0.01)

            # Wrong move
            if initiator.get_hexagon() not in self.pathfinder.path:
                animation_player.stop()
                animation_player = AnimationPlayer()
                animation_player.set_animation(AnimationPulse(self.playingfield.interface, initiator))
                animation_player.play()
                self.error_count += 1
            
            # Correct move
            else:
                correct.append(initiator)
                left = [h for h in self.playingfield.interface.get_controllers() if h not in correct]
                animation_player.stop()
                animation_player = AnimationPlayer()
                animation_player.set_animation(AnimationWaves(left))
                animation_player.play(looping=True)

                initiator.get_led().set_color(COLORS.RED)
                current_position = initiator.get_hexagon()
        
        animation_player.stop()
        self.running = False

    def start_thread(self):
        t = threading.Thread(target=self.game_loop, daemon=True)
        t.start()

    
