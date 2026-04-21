from pathlib import Path
from typing import Iterable
from textual.widgets import DirectoryTree


class FilteredDirectoryTree(DirectoryTree):
    """
    A DirectoryTree widget that can filter out certain directories and files.
    """

    NAMES_TO_EXCLUDE = {"bios", "image"}

    def __init__(self, path: str, allowed_systems: set[str] | None = None, **kwargs):
        """
        Initializes the FilteredDirectoryTree.

        Args:
            path (str): The path to the directory to display.
            allowed_systems (set[str] | None): Top-level folder names to show.
        """
        self.root_path = Path(path).expanduser().resolve()
        self.allowed_systems = set(allowed_systems) if allowed_systems is not None else None
        super().__init__(path, **kwargs)

    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        filtered_paths = []

        for path in paths:
            if path.name.startswith('.'):
                continue
            if path.name in self.NAMES_TO_EXCLUDE:
                continue
            if path.is_file():
                continue
            
            # Only filter top-level folders under the ROMs root.
            if self.allowed_systems is not None and path.is_dir():
                try:
                    resolved_parent = path.resolve().parent
                except OSError:
                    resolved_parent = path.parent

                if resolved_parent == self.root_path and path.name not in self.allowed_systems:
                    continue

            filtered_paths.append(path)

        return filtered_paths

