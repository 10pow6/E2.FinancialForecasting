from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import LoadingIndicator, RichLog, Header, Footer
from textual.worker import Worker

class Loading(Screen):
    def __init__(self, init_mode: str, init_msg: str, api_handler) -> None:
        self.init_mode = init_mode
        self.init_msg = init_msg
        self.api_handler = api_handler
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield LoadingIndicator()
        yield RichLog(highlight=True, markup=True)
        yield Footer()
    
    def on_mount(self) -> None:
        text_log = self.query_one(RichLog)
        text_log.write("[bold magenta]"+self.init_msg)
        self.run_worker(self.api_handler.tileprices_v2(), exclusive=True)

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
            """Called when the worker state changes."""
            if( event.worker.name=="tileprices_v2" and event.worker.result != None):
                self.log(event)
                self.log(event.worker.result)
                text_log = self.query_one(RichLog)
                text_log.write("Pulled data from tile statistics (valid for T1 & T2).")