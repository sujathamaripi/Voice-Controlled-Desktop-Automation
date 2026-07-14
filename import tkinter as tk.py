import tkinter as tk
from tkinter import scrolledtext, messagebox
import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import datetime
import pyautogui
import threading
import screen_brightness_control as sbc # pip install screen-brightness-control
import subprocess

# ---------------- SETTINGS ---------------- #
engine = pyttsx3.init()
engine.setProperty('rate', 170)

class AssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Voice AI")
        self.root.geometry("400x300")
        
        # Main Window UI
        self.label = tk.Label(root, text="Voice Automation System", font=("Arial", 14, "bold"))
        self.label.pack(pady=20)
        
        self.start_btn = tk.Button(root, text="Launch Assistant", bg="green", fg="white", 
                                   command=self.open_output_window, height=2, width=20)
        self.start_btn.pack(pady=10)

    def open_output_window(self):
        # Create a new Toplevel window for output
        self.output_win = tk.Toplevel(self.root)
        self.output_win.title("Assistant Live Output")
        self.output_win.geometry("600x400")
        
        self.log_box = scrolledtext.ScrolledText(self.output_win, width=70, height=20, bg="#1e1e1e", fg="white")
        self.log_box.pack(pady=10)
        
        # Start the voice logic in a background thread
        threading.Thread(target=self.run_assistant, daemon=True).start()

    def log(self, text):
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.see(tk.END)

    def speak(self, text):
        self.log(f"Assistant: {text}")
        engine.say(text)
        engine.runAndWait()

    def take_command(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.log("Listening...")
            recognizer.pause_threshold = 1
            audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            self.log(f"You: {command}")
            return command
        except:
            return ""

    def run_assistant(self):
        self.speak("Systems Online. How can I help?")
        while True:
            query = self.take_command()

            if "open youtube" in query:
                self.speak("What should I search for on YouTube?")
                search = self.take_command()
                webbrowser.open(f"https://www.youtube.com/results?search_query={search}")
                
            elif "google search" in query:
                self.speak("What do you want to search?")
                search = self.take_command()
                webbrowser.open(f"https://www.google.com/search?q={search}")

            elif "whatsapp" in query:
                webbrowser.open("https://web.whatsapp.com")
                self.speak("Opening WhatsApp. You can now dictate your message manually.")

            # SYSTEM CONTROLS
            elif "increase brightness" in query:
                current = sbc.get_brightness()[0]
                sbc.set_brightness(current + 20)
                self.speak("Brightness increased")

            elif "decrease brightness" in query:
                current = sbc.get_brightness()[0]
                sbc.set_brightness(max(0, current - 20))
                self.speak("Brightness decreased")

            elif "wifi on" in query:
                os.system('netsh interface set interface "Wi-Fi" enabled')
                self.speak("Turning on WiFi")

            elif "wifi off" in query:
                os.system('netsh interface set interface "Wi-Fi" disabled')
                self.speak("Turning off WiFi")

            elif "screenshot" in query:
                img = pyautogui.screenshot()
                img.save(f"screenshot_{datetime.datetime.now().second}.png")
                self.speak("Screenshot saved to project folder")

            elif "volume up" in query:
                for _ in range(5): pyautogui.press("volumeup")
                self.speak("Volume up")

            elif "mute" in query:
                pyautogui.press("volumemute")

            # APPS
            elif "open word" in query:
                os.system("start winword")
            elif "open excel" in query:
                os.system("start excel")
            elif "open camera" in query:
                subprocess.run('start microsoft.windows.camera:', shell=True)

            elif "stop" in query or "exit" in query:
                self.speak("Goodbye!")
                self.output_win.destroy()
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = AssistantGUI(root)
    root.mainloop()