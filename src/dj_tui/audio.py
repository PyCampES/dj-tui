from typing_extensions import Never
from enum import Enum, IntEnum, auto
from pathlib import Path
import pygame


class Deck(IntEnum):
    LEFT = 1
    RIGHT = 2


class Action(Enum):
    PLAY = auto()
    PAUSE = auto()

class AudioController():

    def check_audio_mixer_started(self,):
        '''Check if pygame audio mixer is running, start it
        if it is not. 
        Returns the two audio channels.
        '''
        if pygame.mixer.get_init() is None:
            pygame.mixer.init()
            self.chan_0 = pygame.mixer.Channel(0)
            self.chan_1 = pygame.mixer.Channel(1)

    def play_pause(self, action: Action, deck: Deck) -> None:
        """Play and pause action on a specific deck.

        Params:
            action: Action.PLAY or Action.PAUSE.
            deck: Deck.LEFT or Deck.RIGHT.
        """
        self.check_audio_mixer_started()
        ...


    def set_volume(self, value: int, deck: Deck) -> None:
        """Set volume on a specific deck.

        Params:
            value: Volume from 0 to 126.
            deck: Deck.LEFT or Deck.RIGHT.
        """
        self.check_audio_mixer_started()
        ...


    def load_song(self, path: Path, deck: Deck) -> None:
        """Load an audio file to a specific deck.

        Params:
            path: Path of the song to be loaded.
            deck: Deck.LEFT or Deck.RIGHT.
        """
        self.check_audio_mixer_started()
        if deck is Deck.LEFT:
            ...
        elif deck is Deck.RIGHT:
            ...
        else:
            raise ValueError("Invalid deck")
