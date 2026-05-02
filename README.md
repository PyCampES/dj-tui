# DJ Tui

![A PyCamp project](https://img.shields.io/badge/pycamp-project-green?logo=python)

DJ mixer on the terminal.

To launch it, clone the repository and do

```
$ uv run dj-tui
```

# Development notes

## Inspiration

Open source, multi-platform DJ software exists: [Mixxx](https://mixxx.org/).

We want to do something similar, with a Terminal User Interface (TUI).
Our framework of choice is [Textual](https://textual.textualize.io/).

## MVP

A Python package that can be installed as follows

```
$ pip install dj-tui
```

That launches a TUI with the following capabilities:
- Loading an MP3 on the left deck
- Loading an MP3 on the right deck
- Setting and playing a single cue point on the left and right track
- Controlling the volume of the left and right track independently
- These actions can be performed with a DJ controller, for example a Pioneer DDJ-200,
  as well as with basic keyboard shortcuts (for those who don't possess one)

## Extras

- Display waveform of tracks
- Visual representation of the jog wheels
- Other audio formats
- Tempo controls
- Equalizers (knobs to tweak low, mid, high frequencies)
- ...? (Ideas welcome!)

## Resources

MIDI and DJ controllers:
- https://manual.mixxx.org/2.4/en/hardware/controllers/pioneer_ddj_200
- https://web.archive.org/web/20250910180949/https://www.pioneerdj.com/-/media/pioneerdj/software-info/controller/ddj-200/ddj-200_midi_message_list_e2.pdf
- https://pypi.org/project/mido/
- https://pypi.org/project/flx4py/ (Pioneer DDJ-FLX4)

TUI inspiration:
- https://github.com/oleksis/awesome-textualize-projects

Playing audio:
- https://pypi.org/project/sounddevice/
- https://pypi.org/project/soundfile/

## Architecture

### Sound layer

```python
from enum import Enum, auto

class Deck(Enum):
    LEFT = auto()
    RIGHT = auto()


class Action(Enum):
    PLAY = auto()
    PAUSE = auto()


def play_pause(action: Action, deck: Deck) -> None:
    """
    Params:
        action: Action.PLAY or Action.PAUSE.
        deck: Deck.LEFT or Deck.RIGHT.
    """
    ...


def set_volume(value: int, deck: Deck) -> None:
    """
    Params:
        value: Volume from 0 to 126.
        deck: Deck.LEFT or Deck.RIGHT.
    """
    ...

def load_song(path: Path, deck: Deck) -> None:
    """
    Params:
        path: Path of the song to be loaded.
        deck: Deck.LEFT or Deck.RIGHT.
    """
    ...
```

Example:

```python3
from dj_tui.audio import Deck, load_song
from pathlib import Path

song_path = Path("/home/juanlu/Music/Avicii - Levels (Radio Edit).mp3")
load_song(song_path, Deck.LEFT)
```
