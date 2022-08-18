from pynput import keyboard

import captureParameters


class InputManager(keyboard.Listener):
    def __init__(self) -> None:
        self.pressed_keys = dict.fromkeys(captureParameters.KEYS_TO_LOG, 0)

        keyboardCaptureProcess = keyboard.Listener(on_press=self._onPressKeyboard, 
                                                    on_release=self._onReleaseKeyboard)
        keyboardCaptureProcess.start()

    def _onPressKeyboard(self, key):
        key = str(key).replace("'", "").upper()
        if str(key) in captureParameters.KEYS_TO_LOG:
            self.pressed_keys[str(key)] = 1
            
    def _onReleaseKeyboard(self, key):
        key = str(key).replace("'", "").upper()
        if str(key) in captureParameters.KEYS_TO_LOG:
            self.pressed_keys[str(key)] = 0
    
    def getPressedKeys(self):
        return self.pressed_keys