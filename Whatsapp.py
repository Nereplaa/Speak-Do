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


class WhatsAppActions:
    @staticmethod
    def open_whatsapp():
        try:
            print("Opening WhatsApp.")
            os.system("explorer.exe shell:appsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App")
        except Exception as e:
            print(f"Error opening WhatsApp: {e}")

    @staticmethod
    def close_whatsapp():
        try:
            print("Closing WhatsApp.")
            os.system("taskkill /im WhatsApp.exe /f")
        except Exception as e:
            print(f"Error closing WhatsApp: {e}")

    def search_contact(contact_name):
        try:
            print(f"Searching for contact: {contact_name}")
            search_box_coords = pyautogui.locateCenterOnScreen('search_box.png', confidence=0.8)
            if search_box_coords:
                pyautogui.click(search_box_coords)
                time.sleep(0.2)
                pyautogui.typewrite(contact_name)
                time.sleep(0.3)
                pyautogui.press('tab')
                pyautogui.press('enter')
                print("Contact found.")
            else:
                print("Search box not found. Please ensure WhatsApp is open and visible.")
        except Exception as e:
            print(f"Error searching for contact: {e}")

    @staticmethod
    def send_message(message):
        try:
            print(f"Sending message to contact.")
            message_box_coords = pyautogui.locateCenterOnScreen('message_box.png', confidence=0.8)
            if message_box_coords:
                pyautogui.click(message_box_coords)
                time.sleep(0.2)
                pyautogui.typewrite(message)
                time.sleep(0.3)
                pyautogui.press('enter')
                print("Message sent.")
            else:
                print("Message box not found. Please ensure WhatsApp is open and visible.")
        except Exception as e:
            print(f"Error sending message: {e}")

# Example of how to use the classes
if __name__ == "__main__":

    WhatsAppActions.open_whatsapp()
    time.sleep(2)
    WhatsAppActions.search_contact("Beden")
    time.sleep(0.5)
    WhatsAppActions.send_message("Hello, how are you?")
    time.sleep(0.5)
    WhatsAppActions.close_whatsapp()