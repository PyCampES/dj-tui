from dataclasses import dataclass

import flx4py

from .model import StateController
from .ui import DjApp


class DDJ200(flx4py.DDJFlx4):
    def __init__(self):
        super().__init__("DDJ-200")


@dataclass
class App:
    ui: DjApp
    midi_controller: DDJ200
    state_controller: StateController

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
        set_volume(normalized_value, Deck(event.deck))

    def button_pressed(self, event: flx4py.ButtonEvent):
        if event.pressed:
            # We ignore button press
            return
        self.ui.play(event.deck)
        deck = Deck(event.deck)
        action = self.state_controller.get_action(deck)
        play_pause(action, deck)


def main():
    app = App(
        DjApp(),
        DDJ200(),
        StateController(),
    )
    app.run()


if __name__ == "__main__":
    main()
