
import os
import subprocess
from pathlib import Path
from typing import Optional
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, DirectoryTree, Label, Tree, OptionList
from textual.widgets.option_list import Option
from textual.reactive import var
from pystation.settings_loader import SettingsLoader
from pystation.widgets.filtered_directory_tree import FilteredDirectoryTree


class FileExplorer(App):

    def __init__(self, settings: SettingsLoader = None):
        super().__init__()

        self.paths = settings.get_all_paths()
        self.roms_path = self.paths.get('roms_path')
        self.cores_path = self.paths.get('cores_path')
        self.default_cores = settings.get_default_cores()

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
    selected_rom = var("")
    selected_system = var("")

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        valid_extensions = {".gba", ".chd", ".zip"}
        yield Header(show_clock=False)
        with Container(id="main-container"):
            with Container(id="left-pane"):
                yield FilteredDirectoryTree(
                    self.roms_path,
                    allowed_systems=set(self.default_cores.keys()),
                    id="file-tree",
                )
            with Container(id="right-pane"):
                yield OptionList(id="file-list")
        yield Footer()

    def on_mount(self) -> None:
        """Called when app is mounted."""
        self.query_one("#file-tree", DirectoryTree).focus()

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Called when the user selects a file in the directory tree."""
        if not str(event.path):
            return

        selected_rom = str(event.path)
        bios_path = self.paths.get('bios_path')
        command = self.get_retroarch_command(self.cores_path, selected_rom, bios_path)
        
        # make sure we have a valid command object
        if not command:
            return
               
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            print(f"Stderr: {e.stderr}")

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Called when the user selects an option in the option list."""
        selected_option = event.option
        selected_rom = selected_option.id
        bios_path = self.paths.get('bios_path')
        command = self.get_retroarch_command(self.cores_path, selected_rom, bios_path)
        
        # make sure we have a valid command object
        if not command:
            return
       
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            print(f"Stderr: {e.stderr}")
            
    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        """Called when a tree node is expanded."""
        if event.node.data and Path(event.node.data).is_dir():
            self.update_file_list(event.node.data)

    def on_directory_tree_directory_selected(self, event: DirectoryTree.DirectorySelected) -> None:
        """Called when a directory is selected in the tree."""
        self.update_file_list(event.path)

    def update_file_list(self, directory: str | Path) -> None:
        """Refresh the right-pane file list for the selected directory."""
        directory_path = Path(directory)

        if not directory_path.is_dir():
            file_list = self.query_one("#file-list", OptionList)
            file_list.clear_options()
            return

        files = sorted(directory_path.iterdir(), key=lambda x: x.name)
        file_options = []

        for entry in files:
            if entry.is_file() and not entry.name.startswith('.'):
                file_options.append(Option(prompt=entry.name, id=str(entry)))

        file_list = self.query_one("#file-list", OptionList)
        file_list.clear_options()
        file_list.add_options(file_options)

    def action_quit(self) -> None:
        """Action to quit the application."""
        self.exit()

    def get_retroarch_command(self, cores_path: str, rom_path: str, bios_path: str) -> list[str]:
        system_name = self.get_system_name(rom_path)
        # get the default_core for the system's rom we are going to launch
        default_core = self.default_cores.get(system_name)
        if not default_core:
            return
        # join the full qualified path to the core
        core_path = os.path.join(cores_path, default_core)
        
        program = "retroarch"
        # return an object which will be used to provide all of the arguments to retroarch``
        return [program, "-L", core_path, rom_path, "-s", bios_path]

    def get_system_name(self, rom_path: str) -> str:
        # parse the system_name out of the full path to the rom
        system_name = os.path.split(os.path.split(rom_path)[0])[1]
        return system_name

def main():
    settings = SettingsLoader()
    app = FileExplorer(settings)
    app.run()

