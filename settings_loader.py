import toml
from pathlib import Path

class SettingsLoader:
    """
    A class to load application settings from a TOML file.
    """
    def __init__(self, config_file: str = "config.toml"):
        """
        Initializes the settings loader and attempts to load the configuration.
        """
        self.config_file = Path(config_file)
        self.settings = {}
        self.load_settings()

    def load_settings(self):
        """
        Loads the settings from the specified TOML file.
        """
        if not self.config_file.exists():
            print(f"Error: Configuration file '{self.config_file}' not found.")
            return

        try:
            self.settings = toml.loads(self.config_file.read_text())
            print(f"Successfully loaded settings from '{self.config_file}'.")
        except toml.TomlDecodeError as e:
            print(f"Error: Failed to parse TOML file. Details: {e}")

    def get_path(self, section: str, key: str) -> str:
        """
        Retrieves a path from the settings dictionary.
        Returns an empty string if the key or section is not found.
        """
        if section in self.settings and key in self.settings[section]:
            return self.settings[section][key]
        return ""

    def get_all_paths(self) -> dict:
        """
        Retrieves all paths from the 'paths' section of the settings.
        Returns an empty dictionary if the section is not found.
        """
        return self.settings.get("paths", {})

if __name__ == "__main__":
    # Example usage of the SettingsLoader class.
    
    # Note: You need to have a 'config.toml' file in the same directory.
    # The toml library can be installed with 'pip install toml'.
    
    settings_manager = SettingsLoader()

    # Retrieve the paths from the loaded settings.
    bios_folder = settings_manager.get_path("paths", "bios_folder")
    roms_folder = settings_manager.get_path("paths", "roms_folder")
    images_folder = settings_manager.get_path("paths", "images_folder")

    # Print the paths to verify they were loaded correctly.
    print(f"\nBIOS Path: {bios_folder}")
    print(f"ROMs Path: {roms_folder}")
    print(f"Images Path: {images_folder}")

