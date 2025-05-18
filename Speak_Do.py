import pytesseract
import speech_recognition as sr
import webbrowser
import os
import pyautogui
from pynput.keyboard import Controller, Key
import winsound
from gtts import gTTS
import time
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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

def recognize_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a command...")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except Exception as e:
            print(f"Error recognizing voice: {e}")
            speak("I could not understand. Please try again.")
            return None

class GoogleController:
    @staticmethod
    def open_google():
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    @staticmethod
    def search(query):
        speak(f"Google opening {query}.")
        webbrowser.open(f"https://www.{query}.com")

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
        """
        Captures a screenshot of the entire screen.
        """
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(file_name)
            print(f"Screenshot saved as {file_name}.")
            return file_name
        except Exception as e:
            print(f"Screenshot capture error: {e}")
            return None

class PressCommands:
    @staticmethod
    def press_by_text(target_text):
        """
        Simulates clicking on visible text on the screen.
        """
        try:
            speak(f"Searching for the text: '{target_text}'...")

            # Capture a screenshot of the entire screen
            screenshot_path = "press_command_screenshot.png"
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")

            # Perform OCR on the captured screenshot
            texts_and_coords = PressCommands.extract_text_and_coordinates(screenshot_path)
            if not texts_and_coords:
                speak("No text found in OCR results.")
                return

            # Find and click the target text
            if not PressCommands.find_and_click_text(target_text, texts_and_coords):
                speak(f"Could not find '{target_text}' on the screen.")
            else:
                speak(f"Successfully clicked on '{target_text}'.")
        except Exception as e:
            print(f"press_by_text error: {e}")
            speak("An error occurred while attempting to press the text.")

    @staticmethod
    def extract_text_and_coordinates(image_path):
        """
        Extracts text and coordinates from an image using Tesseract OCR.
        """
        try:
            # Direct OCR configuration
            custom_config = r'--oem 3 --psm 6'  # Standard OCR settings
            data = pytesseract.image_to_data(
                image_path,
                lang='eng',  # Default to English
                config=custom_config,
                output_type=pytesseract.Output.DICT
            )

            # Extract text and bounding box coordinates
            texts_and_coords = []
            for i in range(len(data['text'])):
                text = data['text'][i].strip()
                if text:
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    texts_and_coords.append((text, (x, y, x + w, y + h)))

            return texts_and_coords
        except Exception as e:
            print(f"OCR processing error: {e}")
            return []

    @staticmethod
    def find_and_click_text(target_text, texts_and_coords, region=None):
        """
        Finds the specified text in the extracted data and clicks it.
        Adjusts coordinates for region offsets if a region is used.
        """
        for text, (x1, y1, x2, y2) in texts_and_coords:
            if target_text.lower() in text.lower():
                # Adjust coordinates if a region is used
                if region:
                    x_offset, y_offset = region[0], region[1]
                    x1 += x_offset
                    y1 += y_offset
                    x2 += x_offset
                    y2 += y_offset
                
                # Calculate the center of the text box
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                # Move to the adjusted coordinates and click
                pyautogui.moveTo(center_x, center_y)
                pyautogui.click()
                print(f"Clicked on text: '{text}' at ({center_x}, {center_y}).")
                return True

        print(f"Text '{target_text}' not found.")
        return False
    
