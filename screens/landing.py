from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, RadioButton, RadioSet, ListView, ListItem, Label, Button
from textual.containers import Container, Vertical
from textual.widget import Widget
from textual.reactive import reactive

from screens.screenflow_event import ScreenFlowEvent
from statics import DirectoryConfig

import os

class Profile(Widget):
    configs: reactive[list[str]] = reactive(list, recompose=True) 
    selected_config:str

    def compose(self) -> ComposeResult:
        with RadioSet():
            for idx,label in enumerate(self.configs):
                yield RadioButton(label=label,value=(idx==0),name=label)
    
    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        print(event.pressed.name)
        print(event.radio_set.pressed_index)
        self.selected_config=event.pressed.name

    def on_mount(self) -> None:
        # Get config profiles
        path = DirectoryConfig.configs
        dir_list = os.listdir(path)
        if( len(dir_list) > 0 ): # set default
            self.selected_config=dir_list[0]

        for file in dir_list:
            self.configs.append(file)    
        
        self.mutate_reactive(Profile.configs)

class Snapshot(Widget):
    snapshots: reactive[list[ListItem]] = reactive(list, recompose=True) 
    def compose(self) -> ComposeResult:
        yield ListView( *self.snapshots )

    def on_mount(self) -> None:
        # Get config profiles
        path = DirectoryConfig.snapshots
        dir_list = os.listdir(path)
        for file in dir_list:
            self.snapshots.append( ListItem(Label(file))  )
        if( len(self.snapshots) == 0 ):
            load_button=self.app.query_one("Landing #button-load-snapshot")
            load_button.disabled=True
        self.mutate_reactive(Snapshot.snapshots)


class Landing(Screen):
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()

        with Vertical():
            with Container():
                yield Static(" Profiles ", id="profile-title")
                yield Profile(id="profile")
            with Container():
                yield Static(" Snapshots ", id="history-title")
                yield Snapshot(id="history")

        with Container(id="start-forecast"):
            yield Static(" Actions ", id="actions-title")
            yield Button("Generate New Snapshot", variant="default", id="button-generate-new" )
            yield Button("Load Snapshot", variant="default", disabled=False, id="button-load-snapshot" )
            yield Button("Quit", variant="default", id="button-quit" )

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id

        if button_id == "button-quit":
            self.app.exit()
        if button_id == "button-generate-new":
            
            profile=self.app.query_one("Landing #profile")
            selected_config=profile.selected_config
            self.app.post_message(ScreenFlowEvent( id="flow.push.execute_api",desc="Beginning data pull of tile statistics...", data={"selected_config":selected_config} ))

        
