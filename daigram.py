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

    # -------- GLOBAL TYPING MODE --------
    if typing_mode and "stop typing" not in command:
        pyautogui.write(command + " ")
        return

    # -------- GREETING --------
    if "hello assistant" in command:
        speak("Hello boss, how can I help you")

    # -------- OPEN APPS --------
    elif "open chrome" in command:
        speak("Opening Chrome")
        os.system("start chrome")

    elif "open google" in command:
        speak("Opening Google")
        os.system("start chrome https://www.google.com")

    # -------- FIXED SEARCH --------
    elif "search" in command:
        query = command.replace("search", "").strip()
        speak("Searching for " + query)
        os.system(f"start chrome https://www.google.com/search?q={query}")

    elif "open youtube" in command:
        speak("Opening YouTube")
        os.system("start chrome https://www.youtube.com")

    elif "open whatsapp" in command:
        speak("Opening WhatsApp")
        os.system("start chrome https://web.whatsapp.com")

    elif "play" in command:
        song = command.replace("play", "")
        speak("Playing " + song)
        pywhatkit.playonyt(song)

    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("calc")

    # -------- NOTEPAD AUTO TYPE --------
    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")
        time.sleep(2)

        # click inside notepad
        pyautogui.click(400, 400)

        typing_mode = True
        speak("You can start speaking, I will type for you")

    elif "stop typing" in command:
        typing_mode = False
        speak("Typing stopped")

    elif "open cmd" in command:
        speak("Opening Command Prompt")
        os.system("start cmd")

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

    # -------- SCREENSHOT --------
    elif "screenshot" in command:
        path = os.path.join(os.getcwd(), "screenshot.png")
        img = pyautogui.screenshot()
        img.save(path)
        speak(f"Screenshot saved in {path}")

    # -------- SYSTEM --------
    elif "shutdown" in command:
        speak("Shutting down system in 5 seconds")
        os.system("shutdown /s /t 5")

    elif "restart" in command:
        speak("Restarting system")
        os.system("shutdown /r /t 5")

    elif "lock" in command:
        speak("Locking system")
        os.system("rundll32.exe user32.dll,LockWorkStation")

    # -------- VOLUME --------
    elif "volume up" in command:
        pyautogui.press("volumeup")

    elif "volume down" in command:
        pyautogui.press("volumedown")

    elif "mute" in command:
        pyautogui.press("volumemute")

    # -------- BRIGHTNESS --------
    elif "brightness increase" in command:
        sbc.set_brightness(80)
        speak("Brightness increased")

    elif "brightness decrease" in command:
        sbc.set_brightness(30)
        speak("Brightness decreased")

    # -------- WEATHER --------
    elif "weather" in command:
        speak("Fetching weather")
        city = "Hyderabad"
        url = f"https://wttr.in/{city}?format=3"
        weather = requests.get(url).text
        speak(weather)

    # -------- TIME --------
    elif "time" in command:
        time_now = datetime.datetime.now().strftime("%H:%M")
        speak("The time is " + time_now)

    # -------- CALCULATOR --------
    elif "calculate" in command:
        try:
            expression = command.replace("calculate", "").strip()
            expression = expression.replace("plus","+").replace("add","+")
            expression = expression.replace("minus","-").replace("times","*")
            expression = expression.replace("multiplied by","*")
            expression = expression.replace("divided by","/")
            expression = expression.replace("power","**")

            result = eval(expression)

            speak("The answer is " + str(result))
            output_box.insert(tk.END, "Result: " + str(result) + "\n")

        except:
            speak("Sorry I cannot calculate that")

    # -------- FUN --------
    elif "tell me a joke" in command:
        speak("Why do programmers prefer dark mode? Because light attracts bugs.")

    elif "motivate me" in command:
        speak("Keep working hard. Every expert was once a beginner.")

    elif "exit" in command:
        speak("Goodbye")
        root.quit()

# ---------------- LOOP ----------------
def assistant_loop():
    while True:
        command = listen()
        execute_command(command)

# ---------------- START ----------------
def start_assistant():
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

root.mainloop()