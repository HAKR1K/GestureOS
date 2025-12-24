import pyautogui
import platform
import time
import subprocess

OS = platform.system()

def copy():
    pyautogui.hotkey("command" if OS == "Darwin" else "ctrl", "c")


def paste():
    pyautogui.hotkey("command" if OS == "Darwin" else "ctrl", "v")


def smooth_scroll(amount, steps=10, delay=0.015):
    """
    amount: total scroll distance
    steps: number of small scrolls
    delay: pause between scrolls (seconds)
    """
    step_amount = int(amount / steps)
    for _ in range(steps):
        pyautogui.scroll(step_amount)
        time.sleep(delay)


def scroll_down():
    # Slow, smooth downward scroll
    smooth_scroll(-30, steps=20, delay=0.02)


def scroll_up():
    # Slow, smooth upward scroll
    smooth_scroll(30, steps=20, delay=0.02)


# 🔥 NEW: RELIABLE CLOSE WINDOW
def close_window():
    if OS == "Darwin":
        # macOS – use AppleScript (most reliable)
        script = '''
        tell application "System Events"
            keystroke "w" using command down
        end tell
        '''
        subprocess.run(["osascript", "-e", script])
    else:
        # Windows / Linux
        pyautogui.hotkey("alt", "f4")


ACTION_MAP = {
    "COPY": copy,
    "PASTE": paste,
    "SCROLL_DOWN": scroll_down,
    "SCROLL_UP": scroll_up,
    "CLOSE": close_window,   # 🔥 added
}
