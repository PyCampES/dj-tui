from pathlib import Path
from typing import Callable

from rich.text import Text
from textual import events, on, work
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Footer, Header, Label, Static
from textual_fspicker import FileOpen


class Deck(Container):
    track_name: reactive[str] = reactive("Sin pista cargada", init=False)
    is_playing: reactive[bool] = reactive(False, init=False)

    def __init__(self, deck_num: int) -> None:
        super().__init__(id=f"deck-{deck_num}", classes="deck")
        self.deck_num = deck_num

    def compose(self) -> ComposeResult:
        yield Static("∿∿∿∿  ∿∿∿∿  ∿∿∿∿", classes="waveform")
        yield Label("Sin pista cargada", classes="track-name")
        with Horizontal():
            yield Button("▶  Play", id=f"play-{self.deck_num}", classes="play-btn")
            yield Button(
                "📁  Cargar pista", id=f"load-{self.deck_num}", classes="load-btn"
            )
            yield VolumeFader(id=f"fader-{self.deck_num}")

    def watch_track_name(self, name: str) -> None:
        self.query_one(".track-name", Label).update(name)

    def watch_is_playing(self, playing: bool) -> None:
        btn = self.query_one(f"#play-{self.deck_num}", Button)
        btn.label = "⏸  Pause" if playing else "▶  Play"
        btn.variant = "success" if playing else "default"


class VolumeSlider(Widget):
    volume: reactive[int] = reactive(50)

    class Changed(Message):
        def __init__(self, volume: int) -> None:
            super().__init__()
            self.volume = volume

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._dragging = False

    def render(self) -> Text:
        h = self.size.height
        if h <= 0:
            return Text("")

        thumb_row = round((1 - self.volume / 100) * max(1, h - 1))
        text = Text()
        for i in range(h):
            if i < thumb_row:
                text.append("  │  ", style="dim")
            elif i == thumb_row:
                text.append("══█══", style="bold")
            else:
                text.append("  █  ")
            if i < h - 1:
                text.append("\n")
        return text

    def _y_to_volume(self, y: int) -> int:
        h = self.size.height
        if h <= 1:
            return self.volume
        clamped = max(0, min(h - 1, y))
        return round((1 - clamped / (h - 1)) * 100)

    def watch_volume(self, vol: int) -> None:
        self.post_message(self.Changed(vol))

    def on_mouse_down(self, event: events.MouseDown) -> None:
        self._dragging = True
        self.capture_mouse()
        self.volume = self._y_to_volume(event.y)

    def on_mouse_move(self, event: events.MouseMove) -> None:
        if self._dragging:
            self.volume = self._y_to_volume(event.y)

    def on_mouse_up(self, event: events.MouseUp) -> None:
        self._dragging = False
        self.release_mouse()


class VolumeFader(Container):
    def compose(self) -> ComposeResult:
        yield Label("VOL", classes="fader-cap")
        yield VolumeSlider(id="slider")
        yield Label("50%", id="vol-label")

    @on(VolumeSlider.Changed)
    def on_slider_changed(self, event: VolumeSlider.Changed) -> None:
        self.query_one("#vol-label", Label).update(f"{event.volume}%")

    @property
    def volume(self) -> int:
        return self.query_one(VolumeSlider).volume

    @volume.setter
    def volume(self, value: int) -> None:
        self.query_one(VolumeSlider).volume = max(0, min(100, value))


class DjApp(App):
    CSS_PATH = "dj.tcss"
    TITLE = "🎧 DJ Booth"
    on_track_loaded: Callable[[int, Path], None] = staticmethod(
        lambda deck, path: None
    )

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="booth"):
            yield Deck(1)
            yield Deck(2)
        yield Footer()

    @on(Button.Pressed, ".play-btn")
    def on_play(self, event: Button.Pressed) -> None:
        num = event.button.id.split("-")[1]
        self.play(num)

    def play(self, num) -> None:
        deck = self.query_one(f"#deck-{num}", Deck)
        deck.is_playing = not deck.is_playing
        deck.watch_is_playing(deck.is_playing)

    def set_volume(self, deck_num, value) -> None:
        self.query_one(f"#fader-{deck_num}", expect_type=VolumeFader).volume = value

    @on(Button.Pressed, ".load-btn")
    @work
    async def on_load(self, event: Button.Pressed) -> None:
        num = event.button.id.split("-")[1]
        deck = self.query_one(f"#deck-{num}", Deck)
        if path := await self.push_screen_wait(FileOpen()):
            path = Path(path)
            deck.track_name = path.name
            self.on_track_loaded(num, path)


def main():
    DjApp().run()


if __name__ == "__main__":
    main()
