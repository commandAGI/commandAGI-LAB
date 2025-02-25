import base64
import subprocess

try:
    from e2b_desktop import Sandbox
except ImportError:
    raise ImportError(
        "e2b_desktop is not installed. Please install commandLAB with the e2b_desktop extra:\n\npip install commandLAB[e2b_desktop]"
    )

from commandLAB.computers.base_computer import BaseComputer
from commandLAB.types import (
    CommandAction,
    KeyboardKey,
    KeyboardKeyDownAction,
    KeyboardKeyReleaseAction,
    KeyboardStateObservation,
    MouseButton,
    MouseButtonDownAction,
    MouseButtonUpAction,
    MouseMoveAction,
    MouseScrollAction,
    MouseStateObservation,
    ScreenshotObservation,
    TypeAction,
)


class E2BDesktopComputer(BaseComputer):
    """Environment that uses E2B Desktop Sandbox for secure computer interactions"""

    def __init__(self, video_stream=False):
        super().__init__()
        self.desktop = Sandbox(video_stream=video_stream)

    def reset(self):
        """Reset the desktop environment and return initial observation"""
        self.desktop.hotkey("win", "d")  # Show desktop
        return self.get_observation()

    def step(self, action):
        """Execute action and return (observation, reward, done, info)"""
        success = self.execute_action(action)
        observation = self.get_observation()

        reward = 1.0 if success else -1.0
        done = False
        info = {"action_success": success}

        return observation, reward, done, info

    def close(self):
        """Clean up resources"""
        self.desktop = None  # E2B sandbox automatically closes when object is destroyed

    def get_screenshot(self) -> ScreenshotObservation:
        """Return a screenshot of the current state as base64 encoded string."""
        screenshot = self.desktop.take_screenshot()
        b64_screenshot = base64.b64encode(screenshot).decode("utf-8")
        return ScreenshotObservation(screenshot=b64_screenshot)

    def get_mouse_state(self) -> MouseStateObservation:
        """Return dummy mouse state as Sandbox does not provide real-time states."""
        raise NotImplementedError(
            "E2BDesktopEnv does not support mouse state observation"
        )

    def get_keyboard_state(self) -> KeyboardStateObservation:
        """Return dummy keyboard state as Sandbox does not track key states."""
        raise NotImplementedError(
            "E2BDesktopEnv does not support keyboard state observation"
        )

    def execute_command(self, action: CommandAction) -> bool:
        """Execute a system command in the host environment using subprocess."""
        try:
            result = subprocess.run(
                action.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=action.timeout if action.timeout is not None else 10,
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Error executing command: {e}")
            return False

    def execute_keyboard_key_down(self, action: KeyboardKeyDownAction) -> bool:
        """Execute key down for a keyboard key using action signature."""
        e2b_key = KeyboardKey.to_e2b(action.key)
        return self.desktop.pyautogui(f"pyautogui.keyDown('{e2b_key}')")

    def execute_keyboard_key_release(self, action: KeyboardKeyReleaseAction) -> bool:
        """Execute key release for a keyboard key using action signature."""
        e2b_key = KeyboardKey.to_e2b(action.key)
        return self.desktop.pyautogui(f"pyautogui.keyUp('{e2b_key}')")

    def execute_type(self, action: TypeAction) -> bool:
        return self.desktop.write(action.text)

    def execute_mouse_move(self, action: MouseMoveAction) -> bool:
        return self.desktop.mouse_move(action.x, action.y)

    def execute_mouse_scroll(self, action: MouseScrollAction) -> bool:
        return self.desktop.pyautogui(f"pyautogui.scroll({action.amount})")

    def execute_mouse_button_down(self, action: MouseButtonDownAction) -> bool:
        e2b_button = MouseButton.to_e2b(action.button)
        return self.desktop.pyautogui(f"pyautogui.mouseDown(button='{e2b_button}')")

    def execute_mouse_button_up(self, action: MouseButtonUpAction) -> bool:
        e2b_button = MouseButton.to_e2b(action.button)
        return self.desktop.pyautogui(f"pyautogui.mouseUp(button='{e2b_button}')")
