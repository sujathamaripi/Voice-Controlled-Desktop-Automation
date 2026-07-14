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
from selenium import webdriver
from selenium.webdriver.common.by import By

# ---------------- INITIAL SETUP ----------------
engine = pyttsx3.init()
typing_mode = False
driver = None  # For Selenium Google search

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
    global driver

    # ---------- GREETING ----------
    if "hello assistant" in command or "hi assistant" in command or "hey assistant" in command:
        speak("Hello boss, how can I help you")

    # ---------- OPEN APPS ----------
    elif "open chrome" in command:
        speak("Opening Chrome")
        os.system("start chrome")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("calc")

    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")
        time.sleep(1)
        pyautogui.click()
        typing_mode = True
        speak("Voice typing activated. Say 'stop typing' to finish.")

    elif "open cmd" in command:
        speak("Opening Command Prompt")
        os.system("start cmd")

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

    # ---------- CLOSE APPS ----------
    elif "close chrome" in command:
        speak("Closing Chrome")
        os.system("taskkill /f /im chrome.exe")

    elif "close calculator" in command:
        speak("Closing Calculator")
        os.system("taskkill /f /im CalculatorApp.exe")

    elif "close notepad" in command:
        speak("Closing Notepad")
        os.system("taskkill /f /im notepad.exe")

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

    elif "close file explorer" in command:
        speak("Closing File Explorer")
        os.system("taskkill /f /im explorer.exe")

    # ---------- VOICE TYPING ----------
    elif typing_mode:
        if "stop typing" in command:
            typing_mode = False
            speak("Voice typing stopped")
        else:
            pyautogui.write(command + " ")

    # ---------- GOOGLE SEARCH WITH SELENIUM ----------
    elif "search" in command:
        query = command.replace("search", "").strip()
        speak("Searching for " + query)

        driver = webdriver.Chrome()
        driver.get("https://www.google.com")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.submit()
        speak("Here are the results. You can say 'open first result'")

    # ---------- OPEN SEARCH RESULTS ----------
    elif "open first result" in command:
        try:
            links = driver.find_elements(By.XPATH, "//h3")
            links[0].click()
            speak("Opening first result")
        except:
            speak("Unable to open first result")

    elif "open second result" in command:
        try:
            links = driver.find_elements(By.XPATH, "//h3")
            links[1].click()
            speak("Opening second result")
        except:
            speak("Unable to open second result")

    elif "open third result" in command:
        try:
            links = driver.find_elements(By.XPATH, "//h3")
            links[2].click()
            speak("Opening third result")
        except:
            speak("Unable to open third result")

    # ---------- SCROLL CONTROL ----------
    elif "scroll down" in command:
        try:
            driver.execute_script("window.scrollBy(0,500)")
            speak("Scrolling down")
        except:
            speak("Unable to scroll down")

    elif "scroll up" in command:
        try:
            driver.execute_script("window.scrollBy(0,-500)")
            speak("Scrolling up")
        except:
            speak("Unable to scroll up")

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

    # ---------- MEDIA ----------
    elif "play" in command:
        song = command.replace("play", "").strip()
        speak("Playing " + song)
        pywhatkit.playonyt(song)

    elif "tutorial" in command:
        topic = command.replace("tutorial", "").strip()
        speak("Opening tutorial for " + topic)
        pywhatkit.playonyt(topic + " tutorial")

    # ---------- SCREENSHOT ----------
    elif "screenshot" in command:
        img = pyautogui.screenshot()
        img.save("screenshot.png")
        speak("Screenshot taken")

    # ---------- SYSTEM CONTROLS ----------
    elif "shutdown" in command:
        speak("Shutting down in 5 seconds")
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

    elif "time" in command:
        time_now = datetime.datetime.now().strftime("%H:%M")
        speak("The time is " + time_now)

    elif "weather" in command:
        city = "Hyderabad"
        url = f"https://wttr.in/{city}?format=3"
        weather = requests.get(url).text
        speak(weather)

    # ---------- VOICE CALCULATOR ----------
    elif "calculate" in command:
        try:
            expression = command.replace("calculate", "").strip()
            expression = expression.replace("plus", "+").replace("add","+")
            expression = expression.replace("minus", "-").replace("times", "*")
            expression = expression.replace("multiplied by", "*").replace("into","*")
            expression = expression.replace("divided by", "/").replace("power","**")

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

    # ---------- FUN / INFO ----------
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
        execute_command(command)

# ---------------- START ASSISTANT ----------------
def start_assistant():
    threading.Thread(target=assistant_loop).start()

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Voice Controlled Desktop Assistant")
root.geometry("700x500")

title = tk.Label(root, text="Desktop Voice Automation", font=("Arial",16))
title.pack()

start_button = tk.Button(root, text="Start Listening", command=start_assistant)
start_button.pack()

output_box = tk.Text(root, height=25)
output_box.pack()

root.mainloop()