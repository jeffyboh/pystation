from pathlib import Path
from typing import Iterable
from textual.widgets import DirectoryTree
import os


class FilteredDirectoryTree(DirectoryTree):
    """
    A DirectoryTree widget that can filter out certain directories and files.
    """

    NAMES_TO_EXCLUDE = {"bios", "image"}

    def __init__(self, path: str, **kwargs):
        """
        Initializes the FilteredDirectoryTree.

        Args:
            path (str): The path to the directory to display.
            valid_extensions (set, optional): A set of file extensions to show.
                Supported ROM types in our case.
        """

        super().__init__(path, **kwargs)

    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [path for path in paths if not path.name in self.NAMES_TO_EXCLUDE]

