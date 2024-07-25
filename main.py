from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from screens.landing import Landing

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
        self.install_screen(Landing(), name="landing")
        self.push_screen('landing')

if __name__ == "__main__":
    app = ForecastApp()
    app.run()