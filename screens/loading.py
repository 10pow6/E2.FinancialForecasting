from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import LoadingIndicator, RichLog, Header, Footer

class Loading(Screen):
    def __init__(self, init_mode: str, init_msg: str) -> None:
        self.init_mode = init_mode
        self.init_msg = init_msg
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield LoadingIndicator()
        yield RichLog(highlight=True, markup=True)
        yield Footer()
    
    def on_mount(self) -> None:
        text_log = self.query_one(RichLog)
        text_log.write("[bold magenta]"+self.init_msg)