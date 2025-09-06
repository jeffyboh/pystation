
import os
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, DirectoryTree, Label, Tree
from textual.reactive import var
from settings_loader import SettingsLoader



class FileExplorer(App):

    def __init__(self, root_folder: str = None):
        super().__init__()
        self.roms_folder = root_folder if root_folder else os.getcwd()

    # Set the application's CSS.
    # The grid layout is used to create the two panes.
    TITLE = "PyStation"
    CSS = """
    #main-container {
        layout: grid;
        grid-size: 2;
        grid-columns: 3fr 7fr;
        height: 100%;
    }

    #left-pane {
        border: heavy $accent;
        padding: 1;
        width: 1fr;
        height: 1fr;
    }

    #right-pane {
        border: heavy $secondary;
        padding: 1;
        width: 1fr;
        height: 1fr;
    }

    #info-label {
        margin: 1 2;
        text-style: bold;
    }
    """
    
    # Define the application's key bindings.
    BINDINGS = [
        ("q", "quit", "Quit PyStation"),
        ("escape", "quit", "Quit PyStation"),
    ]

    # This reactive variable will hold the path of the selected file.
    selected_path = var("No ROM file selected.")

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=False)
        with Container(id="main-container"):
            with Container(id="left-pane"):
                yield DirectoryTree(self.roms_folder, id="file-tree")
            with Container(id="right-pane"):
                yield Label("Right Pane: File Info")
                yield Label("Use arrow keys to navigate the tree and press Enter to select an item.")
                yield Label("", id="info-label")
        yield Footer()

    def on_mount(self) -> None:
        """Called when app is mounted."""
        # Find the label that will display the selected file path
        self.query_one("#info-label", Label).update(f"Current directory: {self.roms_folder}")
        self.query_one("#file-tree", DirectoryTree).focus()

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Called when the user selects a file in the directory tree."""
        # Update the label with the selected file's path.
        self.selected_path = str(event.path)
        self.query_one("#info-label", Label).update(f"Selected file: {self.selected_path}")

    def on_directory_tree_directory_selected(self, event: DirectoryTree.DirectorySelected) -> None:
        """Called when the user selects a directory in the directory tree."""
        # Update the label with the selected directory's path.
        self.selected_path = str(event.path)
        self.query_one("#info-label", Label).update(f"Selected directory: {self.selected_path}")

    def action_quit(self) -> None:
        """Action to quit the application."""
        self.exit()

if __name__ == "__main__":
    settings = SettingsLoader()
    paths = settings.get_all_paths()

    roms_folder = paths.get('roms_folder')

    app = FileExplorer(roms_folder)
    app.run()
