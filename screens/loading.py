from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import LoadingIndicator, RichLog, Header, Footer
from textual.worker import Worker
import json
from statics import DirectoryConfig
import datetime

class Loading(Screen):
    def __init__(self, init_mode: str, init_msg: str, api_handler) -> None:
        self.init_mode = init_mode
        self.init_msg = init_msg
        self.api_handler = api_handler
        self.tile_info = {}
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield LoadingIndicator()
        yield RichLog(highlight=True, markup=True)
        yield Footer()
    
    async def call_apis(self):
          # API Pulls
        workers=[self.run_worker(self.api_handler.tileprices_v2(), exclusive=False),
                 self.run_worker(self.api_handler.territory_prices(), exclusive=False)]
        await self.workers.wait_for_complete(workers)
        return True

    def on_mount(self) -> None:
        text_log = self.query_one(RichLog)
        text_log.write("[bold magenta]"+self.init_msg)

        self.run_worker(self.call_apis(), exclusive=False)
        
    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
            """Called when the worker state changes."""
            if( event.worker.name=="tileprices_v2" and event.worker.result != None):
                self.log(event)
                self.log(event.worker.result)
                
                self.tile_info["countries"] = event.worker.result

                text_log = self.query_one(RichLog)
                text_log.write("Pulled data from tile statistics (valid for T1 & T2).")
            elif( event.worker.name=="territory_prices" and event.worker.result != None):
                self.log(event)
                self.log(event.worker.result)
                
                self.tile_info["territories"] = event.worker.result

                text_log = self.query_one(RichLog)
                text_log.write("Pulled data from tile statistics (Territories).")
            elif( event.worker.name=="call_apis" and event.worker.result != None):
                # Write Snapshot after API calls
                path = DirectoryConfig.snapshots
                now = datetime.datetime.now()
                formatted_datetime = now.strftime("%Y%m%d%H%M%S")
                filename = f"snapshot-{formatted_datetime}.json"

                with open(path+"/"+filename, 'w') as file:
                    json.dump(self.tile_info, file, indent=4)

                text_log = self.query_one(RichLog)
                text_log.write("Successfully wrote snapshot file.")