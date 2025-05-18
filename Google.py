import webbrowser
import pyautogui
import os
from gtts import gTTS
import winsound
import pytesseract
import time

def speak(text):
    try:
        tts = gTTS(text, lang='en')
        tts.save("response.mp3")
        os.system("ffmpeg -i response.mp3 response.wav -y")
        winsound.PlaySound("response.wav", winsound.SND_FILENAME)
        os.remove("response.mp3")
        os.remove("response.wav")
    except Exception as e:
        print(f"Error in speak function: {e}")

class GoogleController:
    @staticmethod
    def open_google():
        try:
            speak("Opening Google.")
            webbrowser.open("https://www.google.com")
        except Exception as e:
            speak("Failed to open Google.")
            print(f"Error opening Google: {e}")

    @staticmethod
    def search(query):
        try:
            speak(f"Searching Google for {query}.")
            search_url = f"https://www.google.com/search?q={query}"
            webbrowser.open(search_url)
        except Exception as e:
            speak("Failed to search on Google.")
            print(f"Error searching on Google: {e}")

    @staticmethod
    def open_new_tab():
        try:
            speak("Opening a new tab.")
            pyautogui.hotkey('ctrl', 't')
        except Exception as e:
            speak("Failed to open a new tab.")
            print(f"Error opening new tab: {e}")

    @staticmethod
    def close_tab():
        try:
            speak("Closing the tab.")
            pyautogui.hotkey('ctrl', 'w')
        except Exception as e:
            speak("Failed to close the tab.")
            print(f"Error closing tab: {e}")
            
    @staticmethod
    def close_google():
        try:
            speak("Closing Google.")
            pyautogui.hotkey('alt', 'f4')
        except Exception as e:
            speak("Failed to close Google.")
            print(f"Error closing Google: {e}")

    @staticmethod
    def scroll(direction):
        try:
            amount = 500 if direction == "up" else -500
            pyautogui.scroll(amount)
            speak(f"Scrolling {direction}.")
        except Exception as e:
            speak("Failed to scroll.")
            print(f"Error scrolling: {e}")

    @staticmethod
    def navigate_back():
        try:
            pyautogui.hotkey('ctrl','shift','tab')
            speak("Navigating back.")
        except Exception as e:
            speak("Failed to navigate back.")
            print(f"Error navigating back: {e}")

    @staticmethod
    def navigate_forward():
        try:
            pyautogui.hotkey('ctrl', 'tab')
            speak("Navigating forward.")
        except Exception as e:
            speak("Failed to navigate forward.")
            print(f"Error navigating forward: {e}")

    @staticmethod
    def google_history():
        try:
            pyautogui.hotkey('ctrl', 'h')
            speak("Opening Google history.")
        except Exception as e:
            speak("Failed to open history.")
            print(f"Error opening history: {e}")

    @staticmethod
    def type_in_google(text):
        try:
            speak(f"Typing {text} in Google search.")
            pyautogui.typewrite(text)
            pyautogui.press("enter")
        except Exception as e:
            speak("Failed to type in Google.")
            print(f"Error typing in Google: {e}")

    @staticmethod
    def capture_screenshot(file_name="screenshot.png"):
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(file_name)
            print(f"Screenshot saved as {file_name}.")
            return file_name
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            return None

    @staticmethod
    def extract_text_and_coordinates(image_path):
        try:
            image = image.open(image_path)
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            texts_and_coords = []

            for i in range(len(data['text'])):
                text = data['text'][i].strip()
                if text:
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    texts_and_coords.append((text, (x, y, x + w, y + h)))

            print("Extracted text and coordinates:", texts_and_coords)
            return texts_and_coords
        except Exception as e:
            print(f"Error extracting text and coordinates: {e}")
            return []

    @staticmethod
    def move_and_click_text(texts_and_coords, target_text):
        try:
            for text, (x1, y1, x2, y2) in texts_and_coords:
                if target_text.lower() in text.lower():
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    pyautogui.moveTo(center_x, center_y)
                    pyautogui.click()
                    print(f"Clicked on text: '{text}' at ({center_x}, {center_y}).")
                    return True
            print(f"Text '{target_text}' not found.")
            return False
        except Exception as e:
            print(f"Error moving and clicking text: {e}")
            return False

    @staticmethod
    def press_title(target_text):
        try:
            # Step 1: Capture a screenshot
            screenshot_path = GoogleController.capture_screenshot()

            if not screenshot_path:
                print("Failed to capture a screenshot.")
                return

            # Step 2: Extract text and coordinates
            texts_and_coords = GoogleController.extract_text_and_coordinates(screenshot_path)

            # Step 3: Move to and click on the target text
            if not GoogleController.move_and_click_text(texts_and_coords, target_text):
                print(f"Unable to find or click the text: {target_text}.")
        except Exception as e:
            print(f"Error in press_title: {e}")

if __name__ == "__main__":

    controller = GoogleController()
    controller.open_google()
    time.sleep(2)
    controller.search("Python programming")
    time.sleep(2)
    controller.scroll("down")
    time.sleep(2)
    controller.navigate_back()
    time.sleep(2)
    controller.navigate_forward()
    time.sleep(2)
    controller.google_history()
    time.sleep(2)
    controller.close_tab()  # Now works without TypeError
    time.sleep(2)
    controller.open_new_tab()
    time.sleep(2)
    controller.type_in_google("Machine learning")
    time.sleep(2)
    controller.press_title("Machine learning")
    time.sleep(2)
    controller.close_google()
