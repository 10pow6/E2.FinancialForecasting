from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

from screens import Landing
from screens import Loading
from screens import Report

from screens.screenflow_event import ScreenFlowEvent

from handlers.api_handler import APIHandler
import os

from statics import DirectoryConfig

# QOL make dir if does not exist
# Get the current working directory


os.makedirs(DirectoryConfig.snapshots, exist_ok=True)
os.makedirs(DirectoryConfig.calculated, exist_ok=True)


api_handler = APIHandler()

class ForecastApp(App):
    """A Textual app to forecast E2 Financials."""
    CSS_PATH = "main.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"),("q","quit","Quit")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def on_mount(self) -> None:
        self.push_screen(Landing())
    
    def on_screen_flow_event( self, event: ScreenFlowEvent):
        print( "==============event id================")
        print( event.id )
        print( "======================================")
        parsed=event.id.split(".")
        event_payload = {
            "type":parsed[0],
            "direction":parsed[1],
            "action":parsed[2],
            "data":event.data
        }
        print(event_payload)
        print( "======================================")

        if( event_payload["type"]=="flow" and event_payload["direction"]=="push" ):
            if( event_payload["action"]=="execute_api"):
                api_handler.set_options(config_file=event_payload["data"]["selected_config"])
                self.push_screen( Loading( init_mode=event.id, init_msg=event.desc, api_handler=api_handler ) )
            if( event_payload["action"]=="load_snapshot"):
                api_handler.set_options(config_file=event_payload["data"]["selected_config"])
                self.push_screen( Loading( init_mode=event.id, init_msg=event.desc, api_handler=api_handler,snapshot_name=event_payload["data"]["snapshot"] ) )
            if( event_payload["action"]=="run_report"):
                self.push_screen( Report( init_msg=event.desc, final_calc=event_payload["data"]["final_calc"], aggregates=event_payload["data"]["aggregates"], forecasting_config=api_handler.options["FORECASTING_CONFIG"] ) )
                


if __name__ == "__main__":
    app = ForecastApp()
    app.run()