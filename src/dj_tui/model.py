from .audio import Action, Deck


class StateController:
    def __init__(self):
        self.deck_left_state = Action.PAUSE
        self.deck_right_state = Action.PAUSE

    def get_action(self, deck: Deck) -> Action:
        if deck == Deck.LEFT:
            return self._toggle_action(self.deck_left_state)
        else:
            return self._toggle_action(self.deck_right_state)

    @staticmethod
    def _toggle_action(action: Action):
        return Action.PLAY if action == Action.PAUSE else Action.PAUSE
