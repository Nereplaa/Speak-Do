import pyautogui
import keyboard
import os

def test_selected_area(region):
    print("Please press Alt+Tab to switch to the YouTube homepage.")
    print("Press Shift+Alt when you're ready to take the screenshot.")

    # Wait for Shift+Alt key combination
    keyboard.wait('shift+alt')
    print("Taking screenshot...")

    # Take the screenshot
    screenshot_path = "test_region.png"
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")
    os.system(f"start {screenshot_path}")  # Works on Windows

# Example usage
test_selected_area(region=(0, 310, 2230, 1235))
