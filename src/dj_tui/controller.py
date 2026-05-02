from sounddevice import play
import flx4py
import time

from .audio import play_pause, set_volume, Deck

controller = flx4py.DDJFlx4("DDJ-200")

@controller.on_knob("CH_FADER")
def crossfader(event: flx4py.KnobEvent):
    # FIXME: normalize value
    normalized_value = value
    set_volume(normalized_value, Deck(event.deck))


@controller.on_button("PLAY_PAUSE")
def button_pressed(event: flx4py.ButtonEvent):
    if event.pressed:
        # We ignore button press
        return

    # Flip status (from "PLAYING" to "PAUSED")
    # TODO: We need to track state
    action = ...
    play_pause(action, Deck(event.deck))


if __name__ == "__main__":
    with controller:
        while True:
            time.sleep(1)
