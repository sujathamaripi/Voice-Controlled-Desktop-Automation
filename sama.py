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
import subprocess

engine = pyttsx3.init()
typing_mode = False
active_window = None

# ---------------- SPEAK FUNCTION ----------------
def speak(text):
    output_box.insert(tk.END, "Assistant: " + text + "\n")
    output_box.see(tk.END)
    engine.say(text)
    engine.runAndWait()

# ---------------- LISTEN FUNCTION ----------------
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        output_box.insert(tk.END, "Listening...\n")
        output_box.see(tk.END)
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        output_box.insert(tk.END, "You (Voice): " + command + "\n")
        output_box.see(tk.END)
        return command.lower()
    except:
        speak("Sorry, I didn't understand")
        return ""

# ---------------- TEXT INPUT ----------------
def take_text_input():
    command = entry_box.get()
    entry_box.delete(0, tk.END)
    if command:
        output_box.insert(tk.END, "You (Text): " + command + "\n")
        execute_command(command.lower())

# ---------------- COMMAND EXECUTION ----------------
def execute_command(command):
    global typing_mode, active_window

    # ---------- VOICE TYPING ----------
    if typing_mode:
        pyautogui.write(command + " ")
        return

    # ---------- OPEN ANY APPLICATION ----------
    if "open" in command:
        app = command.replace("open", "").strip()
        speak(f"Opening {app}")
        try:
            subprocess.Popen(app)
        except:
            try:
                os.system(f"start {app}")
            except:
                speak("Application not found")

    # ---------- VOICE TYPING IN NOTEPAD ----------
    elif "voice typing" in command or "start typing" in command:
        speak("Opening Notepad for voice typing")
        os.system("notepad")
        time.sleep(2)
        pyautogui.hotkey("ctrl", "n")
        typing_mode = True
        active_window = "notepad"
        speak("You can start speaking. I will type.")

    elif "stop typing" in command:
        typing_mode = False
        speak("Voice typing stopped")

    # ---------- CLOSE ANY APPLICATION ----------
    elif "close" in command:
        app = command.replace("close", "").strip()
        speak(f"Closing {app}")
        os.system(f"taskkill /f /im {app}.exe")

    # ================= YOUTUBE DESKTOP CONTROL =================
    elif "open youtube" in command:
        speak("Opening YouTube")
        try:
            os.system("start youtube")  # if app installed
        except:
            webbrowser.open("https://www.youtube.com")

    elif "pause video" in command or "play video" in command:
        pyautogui.press("space")

    elif "next video" in command:
        pyautogui.hotkey("shift", "n")

    elif "previous video" in command:
        pyautogui.hotkey("shift", "p")

    elif "fullscreen youtube" in command:
        pyautogui.press("f")

    # ================= WHATSAPP DESKTOP CONTROL =================
    elif "open whatsapp" in command:
        speak("Opening WhatsApp")
        try:
            os.system("start whatsapp")
        except:
            speak("WhatsApp not found")

    elif "send message" in command:
        speak("Opening WhatsApp")
        os.system("start whatsapp")
        time.sleep(5)

        speak("Tell me the contact name")
        name = listen()

        speak(f"Searching for {name}")
        pyautogui.hotkey("ctrl", "f")
        time.sleep(1)
        pyautogui.write(name)
        time.sleep(2)
        pyautogui.press("enter")

        speak("What is the message")
        msg = listen()

        pyautogui.write(msg)
        pyautogui.press("enter")
        speak("Message sent")

    # ---------- YOUTUBE (OLD FEATURE KEPT) ----------
    elif "play" in command:
        song = command.replace("play", "")
        speak("Playing " + song)
        pywhatkit.playonyt(song)

    # ---------- WEATHER ----------
    elif "weather" in command:
        speak("Tell me the city name")
        city = listen()
        if city:
            try:
                url = f"https://wttr.in/{city}?format=3"
                weather = requests.get(url).text
                speak(weather)
            except:
                speak("Unable to fetch weather")

    # ---------- SEARCH ----------
    elif "search" in command:
        query = command.replace("search", "")
        speak("Searching " + query)
        pywhatkit.search(query)

    elif "wikipedia" in command:
        query = command.replace("wikipedia", "")
        speak("Searching Wikipedia for " + query)
        webbrowser.open("https://en.wikipedia.org/wiki/" + query)

    # ---------- SCREENSHOT ----------
    elif "screenshot" in command:
        img = pyautogui.screenshot()
        img.save("screenshot.png")
        speak("Screenshot taken")

    # ---------- SYSTEM ----------
    elif "shutdown" in command:
        speak("Shutting down system")
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

    # ---------- TIME ----------
    elif "time" in command:
        time_now = datetime.datetime.now().strftime("%H:%M")
        speak("The time is " + time_now)

    # ---------- FUN ----------
    elif "joke" in command:
        speak("Why do programmers hate nature? Too many bugs.")

    elif "who are you" in command:
        speak("I am your advanced desktop voice assistant.")

    elif "exit" in command:
        speak("Goodbye")
        root.quit()

# ---------------- ASSISTANT LOOP ----------------
def assistant_loop():
    while True:
        command = listen()
        if command:
            execute_command(command)

# ---------------- START ASSISTANT ----------------
def start_assistant():
    speak("Assistant started. Say your command.")
    threading.Thread(target=assistant_loop).start()

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Advanced Voice Assistant")
root.geometry("650x500")

title = tk.Label(root, text="Voice + Text Desktop Assistant", font=("Arial", 16))
title.pack()

start_button = tk.Button(root, text="Start Voice Assistant", command=start_assistant)
start_button.pack()

entry_box = tk.Entry(root, width=50)
entry_box.pack()

send_button = tk.Button(root, text="Send Text Command", command=take_text_input)
send_button.pack()

output_box = tk.Text(root, height=20)
output_box.pack()

root.mainloop()  