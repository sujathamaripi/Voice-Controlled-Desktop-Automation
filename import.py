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

engine = pyttsx3.init()
driver = None  # Selenium driver for Google search
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
    global typing_mode, driver

    # ---------- GREETING ----------
    if "hello assistant" in command or "hi assistant" in command:
        speak("Hello boss, how can I help you?")

    # ---------- OPEN APPLICATIONS ----------
    elif "open chrome" in command:
        speak("Opening Chrome")
        os.system("start chrome")

    elif "open cmd" in command:
        speak("Opening Command Prompt")
        os.system("start cmd")

    elif "open google" in command:
        speak("Opening Google")
        os.system("start chrome https://www.google.com")

    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("calc")

    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")

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

    elif "open camera" in command:
        speak("Opening Camera")
        os.system("start microsoft.windows.camera:")

    elif "open chatgpt" in command:
        speak("Opening ChatGPT")
        webbrowser.open_new_tab("https://chat.openai.com")

    # ---------- CLOSE APPLICATIONS ----------
    elif "close chrome" in command:
        os.system("taskkill /f /im chrome.exe")
        speak("Chrome closed")

    elif "close cmd" in command:
        os.system("taskkill /f /im cmd.exe")
        speak("Command Prompt closed")

    elif "close google" in command:
        os.system("taskkill /f /im chrome.exe")
        speak("Google closed")

    elif "close calculator" in command:
        os.system("taskkill /f /im Calculator.exe")
        speak("Calculator closed")

    elif "close notepad" in command:
        os.system("taskkill /f /im notepad.exe")
        speak("Notepad closed")

    elif "close youtube" in command:
        os.system("taskkill /f /im chrome.exe")
        speak("YouTube closed")

    elif "close whatsapp" in command:
        os.system("taskkill /f /im chrome.exe")
        speak("WhatsApp closed")

    elif "close vs code" in command:
        os.system("taskkill /f /im Code.exe")
        speak("VS Code closed")

    elif "close word" in command:
        os.system("taskkill /f /im WINWORD.EXE")
        speak("Word closed")

    elif "close excel" in command:
        os.system("taskkill /f /im EXCEL.EXE")
        speak("Excel closed")

    elif "close powerpoint" in command:
        os.system("taskkill /f /im POWERPNT.EXE")
        speak("PowerPoint closed")

    elif "close file explorer" in command:
        os.system("taskkill /f /im explorer.exe")
        speak("File Explorer closed")  # Explorer will restart automatically

    elif "close camera" in command:
        os.system("taskkill /f /im WindowsCamera.exe")
        speak("Camera closed")

    elif "close chatgpt" in command:
        os.system("taskkill /f /im chrome.exe")
        speak("ChatGPT closed")

    # ---------- VOICE TYPING ----------
    elif "start typing" in command:
        typing_mode = True
        speak("Voice typing activated")

    elif "stop typing" in command:
        typing_mode = False
        speak("Voice typing stopped")

    elif typing_mode:
        pyautogui.write(command + " ")

    # ---------- NOTEPAD VOICE TYPING ----------
    elif "voice typing notepad" in command or "open notepad and type" in command:
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

    # ---------- SCREENSHOT ----------
    elif "screenshot" in command:
        img = pyautogui.screenshot()
        img.save("screenshot.png")
        speak("Screenshot taken. Check the program folder")

    # ---------- SYSTEM COMMANDS ----------
    elif "shutdown" in command:
        speak("Okay boss, shutting down in 5 seconds!")
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

    # ---------- VOLUME CONTROL ----------
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

    # ---------- GOOGLE SEARCH WITH SELENIUM ----------
    elif "search" in command:
        query = command.replace("search","").strip()
        speak("Searching for " + query)
        driver = webdriver.Chrome()
        driver.get("https://www.google.com")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.submit()
        speak("Here are the results. You can say open first result, second result, or scroll up/down.")

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
            pyautogui.scroll(-200)
            speak("Scrolling down slowly")

    elif "scroll up" in command:
        try:
            driver.execute_script("window.scrollBy(0,-500)")
            speak("Scrolling up")
        except:
            pyautogui.scroll(200)
            speak("Scrolling up slowly")

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

# ---------- YOUTUBE CONTROLS ----------
    elif "play video" in command or "pause video" in command:
        pyautogui.press("space")
        speak("Toggling play or pause")

    elif "next video" in command:
        pyautogui.hotkey("shift", "n")
        speak("Playing next video")

    elif "previous video" in command:
        pyautogui.hotkey("shift", "p")
        speak("Playing previous video")

    elif "fullscreen" in command:
        pyautogui.press("f")
        speak("Entering fullscreen")

    elif "exit fullscreen" in command:
        pyautogui.press("esc")
        speak("Exiting fullscreen")


    # ---------- WHATSAPP MESSAGE ----------
    elif "send whatsapp message" in command:
        speak("Tell me the phone number with country code")
        number = listen()

        speak("What is the message")
        message = listen()

        speak("Sending message now")
        try:
            pywhatkit.sendwhatmsg_instantly(number, message, wait_time=10, tab_close=True)
            speak("Message sent successfully")
        except:
            speak("Failed to send message")

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

    # ---------- CALCULATOR ----------
    elif "calculate" in command:
        try:
            expression = command.replace("calculate","").strip()
            expression = expression.replace("plus","+").replace("add","+")
            expression = expression.replace("minus","-").replace("times","*")
            expression = expression.replace("multiplied by","*").replace("into","*")
            expression = expression.replace("divided by","/").replace("power","**")

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

    # ---------- EXIT ----------
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
root.geometry("600x400")

title = tk.Label(root, text="Desktop Voice Automation", font=("Arial", 16))
title.pack()

start_button = tk.Button(root, text="Start Listening", command=start_assistant)
start_button.pack()

output_box = tk.Text(root, height=20)
output_box.pack()

root.mainloop()

