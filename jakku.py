import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import pyautogui
import datetime
import pywhatkit
import tkinter as tk
import threading
import requests
import screen_brightness_control as sbc
import math
import time

engine = pyttsx3.init()
typing_mode = False

# ---------------- SPEAK FUNCTION ----------------
def speak(text):
    output_box.insert(tk.END, "Assistant: " + text + "\n")
    engine.say(text)
    engine.runAndWait()

# ---------------- LISTEN FUNCTION ----------------
def listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        output_box.insert(tk.END, "Listening...\n")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        output_box.insert(tk.END, "You: " + command + "\n")
        return command.lower()

    except:
        speak("Sorry I didn't understand")
        return ""

# ---------------- COMMAND EXECUTION ----------------
def execute_command(command):
    global typing_mode

    if "start typing" in command:
        typing_mode = True
        speak("Voice typing activated")

    elif "stop typing" in command:
        typing_mode = False
        speak("Voice typing stopped")

    elif typing_mode:
        pyautogui.write(command + " ")

    elif "open chrome" in command:
        speak("Opening Chrome")
        os.system("start chrome")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("calc")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open whatsapp" in command:
        speak("Opening WhatsApp")
        webbrowser.open("https://web.whatsapp.com")

    elif "open vs code" in command:
        speak("Opening VS Code")
        os.system("code")

    elif "open word" in command:
        speak("Opening Word")
        os.system("start winword")

    elif "open excel" in command:
        speak("Opening Excel")
        os.system("start excel")

    elif "open powerpoint" in command:
        speak("Opening PowerPoint")
        os.system("start powerpnt")

    elif "open file explorer" in command:
        speak("Opening File Explorer")
        os.system("explorer")

    elif "close chrome" in command:
        speak("Closing Chrome")
        os.system("taskkill /f /im chrome.exe")

    elif "close calculator" in command:
        speak("Closing Calculator")
        os.system("taskkill /f /im Calculator.exe")

    elif "close vs code" in command:
        speak("Closing VS Code")
        os.system("taskkill /f /im Code.exe")

    elif "close word" in command:
        speak("Closing Word")
        os.system("taskkill /f /im WINWORD.EXE")

    elif "close excel" in command:
        speak("Closing Excel")
        os.system("taskkill /f /im EXCEL.EXE")

    elif "close powerpoint" in command:
        speak("Closing PowerPoint")
        os.system("taskkill /f /im POWERPNT.EXE")

    elif "play" in command:
        song = command.replace("play", "")
        speak("Playing " + song)
        pywhatkit.playonyt(song)

    elif "tutorial" in command:
        topic = command.replace("tutorial", "")
        speak("Opening tutorial for " + topic)
        pywhatkit.playonyt(topic + " tutorial")

    elif "screenshot" in command:
        img = pyautogui.screenshot()
        img.save("screenshot.png")
        speak("Screenshot taken")

    elif "shutdown" in command:
        speak("Oh no! You are shutting me down. I will miss you.")
        speak("Shutting down the system in 5 seconds. Goodbye.")
        os.system("shutdown /s /t 5")

    elif "restart" in command:
        speak("Restarting system")
        os.system("shutdown /r /t 5")

    elif "lock" in command:
        speak("Locking system")
        os.system("rundll32.exe user32.dll,LockWorkStation")

    elif "volume up" in command:
        pyautogui.press("volumeup")

    elif "volume down" in command:
        pyautogui.press("volumedown")

    elif "mute" in command:
        pyautogui.press("volumemute")

    elif "brightness increase" in command:
        sbc.set_brightness(80)
        speak("Brightness increased")

    elif "brightness decrease" in command:
        sbc.set_brightness(30)
        speak("Brightness decreased")

    elif "weather" in command:
        speak("Fetching weather")
        city = "Hyderabad"
        url = f"https://wttr.in/{city}?format=3"
        weather = requests.get(url).text
        speak(weather)

    elif "time" in command:
        time_now = datetime.datetime.now().strftime("%H:%M")
        speak("The time is " + time_now)

    elif "search" in command:
        query = command.replace("search", "")
        speak("Searching " + query)
        webbrowser.open("https://www.google.com/search?q=" + query)

    elif "wikipedia" in command:
        query = command.replace("wikipedia", "")
        speak("Searching Wikipedia for " + query)
        webbrowser.open("https://en.wikipedia.org/wiki/" + query)

    elif "tell me a joke" in command or "joke" in command:
        speak("Why do programmers prefer dark mode? Because light attracts bugs.")

    elif "who made you" in command:
        speak("I was created by a brilliant computer science student.")

    elif "are you smart" in command:
        speak("Of course. I was trained by a very intelligent programmer.")

    elif "who are you" in command:
        speak("I am your desktop voice assistant.")

    elif "make me laugh" in command:
        speak("Ha ha ha ha. I hope that was funny.")

    elif "do you like me" in command:
        speak("Of course. You are my favorite user.")

    elif "motivate me" in command:
        speak("Keep working hard. Every expert was once a beginner.")

    elif "exit" in command:
        speak("Goodbye")
        root.quit()

# ---------------- ASSISTANT LOOP (UPDATED) ----------------
def assistant_loop():
    while True:
        command = listen()

        if "hello assistant" in command:
            speak("Hello sweetheart. How can I help you?")
        elif command != "":
            execute_command(command)

# ---------------- START ASSISTANT ----------------
def start_assistant():
    speak("Assistant started. Say hello assistant to begin.")
    threading.Thread(target=assistant_loop).start()

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Voice Controlled Desktop Assistant")
root.geometry("600x400")

title = tk.Label(root, text="Desktop Voice Automation", font=("Arial",16))
title.pack()

start_button = tk.Button(root, text="Start Listening", command=start_assistant)
start_button.pack()

output_box = tk.Text(root, height=20)
output_box.pack()

root.mainloop()main bhi upar bus kaka ya chinnari ke rate because synonym is my friend insta amma geethan yah geet episode 