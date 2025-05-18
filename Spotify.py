import pytesseract
import speech_recognition as sr
import webbrowser
import os
import pyautogui
from pynput.keyboard import Controller, Key
import winsound
from gtts import gTTS
import time

def locate_and_click_button(image_path):

    try:
        # Try to locate the image on the screen
        location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
        if location:
            print(f"Found {image_path} at {location}")
            pyautogui.click(location)
            return True
        else:
            print(f"Button {image_path} not found on the screen.")
            return False
    except Exception as e:
        print(f"Error locating or clicking button {image_path}: {e}")
        return False
class SpotifyActions:
    @staticmethod
    def open_spotify():
        try:
            print("Opening Spotify.")
            os.system("start spotify")
        except Exception as e:
            print(f"Error opening Spotify: {e}")

    @staticmethod
    def close_spotify():
        try:
            print("Closing Spotify.")
            os.system("taskkill /im spotify.exe /f")
        except Exception as e:
            print(f"Error closing Spotify: {e}")

    @staticmethod
    def play_song():
        try:
            locate_and_click_button("play_button.png")
            print("Playing song.")
        except Exception as e:
            print("Could not play song")

    @staticmethod
    def pause_song():
        try:
            locate_and_click_button("pause_button.png")
            print("Pausing song.")
        except Exception as e:
            print("Could not pause song")

    @staticmethod
    def next_song():
        try:
            print("Skipping to next song.")
            pyautogui.press('nexttrack')
        except Exception as e:
            print(f"Error skipping to next song: {e}")

    @staticmethod
    def previous_song():
        try:
            print("Going back to previous song.")
            pyautogui.press('prevtrack')
            pyautogui.press('prevtrack')
        except Exception as e:
            print(f"Error going back to previous song: {e}")

    @staticmethod
    def search_song(song_name):
        try:
            print(f"Searching for song: {song_name}")
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

if __name__ == "__main__":

    SpotifyActions.open_spotify()
    time.sleep(5)
    SpotifyActions.search_song("Ezhel - Geceler")
    time.sleep(5)
    SpotifyActions.play_song()
    time.sleep(5)
    SpotifyActions.next_song()
    time.sleep(5)
    SpotifyActions.previous_song()
    time.sleep(5)
    SpotifyActions.pause_song()
    time.sleep(5)
    SpotifyActions.close_spotify()