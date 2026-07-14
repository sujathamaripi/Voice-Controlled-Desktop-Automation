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

    # Greeting
    if "hello assistant" in command or "hi assistant" in command or "hey assistant" in command:
        speak("Hello boss, how can I help you")

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

    elif "play" in command:
        song = command.replace("play","")
        speak("Playing " + song)
        pywhatkit.playonyt(song)

    elif "tutorial" in command:
        topic = command.replace("tutorial","")
        speak("Opening tutorial for " + topic)
        pywhatkit.playonyt(topic + " tutorial")

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

    elif "open camera" in command:
        speak("Opening Camera")
        os.system("start microsoft.windows.camera:")

    elif "open chatgpt" in command:
        speak("Opening ChatGPT")
        webbrowser.open_new_tab("https://chatgpt.com")

    # NOTEPAD VOICE TYPING FEATURE
    elif "open notepad and type" in command or "voice typing notepad" in command:
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

    elif "screenshot" in command:
        img = pyautogui.screenshot()
        img.save("screenshot.png")
        speak("Screenshot taken")

    # Funny Shutdown
    elif "shutdown" in command:
        speak("Okay boss, I am going to sleep now. Don't miss me too much!")
        output_box.insert(tk.END,"Assistant: System will shutdown in 5 seconds...\n")
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
        city="Hyderabad"
        url=f"https://wttr.in/{city}?format=3"
        weather=requests.get(url).text
        speak(weather)

    elif "news" in command:
        speak("Opening latest news")
        webbrowser.open("https://news.google.com")

    elif "time" in command:
        time_now=datetime.datetime.now().strftime("%H:%M")
        speak("The time is "+time_now)

    elif "search" in command:
        query=command.replace("search","").strip()
        speak("Searching "+query)
        webbrowser.open("https://www.google.com/search?q="+query)

    elif "wikipedia" in command:
        query=command.replace("wikipedia","").strip()
        speak("Searching Wikipedia for "+query)
        webbrowser.open("https://en.wikipedia.org/wiki/"+query)

    # ADVANCED VOICE CALCULATOR
    elif "calculate" in command:
        try:
            expression = command.replace("calculate", "").strip()

            expression = expression.replace("plus", "+")
            expression = expression.replace("add", "+")
            expression = expression.replace("minus", "-")
            expression = expression.replace("times", "*")
            expression = expression.replace("multiplied by", "*")
            expression = expression.replace("into", "*")
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