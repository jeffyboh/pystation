import pyglet
from pyglet.window import key
from pyglet.input import get_joysticks

# Key mappings for TUI navigation

KEY_UP = key.UP
KEY_DOWN = key.DOWN
KEY_LEFT = key.LEFT
KEY_RIGHT = key.RIGHT
KEY_ENTER = key.ENTER

class GamePadController:
    def __init__(self, keyboard_handler):
        self.keyboard_handler = keyboard_handler
        self.joystick = None
        self._setup_joystick()

    def _setup_joystick(self):
        controller = pyglet.input.Controller()
        controller.open()
        controller.push_handlers(self)
        joysticks = get_joysticks()
        if joysticks:
            self.joystick = joysticks[0]
            self.joystick.open()
            self.joystick.push_handlers(self)
            #self.joystick.rumble_play_weak(1.0, 0.1)
            print(f"Detected: {controller.name}\nController GUID: {controller.guid}")

        else:
            print("No joystick/gamepad detected.")

    def on_dpad_motion(self, joystick, vector):
        # 8BitDo M30 D-Pad events (hat_x, hat_y): up=(0,1), down=(0,-1), left=(-1,0), right=(1,0)
        if vector == (0, 1):
            self.keyboard_handler(KEY_UP)
        elif vector == (0, -1):
            self.keyboard_handler(KEY_DOWN)
        elif vector == (-1, 0):
            self.keyboard_handler(KEY_LEFT)
        elif vector == (1, 0):
            self.keyboard_handler(KEY_RIGHT)

        print(f"D-Pad motion: {vector}")

    def on_joyhat_motion(self, joystick, hat_x, hat_y):
        if hat_x == 0  and hat_y == 1:
            self.keyboard_handler(KEY_UP)
        elif hat_y == -1:
            self.keyboard_handler(KEY_DOWN)
        if hat_x == -1:
            self.keyboard_handler(KEY_LEFT)
        elif hat_x == 1:
            self.keyboard_handler(KEY_RIGHT)

        print(f"Hat motion: ({hat_x}, {hat_y})")

    def on_joybutton_press(self, joystick, button):
        # A button is usually button 0 on most controllers
        if button == 0:
            self.keyboard_handler(KEY_ENTER)
        print(f"Button {button} pressed")


    def on_connect(controller):
        controller.open()
        controller.rumble_play_weak(1.0, 0.1)
        print(f"Detected: {controller.name}\nController GUID: {controller.guid}")

    def on_disconnect(controller):
        print(f"Disconnected: {controller.name}")



def tui_keyboard_event(key_code):
    # Replace this with actual TUI event handling logic
    print(f"TUI Keyboard Event: {key.symbol_string(key_code)}")

if __name__ == "__main__":
    window = pyglet.window.Window(visible=False)  # No visible window needed
    controller = GamePadController(tui_keyboard_event)
    pyglet.app.run()

