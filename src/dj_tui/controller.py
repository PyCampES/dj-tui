import flx4py
import time

from src.dj_tui.model import StateController
from audio import play_pause, set_volume, Deck

state_controller = StateController()
midi_controller = flx4py.DDJFlx4("DDJ-200")


@midi_controller.on_knob("CH_FADER")
def crossfader(event: flx4py.KnobEvent):
    # FIXME: normalize value
    normalized_value = event.value
    set_volume(normalized_value, Deck(event.deck))


@midi_controller.on_button("PLAY_PAUSE")
def button_pressed(event: flx4py.ButtonEvent):
    if event.pressed:
        # We ignore button press
        return
    deck = Deck(event.deck)
    action = state_controller.get_action(deck)
    play_pause(action, deck)


if __name__ == "__main__":
    with midi_controller:
        while True:
            time.sleep(1)
