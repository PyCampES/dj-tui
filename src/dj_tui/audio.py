from enum import Enum, IntEnum, auto
from pathlib import Path


class Deck(IntEnum):
    LEFT = 1
    RIGHT = 2


class Action(Enum):
    PLAY = auto()
    PAUSE = auto()


def play_pause(action: Action, deck: Deck) -> None:
    """Play and pause action on a specific deck.

    Params:
        action: Action.PLAY or Action.PAUSE.
        deck: Deck.LEFT or Deck.RIGHT.
    """
    ...


def set_volume(value: int, deck: Deck) -> None:
    """Set volume on a specific deck.

    Params:
        value: Volume from 0 to 126.
        deck: Deck.LEFT or Deck.RIGHT.
    """
    ...


def load_song(path: Path, deck: Deck) -> None:
    """Load an audio file to a specific deck.

    Params:
        path: Path of the song to be loaded.
        deck: Deck.LEFT or Deck.RIGHT.
    """
    ...
