from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import LoadingIndicator

class Loading(Screen):
    def compose(self) -> ComposeResult:
        yield LoadingIndicator()