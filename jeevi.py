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
import cv2   # ✅ added for camera

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

    # -------- GREETING --------
    if "hello assistant" in command or "hi assistant" in command:
        speak("Hello boss, how can I help you")

    # -------- TYPING CONTROL --------
    elif "start typing" in command:
        typing_mode = True
        speak("Typing mode activated")

    elif "stop typing" in command:
        typing_mode = False
        speak("Typing stopped")

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

    elif "open cmd" in command:
        speak("Opening Command Prompt")
        os.system("start cmd")

    # -------- NEW FEATURES ADDED --------

    elif "open gmail" in command:
        speak("Opening Gmail")
        webbrowser.open("https://mail.google.com")

    elif "open wordpad" in command:
        speak("Opening WordPad")
        os.system("write")

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

    elif "take photo" in command or "capture photo" in command:
        speak("Opening camera and taking photo")

        cam = cv2.VideoCapture(0)
        time.sleep(2)

        ret, frame = cam.read()

        if ret:
            cv2.imwrite("photo.png", frame)
            speak("Photo captured and saved")
        else:
            speak("Failed to capture photo")

        cam.release()

    # -------- SCREENSHOT --------
    elif "screenshot" in command:
        img = pyautogui.screenshot()
        img.save("screenshot.png")
        speak("Screenshot taken")

    # -------- CALCULATOR --------
    elif any(word in command for word in ["calculate","what is","solve","plus","minus","times","divided","into","x"]):
        try:
            expression = command.lower()

            expression = expression.replace("calculate","")\
                                   .replace("what is","")\
                                   .replace("solve","")

            expression = expression.replace("plus","+")\
                                   .replace("add","+")\
                                   .replace("minus","-")\
                                   .replace("times","*")\
                                   .replace("multiplied by","*")\
                                   .replace("into","*")\
                                   .replace("x","*")\
                                   .replace("divided by","/")\
                                   .replace("by","/")\
                                   .replace("power","**")

            expression = expression.strip()

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

    # -------- SCROLL --------
    elif "scroll down slowly" in command:
        for _ in range(5):
            pyautogui.scroll(-200)
            time.sleep(0.3)
        speak("Scrolling down slowly")

    elif "scroll up slowly" in command:
        for _ in range(5):
            pyautogui.scroll(200)
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

    # -------- EXIT --------
    elif "exit" in command:
        speak("Goodbye")
        root.quit()

# ---------------- LOOP ----------------
def assistant_loop():
    global typing_mode

    while True:
        command = listen()

        if typing_mode:
            if "stop typing" in command:
                typing_mode = False
                speak("Typing stopped")
            else:
                pyautogui.write(command + " ")

        else:
            execute_command(command)

# ---------------- START ----------------
def start_assistant():
    threading.Thread(target=assistant_loop).start()

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("600x400")

tk.Label(root, text="Desktop Voice Automation", font=("Arial",16)).pack()

tk.Button(root, text="Start Listening", command=start_assistant).pack()

output_box = tk.Text(root, height=20)
output_box.pack()

root.mainloop()