import logging
from dataclasses import dataclass
from pathlib import Path

import flx4py

from .audio import AudioController, Deck
from .model import StateController
from .ui import DjApp

logger = logging.getLogger(__name__)


class DDJ200(flx4py.DDJFlx4):
    def __init__(self):
        super().__init__("DDJ-200")


@dataclass
class App:
    ui: DjApp
    midi_controller: DDJ200
    state_controller: StateController
    audio_controller: AudioController

    def run(self):
        self.midi_controller.on_knob(
            "CH_FADER",
            callback=self.crossfader,
        )
        self.midi_controller.on_button(
            "PLAY_PAUSE",
            callback=self.button_pressed,
        )
        self.midi_controller.start()
        self.ui.run()

    def crossfader(self, event: flx4py.KnobEvent):
        normalized_value = event.value * 100
        self.ui.set_volume(event.deck, normalized_value)
        self.audio_controller.set_volume(normalized_value, Deck(event.deck))

    def button_pressed(self, event: flx4py.ButtonEvent):
        if event.pressed:
            # We ignore button press
            return
        self.ui.play(event.deck)
        deck = Deck(event.deck)
        action = self.state_controller.get_action(deck)
        # song_path = self.ui.query_one(f"#deck-0").track_name
        try:
            self.audio_controller.load_song(
                Path("/home/juanlu/Music/Without You (feat. Usher) (Radio Edit).mp3"),
                deck,
            )
            self.audio_controller.play_pause(action, deck)
        except Exception as exc:
            logger.exception("OH NO", exc_info=exc)


def main():
    logging.basicConfig(level=logging.DEBUG)
    app = App(
        DjApp(),
        DDJ200(),
        StateController(),
        AudioController(),
    )
    app.run()


if __name__ == "__main__":
    main()
