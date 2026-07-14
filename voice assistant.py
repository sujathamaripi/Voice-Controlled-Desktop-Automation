import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import webbrowser
import os
import pyautogui
import datetime
import psutil
import requests
from tkinter import *
from tkinter.scrolledtext import ScrolledText

# ------------------- GUI WINDOW -------------------

root = Tk()
root.title("Voice Controlled Desktop Automation")
root.geometry("700x500")

output_box = ScrolledText(root, wrap=WORD, font=("Arial", 12))
output_box.pack(padx=10, pady=10, fill=BOTH, expand=True)

def display(text):
    output_box.insert(END, text + "\n")
    output_box.see(END)

# ------------------- SPEECH ENGINE -------------------

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()
    display("Assistant: " + text)

# ------------------- VOICE INPUT -------------------

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        display("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        display("You: " + command)
        return command
    except:
        speak("Sorry, I didn't understand.")
        return ""

# ------------------- COMMAND FUNCTIONS -------------------

def run_assistant():
    speak("Voice Automation Started")
    while True:
        command = take_command()

        if "open chrome" in command:
            os.system("start chrome")

        elif "search" in command:
            command = command.replace("search", "")
            pywhatkit.search(command)

        elif "open youtube" in command:
            webbrowser.open("https://www.youtube.com")

        elif "play" in command:
            pywhatkit.playonyt(command.replace("play", ""))

        elif "open whatsapp" in command:
            webbrowser.open("https://web.whatsapp.com")

        elif "open vscode" in command:
            os.system("code")

        elif "open word" in command:
            os.system("start winword")

        elif "open excel" in command:
            os.system("start excel")

        elif "open powerpoint" in command:
            os.system("start powerpnt")

        elif "open camera" in command:
            os.system("start microsoft.windows.camera:")

        elif "open file explorer" in command:
            os.system("explorer")

        elif "open chatgpt" in command:
            webbrowser.open("https://chat.openai.com")

        elif "screenshot" in command:
            img = pyautogui.screenshot()
            img.save("screenshot.png")
            speak("Screenshot taken")

        elif "shutdown" in command:
            speak("Shutting down system")
            os.system("shutdown /s /t 5")

        elif "restart" in command:
            speak("Restarting system")
            os.system("shutdown /r /t 5")

        elif "sleep" in command:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        elif "lock" in command:
            os.system("rundll32.exe user32.dll,LockWorkStation")

        elif "time" in command:
            time = datetime.datetime.now().strftime("%H:%M")
            speak("Current time is " + time)

        elif "weather" in command:
            speak("Please say city name")
            city = take_command()
            api_key = "YOUR_API_KEY"
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
            response = requests.get(url).json()
            if response["cod"] == 200:
                temp = response["main"]["temp"] - 273
                speak(f"Temperature in {city} is {round(temp)} degree Celsius")

        elif "news" in command:
            webbrowser.open("https://news.google.com")

        elif "exit" in command or "stop" in command:
            speak("Stopping Assistant")
            break

# ------------------- BUTTON -------------------

start_button = Button(root, text="Start Voice Assistant", command=run_assistant,
                      font=("Arial", 14), bg="green", fg="white")
start_button.pack(pady=10)

root.mainloop()