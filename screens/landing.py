from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, RadioButton, RadioSet, ListView, ListItem, Label, Button
from textual.containers import Container, Vertical
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Placeholder

import os

CONFIG_DIR="configs"
SNAPSHOTS_DIR="snapshots"

class Profile(Widget):
    configs: reactive[list[str]] = reactive(list, recompose=True) 

    def compose(self) -> ComposeResult:
        with RadioSet():
            for idx,label in enumerate(self.configs):
                yield RadioButton(label,value=(idx==0))
    
    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        print(event.pressed.label)
        print(event.radio_set.pressed_index)


class Snapshot(ListItem):
    file_name = ""

    def __init__( self, value: str  ) -> None:
        """Initialise the input."""
        
        self.file_name = value
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label(self.file_name)


class Forecast(Widget):
    snapshots = ListView()
    def compose(self) -> ComposeResult:
        yield self.snapshots

    def on_mount(self) -> None:
        # Get config profiles
        path = SNAPSHOTS_DIR
        dir_list = os.listdir(path)
        self.snapshots.append( Snapshot("Create new..."))   
        for file in dir_list:
            self.snapshots.append( Snapshot(file) )   


class Landing(Screen):
    
    configs: reactive[list[str]] = reactive(list, recompose=True)


    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()

        with Vertical():
            with Container():
                yield Static(" Profile ", id="profile-title")
                yield Profile(id="profile").data_bind(Landing.configs)
            with Container():
                yield Static(" Forecast ", id="history-title")
                yield Forecast(id="history")

        with Container(id="start-forecast"):
            yield Static(" Actions ", id="actions-title")
            yield Button("Generate Forecast", variant="default" )
            yield Button("Load Forecast", variant="default", disabled=True )
            yield Button("Quit", variant="default" )

        yield Footer()
        
        
    def on_mount(self) -> None:
        # Get config profiles
        path = CONFIG_DIR
        dir_list = os.listdir(path)
        for file in dir_list:
            self.configs.append(file)    
        
        self.mutate_reactive(Profile.configs)
