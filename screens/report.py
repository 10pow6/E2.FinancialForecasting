from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static,Tabs

class Report(Screen):
    def __init__(self, init_msg:str, final_calc:dict, aggregates:dict, forecasting_config:dict) -> None:
        self.init_msg = init_msg
        self.final_calc = final_calc
        self.aggregates = aggregates
        self.forecasting_config = forecasting_config
        self.tabs = ["FULL"]
        for year_key, year_data in forecasting_config["DYNAMIC"].items():
            self.tabs.append(year_key)

        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(self.init_msg, id="static-report-header")
        yield Tabs(*self.tabs)
        yield Footer()