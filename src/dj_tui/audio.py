from enum import Enum, IntEnum, auto
from pathlib import Path

import pygame


class Deck(IntEnum):
    LEFT = 1
    RIGHT = 2


class Action(Enum):
    PLAY = auto()
    PAUSE = auto()


class AudioController:
    def __init__(self):
        pygame.mixer.init()
        self.chan_0 = pygame.mixer.Channel(0)
        self.chan_1 = pygame.mixer.Channel(1)
        self.sound_0 = None
        self.sound_1 = None
        self.playing_0 = False
        self.playing_1 = False

    def play_pause(self, action: Action, deck: Deck) -> None:
        """Play and pause action on a specific deck.

        Params:
            action: Action.PLAY or Action.PAUSE.
            deck: Deck.LEFT or Deck.RIGHT.
        """
        if deck is Deck.LEFT:
            if self.sound_0 is None:
                raise RuntimeError
            elif action is Action.PAUSE:
                self.chan_0.pause()
            elif action is Action.PLAY:
                if self.playing_0:
                    self.chan_0.unpause()
                else:
                    self.chan_0.play(self.sound_0)
                    self.playing_0 = True
            else:
                raise ValueError("Invalid action %s", action)

        elif deck is Deck.RIGHT:
            if self.sound_1 is None:
                raise RuntimeError
            elif action is Action.PAUSE:
                self.chan_1.pause()
            elif action is Action.PLAY:
                if self.playing_1:
                    self.chan_1.unpause()
                else:
                    self.chan_1.play(self.sound_1)
                    self.playing_1 = True
            else:
                raise ValueError("Invalid action %s", action)
        else:
            raise ValueError("Invalid deck")
        ...

    def set_volume(self, value: float, deck: Deck) -> None:
        """Set volume on a specific deck.

        Params:
            value: Volume from 0 to 1.
            deck: Deck.LEFT or Deck.RIGHT.
        """
        if deck is Deck.LEFT:
            self.chan_0.set_volume(value)
        elif deck is Deck.RIGHT:
            self.chan_1.set_volume(value)
        else:
            raise ValueError("Invalid deck")
        ...

    def load_song(self, path: Path, deck: Deck) -> None:
        """Load an audio file to a specific deck.

        Params:
            path: Path of the song to be loaded.
            deck: Deck.LEFT or Deck.RIGHT.
        """
        sound = pygame.mixer.Sound(path)
        if deck is Deck.LEFT:
            self.sound_0 = sound
        elif deck is Deck.RIGHT:
            self.sound_1 = sound
        else:
            raise ValueError("Invalid deck")
