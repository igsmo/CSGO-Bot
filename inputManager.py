from pynput import keyboard # , mouse

import parameters


class InputManager(keyboard.Listener):
    def __init__(self) -> None:
        self.pressed_keys = dict.fromkeys(parameters.KEYS_TO_LOG, 0)

        keyboardCaptureProcess = keyboard.Listener(on_press=self._onPressKeyboard, 
                                                    on_release=self._onReleaseKeyboard)
        keyboardCaptureProcess.start()

        # mouseCaptureProcess = mouse.Listener(
        #     on_click=self._onClickMouse)
        # mouseCaptureProcess.start()

    def _onPressKeyboard(self, key):
        key = str(key).replace("'", "").upper()
        if str(key) in parameters.KEYS_TO_LOG:
            self.pressed_keys[str(key)] = 1
            
    def _onReleaseKeyboard(self, key):
        key = str(key).replace("'", "").upper()
        if str(key) in parameters.KEYS_TO_LOG:
            self.pressed_keys[str(key)] = 0
    
    def _onClickMouse(self, x, y, button, pressed):
        print('{0} at {1}'.format(
            'Pressed' if pressed else 'Released',
            (x, y)))
        if not pressed:
            # Stop listener
            return False
    
    def getPressedKeys(self):
        return self.pressed_keys