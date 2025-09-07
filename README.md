## PyStation
PyStation is an open-source front-end game launcher for the RetroArch emulator. Written in Python, it provides a clean and intuitive interface for browsing your game library, managing your ROMs, and launching your favorite retro titles with ease.

## **Planned Features**
- Seamless RetroArch Integration: Automatically detects your RetroArch installation and manages game launching.
- Dynamic Game Library: Scans your roms folder and organizes your collection with a user-friendly interface.
- Customizable Layouts: The user interface can be customized with various themes and layouts to suit your preferences.
- Easy to Extend: Designed with a modular architecture that makes it simple to add new features and emulators.

### **Getting Started**

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### **Prerequisites**

- **Python 3.8+:** PyStation requires a recent version of Python.
- **RetroArch:** Ensure RetroArch is installed on your system. PyStation will need to be configured with the correct path to your RetroArch executable.
- You will need to provide your own BIOS and ROM files.
- BIOS files should be placed in the RetroArch system folder. This would be ~/.congig/retroarch/system on a Linux system.
- Your ROMS can go anywhere, providing you specify the path in config.toml.

### **Installation**

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/pystation.git](https://github.com/jeffyboh/pystation.git)
   cd pystation
   ```
2. **Create a virtual environment:**
It is highly recommended to use a virtual environment to manage project dependencies. This keeps your system's Python packages clean and isolated.
```bash
python3 -m venv venv
```
3. **Activate the virtual environment:**
- On macOS and Linux:
```bash
source venv/bin/activate
```
- On Windows:
```bash
.\venv\Scripts\activate
```
4. **Install dependencies**
```bash
pip install -r requirements.txt
```

### **Contributing**

If you're interested in helping out, please read the `CONTRIBUTING.md` guide for more information on how to get started.
