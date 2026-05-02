import time

import flx4py

from .audio import Deck, play_pause, set_volume
from .model import StateController

state_controller = StateController()
midi_controller = flx4py.DDJFlx4("DDJ-200")


@midi_controller.on_knob("CH_FADER")
def crossfader(event: flx4py.KnobEvent):
    normalized_value = event.value * 100
    set_volume(normalized_value, Deck(event.deck))


@midi_controller.on_button("PLAY_PAUSE")
def button_pressed(event: flx4py.ButtonEvent):
    if event.pressed:
        # We ignore button press
        return
    deck = Deck(event.deck)
    action = state_controller.get_action(deck)
    play_pause(action, deck)


def main():
    with midi_controller:
        while True:
            time.sleep(1)


if __name__ == "__main__":
    main()
