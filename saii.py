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

engine = pyttsx3.init()

def speak(text):
    output_box.insert(tk.END, "Assistant: " + text + "\n")
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        output_box.insert(tk.END,"Listening...\n")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        output_box.insert(tk.END,"You: " + command + "\n")
        return command.lower()

    except:
        speak("Sorry I didn't understand")
        return ""

def execute_command(command):

    if "open chrome" in command:
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

    elif "play" in command:
        song = command.replace("play","")
        speak("Playing " + song)
        pywhatkit.playonyt(song)

    # TUTORIAL COMMAND
    elif "tutorial" in command:
        topic = command.replace("tutorial","")
        speak("Opening tutorial for " + topic)
        pywhatkit.playonyt(topic + " tutorial")

    elif "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")
        speak("Opening WhatsApp")

    elif "open vs code" in command:
        os.system("code")

    elif "open word" in command:
        os.system("start winword")

    elif "open excel" in command:
        os.system("start excel")

    elif "open powerpoint" in command:
        os.system("start powerpnt")

    elif "open file explorer" in command:
        os.system("explorer")

    elif "open camera" in command:
        os.system("start microsoft.windows.camera:")

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
        speak("System going to sleep")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

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

    elif "news" in command:
        speak("Opening latest news")
        webbrowser.open("https://news.google.com")

    elif "meeting" in command or "online class" in command:
        speak("Opening meeting link")
        webbrowser.open("YOUR_MEETING_LINK")

    elif "time" in command:
        time = datetime.datetime.now().strftime("%H:%M")
        speak("The time is " + time)

    # GOOGLE SEARCH
    elif "search" in command or "google search" in command:
        try:
            query = command.replace("search","").replace("google search","").strip()
            speak("Searching " + query)
            webbrowser.open("https://www.google.com/search?q=" + query)
        except:
            speak("Sorry I cannot search that")

    # WIKIPEDIA SEARCH
    elif "wikipedia" in command:
        try:
            query = command.replace("wikipedia","").strip()
            speak("Searching Wikipedia for " + query)
            webbrowser.open("https://en.wikipedia.org/wiki/" + query)
        except:
            speak("Sorry I cannot open Wikipedia")

    # VOICE CALCULATOR
    elif "calculate" in command:
        try:
            expression = command.replace("calculate","")

            expression = expression.replace("plus","+")
            expression = expression.replace("add","+")
            expression = expression.replace("minus","-")
            expression = expression.replace("multiplied by","*")
            expression = expression.replace("times","*")
            expression = expression.replace("into","*")
            expression = expression.replace("divided by","/")
            expression = expression.replace("power","**")

            expression = expression.strip()

            if "sin" in expression:
                number = float(expression.replace("sin","").strip())
                result = math.sin(math.radians(number))

            elif "cos" in expression:
                number = float(expression.replace("cos","").strip())
                result = math.cos(math.radians(number))

            elif "tan" in expression:
                number = float(expression.replace("tan","").strip())
                result = math.tan(math.radians(number))

            elif "square root" in expression:
                number = float(expression.replace("square root","").strip())
                result = math.sqrt(number)

            else:
                result = eval(expression)

            speak("The answer is " + str(result))
            output_box.insert("end","Result: " + str(result) + "\n")

        except:
            speak("Sorry I cannot calculate that")

    elif "exit" in command:
        speak("Goodbye")
        root.quit()


def assistant_loop():
    while True:
        command = listen()
        execute_command(command)

def start_assistant():
    threading.Thread(target=assistant_loop).start()

root = tk.Tk()
root.title("Voice Controlled Desktop Assistant")
root.geometry("600x400")

title = tk.Label(root,text="Desktop Voice Automation",font=("Arial",16))
title.pack()

start_button = tk.Button(root,text="Start Listening",command=start_assistant)
start_button.pack()

output_box = tk.Text(root,height=20)
output_box.pack()

root.mainloop()