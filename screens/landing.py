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

    def on_mount(self) -> None:
        # Get config profiles
        path = CONFIG_DIR
        dir_list = os.listdir(path)
        for file in dir_list:
            self.configs.append(file)    
        
        self.mutate_reactive(Profile.configs)

class Forecast(Widget):
    snapshots: reactive[list[ListItem]] = reactive(list, recompose=True) 
    def compose(self) -> ComposeResult:
        yield ListView( *self.snapshots )

    def on_mount(self) -> None:
        # Get config profiles
        path = SNAPSHOTS_DIR
        dir_list = os.listdir(path)
        self.snapshots.append( ListItem(Label("Create new")) )
        for file in dir_list:
            self.snapshots.append( ListItem(Label(file))  )
        self.mutate_reactive(Forecast.snapshots)


class Landing(Screen):
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()

        with Vertical():
            with Container():
                yield Static(" Profile ", id="profile-title")
                yield Profile(id="profile")
            with Container():
                yield Static(" Forecast ", id="history-title")
                yield Forecast(id="history")

        with Container(id="start-forecast"):
            yield Static(" Actions ", id="actions-title")
            yield Button("Generate Forecast", variant="default" )
            yield Button("Load Forecast", variant="default", disabled=True )
            yield Button("Quit", variant="default" )

        yield Footer()
        
        
