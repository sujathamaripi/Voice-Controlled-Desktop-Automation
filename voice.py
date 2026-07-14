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

# ---------------- SPEAK ---------------- #
def speak(text):
    output_box.insert(tk.END,"Assistant: "+text+"\n")
    engine.say(text)
    engine.runAndWait()

# ---------------- LISTEN ---------------- #
def listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        output_box.insert(tk.END,"Listening...\n")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        output_box.insert(tk.END,"You: "+command+"\n")
        return command.lower()

    except:
        speak("Sorry I didn't understand")
        return ""

# ---------------- COMMAND EXECUTION ---------------- #
def execute_command(command):

    # ---------- OPEN APPLICATIONS ---------- #
    if "open chrome" in command:
        speak("Opening Chrome")
        os.system("start chrome")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open calculator" in command:
        speak("Opening calculator")
        os.system("calc")

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

    # ---------- CLOSE APPLICATIONS ---------- #
    elif "close chrome" in command:
        speak("Closing Chrome")
        os.system("taskkill /f /im chrome.exe")

    elif "close youtube" in command:
        speak("Closing YouTube")
        os.system("taskkill /f /im chrome.exe")

    elif "close whatsapp" in command:
        speak("Closing WhatsApp")
        os.system("taskkill /f /im chrome.exe")

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

    elif "close calculator" in command:
        speak("Closing Calculator")
        os.system("taskkill /f /im CalculatorApp.exe")

    elif "close file explorer" in command:
        speak("Closing File Explorer")
        os.system("taskkill /f /im explorer.exe")

    elif "close window" in command:
        speak("Closing current window")
        pyautogui.hotkey("alt","f4")

    # ---------- MEDIA / SEARCH ---------- #
    elif "play" in command:
        song = command.replace("play","")
        speak("Playing "+song)
        pywhatkit.playonyt(song)

    elif "tutorial" in command:
        topic = command.replace("tutorial","")
        speak("Opening tutorial for "+topic)
        pywhatkit.playonyt(topic+" tutorial")

    elif "search" in command:
        query = command.replace("search","")
        speak("Searching "+query)
        webbrowser.open("https://www.google.com/search?q="+query)

    elif "wikipedia" in command:
        query = command.replace("wikipedia","")
        speak("Searching Wikipedia for "+query)
        webbrowser.open("https://en.wikipedia.org/wiki/"+query)

    # ---------- SCREENSHOT ---------- #
    elif "screenshot" in command:
        img = pyautogui.screenshot()
        img.save("screenshot.png")
        speak("Screenshot taken")

    # ---------- SYSTEM CONTROLS ---------- #
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

    # ---------- VOLUME ---------- #
    elif "volume up" in command:
        pyautogui.press("volumeup")

    elif "volume down" in command:
        pyautogui.press("volumedown")

    elif "mute" in command:
        pyautogui.press("volumemute")

    # ---------- BRIGHTNESS ---------- #
    elif "brightness increase" in command:
        sbc.set_brightness(80)
        speak("Brightness increased")

    elif "brightness decrease" in command:
        sbc.set_brightness(30)
        speak("Brightness decreased")

    # ---------- WEATHER ---------- #
    elif "weather" in command:
        city="Hyderabad"
        url=f"https://wttr.in/{city}?format=3"
        weather=requests.get(url).text
        speak(weather)

    # ---------- TIME ---------- #
    elif "time" in command:
        time=datetime.datetime.now().strftime("%H:%M")
        speak("The time is "+time)

    # ---------- CALCULATOR ---------- #
    elif "calculate" in command:
        try:
            expression=command.replace("calculate","")

            expression=expression.replace("plus","+")
            expression=expression.replace("minus","-")
            expression=expression.replace("times","*")
            expression=expression.replace("divided by","/")

            expression=expression.strip()

            result=eval(expression)

            speak("The answer is "+str(result))
            output_box.insert(tk.END,"Result: "+str(result)+"\n")

        except:
            speak("Sorry I cannot calculate that")

    elif "exit" in command:
        speak("Goodbye")
        root.quit()

# ---------------- ASSISTANT LOOP ---------------- #
def assistant_loop():
    while True:
        command=listen()

        if "hello assistant" in command:
            speak("Yes, how can I help you?")
            command=listen()
            execute_command(command)

# ---------------- START BUTTON ---------------- #
def start_assistant():
    threading.Thread(target=assistant_loop).start()

# ---------------- GUI ---------------- #
root=tk.Tk()
root.title("Voice Controlled Desktop Assistant")
root.geometry("600x400")

title=tk.Label(root,text="Desktop Voice Automation",font=("Arial",16))
title.pack()

start_button=tk.Button(root,text="Start Listening",command=start_assistant)
start_button.pack()

output_box=tk.Text(root,height=20)
output_box.pack()

root.mainloop()