from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, RadioButton, RadioSet, ListView, ListItem, Label, Button
from textual.containers import Container, Vertical
from textual.reactive import reactive
from textual.widget import Widget

from screens import Loading
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

class Snapshot(Widget):
    snapshots: reactive[list[ListItem]] = reactive(list, recompose=True) 
    def compose(self) -> ComposeResult:
        yield ListView( *self.snapshots )

    def on_mount(self) -> None:
        # Get config profiles
        path = SNAPSHOTS_DIR
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
            self.app.push_screen(Loading())

        
