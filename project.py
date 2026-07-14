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
import time

engine = pyttsx3.init()
typing_mode = False
active_window = None  # keeps track if we are in notepad/cmd

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
        speak("Sorry, I didn't understand")
        return ""

# ---------------- COMMAND EXECUTION ----------------
def execute_command(command):
    global typing_mode, active_window

    # ---------- TYPING ----------
    if typing_mode:
        pyautogui.write(command + " ")

    # ---------- OPEN APPLICATIONS ----------
    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")
        time.sleep(1)
        pyautogui.click(200, 200)
        typing_mode = True
        active_window = "notepad"
        speak("Voice typing activated in Notepad")

    elif "open cmd" in command or "open command prompt" in command:
        speak("Opening Command Prompt")
        os.system("start cmd")
        time.sleep(1)
        pyautogui.click(200, 200)
        typing_mode = True
        active_window = "cmd"
        speak("Voice typing activated in CMD")

    # ---------- CLOSE APPLICATIONS ----------
    elif "close chrome" in command:
        speak("Closing Chrome")
        os.system("taskkill /f /im chrome.exe")

    elif "close calculator" in command:
        speak("Closing Calculator")
        os.system("taskkill /f /im CalculatorApp.exe")

    elif "close vs code" in command:
        speak("Closing VS Code")
        os.system("taskkill /f /im Code.exe")

    elif "close word" in command:
        speak("Closing Microsoft Word")
        os.system("taskkill /f /im WINWORD.EXE")

    elif "close excel" in command:
        speak("Closing Microsoft Excel")
        os.system("taskkill /f /im EXCEL.EXE")

    elif "close powerpoint" in command:
        speak("Closing Microsoft PowerPoint")
        os.system("taskkill /f /im POWERPNT.EXE")

    elif "close notepad" in command:
        speak("Closing Notepad")
        os.system("taskkill /f /im notepad.exe")
        typing_mode = False
        active_window = None

    elif "close file explorer" in command:
        speak("Closing File Explorer")
        os.system("taskkill /f /im explorer.exe")

    # ---------- YOUTUBE ----------
    elif "play" in command:
        song = command.replace("play", "")
        speak("Playing " + song)
        pywhatkit.playonyt(song)

    elif "tutorial" in command:
        topic = command.replace("tutorial", "")
        speak("Opening tutorial for " + topic)
        pywhatkit.playonyt(topic + " tutorial")

    # ---------- SCREENSHOT ----------
    elif "screenshot" in command:
        img = pyautogui.screenshot()
        img.save("screenshot.png")
        speak("Screenshot taken")

    # ---------- SYSTEM COMMANDS ----------
    elif "shutdown" in command:
        speak("Shutting down the system in 5 seconds.")
        os.system("shutdown /s /t 5")

    elif "restart" in command:
        speak("Restarting system")
        os.system("shutdown /r /t 5")

    elif "lock" in command:
        speak("Locking system")
        os.system("rundll32.exe user32.dll,LockWorkStation")

    # ---------- VOLUME ----------
    elif "volume up" in command:
        pyautogui.press("volumeup")

    elif "volume down" in command:
        pyautogui.press("volumedown")

    elif "mute" in command:
        pyautogui.press("volumemute")

    # ---------- BRIGHTNESS ----------
    elif "brightness increase" in command:
        sbc.set_brightness(80)
        speak("Brightness increased")

    elif "brightness decrease" in command:
        sbc.set_brightness(30)
        speak("Brightness decreased")

    # ---------- WEATHER ----------
    elif "weather" in command:
        speak("Fetching weather")
        city = "Hyderabad"
        url = f"https://wttr.in/{city}?format=3"
        weather = requests.get(url).text
        speak(weather)

    # ---------- TIME ----------
    elif "time" in command:
        time_now = datetime.datetime.now().strftime("%H:%M")
        speak("The time is " + time_now)

    # ---------- SEARCH ----------
    elif "search" in command:
        query = command.replace("search", "")
        speak("Searching " + query)
        webbrowser.open("https://www.google.com/search?q=" + query)

    elif "wikipedia" in command:
        query = command.replace("wikipedia", "")
        speak("Searching Wikipedia for " + query)
        webbrowser.open("https://en.wikipedia.org/wiki/" + query)

    # ---------- FUNNY / INFO ----------
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


# ---------------- ASSISTANT LOOP ----------------
def assistant_loop():
    while True:
        command = listen()
        if "hello assistant" in command:
            speak("Hello boss. How can I help you?")
            continue  # keep listening after greeting
        elif command != "":
            execute_command(command)


# ---------------- START ASSISTANT ----------------
def start_assistant():
    threading.Thread(target=assistant_loop).start()


# ---------------- GUI ----------------
root = tk.Tk()
root.title("Voice Controlled Desktop Assistant")
root.geometry("600x400")

title = tk.Label(root, text="Desktop Voice Automation", font=("Arial", 16))
title.pack()

start_button = tk.Button(root, text="Start Listening", command=start_assistant)
start_button.pack()
open calculator 
output_box = tk.Text(root, height=20)
output_box.pack()

root.mainloop()