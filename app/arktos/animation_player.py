import threading
import time

from .hardware.hardware_interface import HardwareInterface
from .animation import Animation

class AnimationPlayer:
    def __init__(self):
        self.animation: Animation | None = None

        self.is_playing = False
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def get_is_playing(self):
        return self.is_playing

    def set_animation(self, animation: Animation):
        self.animation = animation

    def play(self, frame_delay: float = 0.01, looping: bool = False):
        if self.animation is None or self.is_playing:
            return

        self._stop_event.clear()
        self.is_playing = True

        self._thread = threading.Thread(
            target=self._run,
            args=(frame_delay, looping),
            daemon=True,
        )
        self._thread.start()

    def _run(self, frame_delay: float, looping: bool):
        try:
            while not self._stop_event.is_set():
                if not self.animation.next_frame():
                    if looping:
                        self.animation.reset()
                    else:
                        break

                time.sleep(frame_delay)
        finally:
            self.is_playing = False

    '''Returns True if ended properly. Returns false if Timeout reached.'''
    def wait_for_animation_end(self, timeout: float | None = None) -> bool:
        if self._thread is None:
            return True

        self._thread.join(timeout)
        return not self._thread.is_alive()

    def stop(self):
        self._stop_event.set()


class AnimationQueue:
    def __init__(self, animation_player: AnimationPlayer):
        self.animation_player = animation_player
        self.queue: list[Animation] = []

        self.current_index = 0
        self.is_playing = False

    def enqueue(self, animation: Animation):
        self.queue.append(animation)

    def play(self, looping=False, max_animation_duration=10.0):
        if self.is_playing:
            return

        self.is_playing = True

        self._thread = threading.Thread(
            target=self._run,
            args=(looping, max_animation_duration),
            daemon=True,
        )
        self._thread.start()

    def stop(self):
        self.is_playing = False
        self.animation_player.stop()

    def _run(self, looping, max_animation_duration):
        while self.is_playing and self.current_index < len(self.queue):
            animation = self.queue[self.current_index]
            animation.reset()

            self.animation_player.set_animation(animation)
            self.animation_player.play()

            finished = self.animation_player.wait_for_animation_end(
                timeout=max_animation_duration
            )

            # Don't advance if stopped.
            if not self.is_playing:
                break

            self.current_index += 1

            if looping and self.current_index == len(self.queue):
                self.current_index = 0

        self.current_index = 0
        self.is_playing = False