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

    # -------- GREETING --------
    if "hello assistant" in command or "hi assistant" in command:
        speak("Hello boss, how can I help you")

    # -------- OPEN APPS --------
    elif "open chrome" in command:
        speak("Opening Chrome")
        os.system("start chrome")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "search" in command:
        query = command.replace("search", "").strip()
        speak("Searching for " + query)
        webbrowser.open("https://www.google.com/search?q=" + query)

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "play" in command:
        song = command.replace("play", "")
        speak("Playing " + song)
        pywhatkit.playonyt(song)

    elif "tutorial" in command:
        topic = command.replace("tutorial", "")
        speak("Opening tutorial for " + topic)
        pywhatkit.playonyt(topic + " tutorial")

    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("calc")

    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")
        time.sleep(1)

    elif "open cmd" in command or "open command prompt" in command:
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

    elif "open camera" in command:
        speak("Opening Camera")
        os.system("start microsoft.windows.camera:")

    elif "open chatgpt" in command:
        speak("Opening ChatGPT")
        webbrowser.open("https://chat.openai.com")

    # -------- NOTEPAD VOICE TYPING --------
    elif "voice typing notepad" in command:
        speak("Opening Notepad and starting voice typing")
        os.system("notepad")
        time.sleep(2)
        speak("Please start speaking. Say stop typing to finish")
        while True:
            text = listen()
            if "stop typing" in text:
                speak("Stopping voice typing")
                break
            pyautogui.write(text + " ")

    # -------- SCREENSHOT --------
    elif "screenshot" in command:
        img = pyautogui.screenshot()
        img.save("screenshot.png")
        speak("Screenshot taken")

    # -------- SYSTEM COMMANDS --------
    elif "shutdown" in command:
        speak("Shutting down system in 5 seconds")
        os.system("shutdown /s /t 5")

    elif "restart" in command:
        speak("Restarting system")
        os.system("shutdown /r /t 5")

    elif "lock" in command:
        speak("Locking system")
        os.system("rundll32.exe user32.dll,LockWorkStation")

    elif "sleep" in command:
        speak("System going to sleep")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

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

    # -------- WEATHER & TIME --------
    elif "weather" in command:
        speak("Fetching weather")
        city = "Hyderabad"
        url = f"https://wttr.in/{city}?format=3"
        weather = requests.get(url).text
        speak(weather)

    elif "time" in command:
        time_now = datetime.datetime.now().strftime("%H:%M")
        speak("The time is " + time_now)

    elif "wikipedia" in command:
        query = command.replace("wikipedia", "").strip()
        speak("Searching Wikipedia for " + query)
        webbrowser.open("https://en.wikipedia.org/wiki/" + query)

    # -------- CALCULATOR --------
    elif "calculate" in command:
        try:
            expression = command.replace("calculate", "").strip()
            expression = expression.replace("plus", "+").replace("add", "+")
            expression = expression.replace("minus", "-").replace("times", "*")
            expression = expression.replace("multiplied by", "*")
            expression = expression.replace("divided by", "/")
            expression = expression.replace("power", "**")

            if "sin" in expression:
                number = float(expression.replace("sin",""))
                result = math.sin(math.radians(number))
            elif "cos" in expression:
                number = float(expression.replace("cos",""))
                result = math.cos(math.radians(number))
            elif "tan" in expression:
                number = float(expression.replace("tan",""))
                result = math.tan(math.radians(number))
            elif "log" in expression:
                number = float(expression.replace("log",""))
                result = math.log10(number)
            elif "ln" in expression:
                number = float(expression.replace("ln",""))
                result = math.log(number)
            elif "square root" in expression:
                number = float(expression.replace("square root",""))
                result = math.sqrt(number)
            else:
                result = eval(expression)

            speak("The answer is " + str(result))
            output_box.insert(tk.END,"Result: "+str(result)+"\n")
        except:
            speak("Sorry I cannot calculate that")

    # -------- SCROLL CONTROL FOR ANY APP --------
    elif "scroll down slowly" in command:
        for _ in range(5):
            pyautogui.scroll(-200)  # scroll down
            time.sleep(0.3)
        speak("Scrolling down slowly")

    elif "scroll up slowly" in command:
        for _ in range(5):
            pyautogui.scroll(200)   # scroll up
            time.sleep(0.3)
        speak("Scrolling up slowly")

    # -------- FUN / INFO --------
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
            speak("Hello boss, how can I help you")
        else:
            execute_command(command)

# ---------------- START ASSISTANT ----------------
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