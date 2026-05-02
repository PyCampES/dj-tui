from .audio import Action, Deck


class StateController:
    def __init__(self):
        self.deck_left_state = Action.PAUSE
        self.deck_right_state = Action.PAUSE

    def set_action(self, deck: Deck) -> Action:
        if deck == Deck.LEFT:
            self.deck_left_state = self._toggle_action(self.deck_left_state)
            return self.deck_left_state
        else:
            self.deck_right_state = self._toggle_action(self.deck_right_state)
            return self.deck_right_state

    @staticmethod
    def _toggle_action(action: Action):
        return Action.PLAY if action == Action.PAUSE else Action.PAUSE