class GoogleSearchActions:
    @staticmethod
    def google_press_by_text(target_text, region=(0, 310, 2230, 1235)):
        """
        Simulates clicking on visible text within Google search results.
        Adjusts for the region offset to ensure accurate clicking.
        """
        try:
            speak(f"Searching for the text: '{target_text}' in Google results...")

            # Capture a screenshot of the specified region
            screenshot_path = "google_search_area.png"
            screenshot = pyautogui.screenshot(region=region)
            screenshot.save(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")

            # Perform OCR on the captured screenshot
            texts_and_coords = PressCommands.extract_text_and_coordinates(screenshot_path)
            if not texts_and_coords:
                speak("No text found in OCR results.")
                return

            # Search for the target text and click it
            if not PressCommands.find_and_click_text(target_text, texts_and_coords, region=region):
                speak(f"Could not find '{target_text}' in Google search results.")
            else:
                speak(f"Successfully clicked on '{target_text}'.")
        except Exception as e:
            print(f"google_press_by_text error: {e}")
            speak("An error occurred while attempting to press the text.")

class YouTubeActions:
    @staticmethod
    def open_video_by_name(video_name, region=(300, 300, 2230, 1220)):
        """
        Simulates opening a video by its name on YouTube.
        """
        try:
            speak(f"Searching for video: {video_name}...")

            # Capture a screenshot of the region
            screenshot_path = "youtube_video_area.png"
            screenshot = pyautogui.screenshot(region=region)
            screenshot.save(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")

            # Perform OCR
            texts_and_coords = PressCommands.extract_text_and_coordinates(screenshot_path)
            if not texts_and_coords:
                speak("No text found in OCR results.")
                return

            # Search for the video name and click it
            if not PressCommands.find_and_click_text(video_name, texts_and_coords, region=region):
                speak(f"Could not find video '{video_name}' in the selected area.")
            else:
                speak(f"Successfully opened video: {video_name}.")
        except Exception as e:
            print(f"Error in open_video_by_name: {e}")
            speak("An error occurred while searching for the video.")

class SpotifyActions:
    @staticmethod
    def open_spotify():
        try:
            speak("Opening Spotify.")
            os.system("start spotify")
        except Exception as e:
            print(f"Error opening Spotify: {e}")

    @staticmethod
    def close_spotify():
        try:
            speak("Closing Spotify.")
            os.system("taskkill /im spotify.exe /f")
        except Exception as e:
            print(f"Error closing Spotify: {e}")

    @staticmethod
    def play_song():
        try:
            speak("Playing song.")
            pyautogui.press('playpause')
        except Exception as e:
            print("Could not play song")

    @staticmethod
    def pause_song():
        try:
            speak("Pausing song.")
            pyautogui.press('playpause')
        except Exception as e:
            print("Could not pause song")

    @staticmethod
    def next_song():
        try:
            speak("Skipping to the next song.")
            pyautogui.press('nexttrack')
        except Exception as e:
            print(f"Error skipping to next song: {e}")

    @staticmethod
    def previous_song():
        try:
            speak("Going back to the previous song.")
            pyautogui.press('prevtrack')
            pyautogui.press('prevtrack')
        except Exception as e:
            print(f"Error going back to previous song: {e}")

    @staticmethod
    def search_song(song_name):
        try:
            speak(f"Searching for song: {song_name}")
            pyautogui.hotkey('ctrl', 'l')  # Focus search bar
            time.sleep(1)
            pyautogui.typewrite(song_name)
            pyautogui.press('enter')
            time.sleep(2)
            for _ in range(4):
                pyautogui.press("tab")
            pyautogui.press('enter')
        except Exception as e:
            print(f"Error searching for song: {e}")

class WhatsAppActions:
    @staticmethod
    def open_whatsapp():
        try:
            speak("Opening WhatsApp.")
            os.system("explorer.exe shell:appsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App")
        except Exception as e:
            print(f"Error opening WhatsApp: {e}")

    @staticmethod
    def close_whatsapp():
        try:
            speak("Closing WhatsApp.")
            os.system("taskkill /im WhatsApp.exe /f")
        except Exception as e:
            print(f"Error closing WhatsApp: {e}")

    @staticmethod
    def search_contact(contact_name):
        try:
                speak(f"Searching for contact: {contact_name}")
                pyautogui.hotkey('ctrl', 'f')
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.typewrite(contact_name)
                time.sleep(0.3)
                pyautogui.press('tab')
                pyautogui.press('enter')
                print("Contact found.")
        except Exception as e:
            print(f"Error searching for contact: {e}")

    @staticmethod
    def send_message(message):
        try:
            speak(f"Sending message: {message}")
            message_box_coords = pyautogui.locateCenterOnScreen('message_box.png', confidence=0.8)
            if message_box_coords:
                pyautogui.click(message_box_coords)
                time.sleep(0.2)
                pyautogui.typewrite(message)
                time.sleep(0.3)
                pyautogui.press('enter')
                print("Message sent.")
            else:
                speak("Message box not found. Please ensure WhatsApp is open and visible.")
        except Exception as e:
            print(f"Error sending message: {e}")

def main():
    speak("Voice command system activated.")
    while True:
        command = recognize_voice()
        if not command:
            continue

        if "open google" in command:
            GoogleController.open_google()
        elif "google open" in command:
            query = command.replace("google open", "").strip()
            GoogleController.search(query)
        elif "open spotify" in command:
            SpotifyActions.open_spotify()
        elif "play song" in command:
            SpotifyActions.play_song()
        elif "pause song" in command:
            SpotifyActions.pause_song()
        elif "next song" in command:
            SpotifyActions.next_song()
        elif "previous song" in command:
            SpotifyActions.previous_song()
        elif "search song" in command:
            song_name = command.replace("search song", "").strip()
            SpotifyActions.search_song(song_name)
        elif "close spotify" in command:
            SpotifyActions.close_spotify()
        elif "open new tab" in command:
            GoogleController.open_new_tab()
        elif "close tab" in command:
            GoogleController.close_tab()
        elif "scroll up" in command:
            GoogleController.scroll("up")
        elif "scroll down" in command:
            GoogleController.scroll("down")
        elif "navigate back" in command:
            GoogleController.navigate_back()
        elif "navigate forward" in command:
            GoogleController.navigate_forward()
        elif "open history" in command:
            GoogleController.google_history()
        elif "type in google" in command:
            speak("What would you like to type?")
            text = recognize_voice()
            if text:
                GoogleController.type_in_google(text)
        elif "close google" in command:
            GoogleController.close_google()
        elif "open whatsapp" in command:
            WhatsAppActions.open_whatsapp()
        elif "search contact" in command:
            speak("Who would you like to search for?")
            contact_name = recognize_voice()
            if contact_name:
                WhatsAppActions.search_contact(contact_name)
        elif "send message" in command:
            speak("What is the message?")
            message = recognize_voice()
            if message:
                WhatsAppActions.send_message(message)
        elif "close whatsapp" in command:
            WhatsAppActions.close_whatsapp()
        elif "press" in command and "google" in command:
            speak("What do you want to press in Google?")
            target_text = recognize_voice()
            if target_text:
                GoogleSearchActions.google_press_by_text(target_text)
            else:
                speak("No valid text detected.")
                speak("Could not recognize the text to press.")
        elif "press" in command:
            speak("What do you want to press?")
            target_text = recognize_voice()
            if target_text:
                PressCommands.press_by_text(target_text)
            else:
                speak("No valid text detected.")
        elif "open video" in command:
            speak("Which video would you like to open?")
            video_name = recognize_voice()
            if video_name:
                YouTubeActions.open_video_by_name(video_name)
            else:
                speak("Could not recognize the video name.")
        elif "cut the system" in command:
            speak("Pausing the system for 2 minutes. I will resume after that.")
            time.sleep(120)
            speak("System is now active.")
        elif "exit" in command or "quit" in command:
            speak("Shutting down the voice command system.")
            break
        elif "shut down" in command:
            speak("Shutting down the computer.")
            os.system("shutdown /s /t 1")

if __name__ == "__main__":
    main()

