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
import cv2
import random

engine = pyttsx3.init()
typing_mode = False

# -------- CONTACTS --------
contacts = {
    "andhagathey": "+918500136444",
    "zeba": "+916300176045",
    "anusha": "+919177497355",
    "sama": "+919553696420",
    
    "Navya": "+918985848512",
    "Archini": "+917981685069",
    "ROSHNI": "+916300873805",
    "Sailaja": "+918019306202",
    "divya Cse":"+91810678787",

    "Charvi":"+919346125321",
    "Gayathri..":"+916301048408",
    "Indhu": "+919912648090",
    "Kaaavvv": "+916301427853",
    "Laavuu": "+919381335466",

}

# ---------------- SPEAK ----------------
def speak(text):
    output_box.insert(tk.END, "Assistant: " + text + "\n")
    engine.say(text)
    engine.runAndWait()

# ---------------- LISTEN ----------------
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

# ---------------- COMMANDS ----------------
def execute_command(command):
    global typing_mode

    # -------- GREETING --------
    if "hello assistant" in command or "hi assistant" in command:
        speak("Hello boss how can i help you")

    # -------- TYPING --------
    elif "start typing" in command:
        typing_mode = True
        speak("Typing mode activated")

    elif "stop typing" in command:
        typing_mode = False
        speak("Typing stopped")

    # -------- OPEN APPS --------
    elif "open chrome" in command:
        os.system("start chrome")

    elif "open google" in command:
        webbrowser.open("https://www.google.com")

    elif "search" in command:
        query = command.replace("search","")
        speak("Searching " + query)
        webbrowser.open("https://www.google.com/search?q=" + query)

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")

    elif "play" in command:
        pywhatkit.playonyt(command.replace("play",""))

    elif "tutorial" in command:
        topic = command.replace("tutorial","")
        pywhatkit.playonyt(topic + " tutorial")

    elif "open notepad" in command:
        os.system("notepad")

    elif "open calculator" in command:
        os.system("calc")

    elif "open cmd" in command:
        os.system("start cmd")

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

    elif "open wordpad" in command:
        os.system("write")

    elif "open gmail" in command:
        webbrowser.open("https://mail.google.com")

    elif "open chatgpt" in command:
        webbrowser.open("https://chat.openai.com")

    # -------- WHATSAPP (UPDATED AUTO SEND) --------
    elif "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")

    elif "send message to" in command:
        try:
            words = command.split()
            name = words[words.index("to") + 1].lower()
            message = " ".join(words[words.index(name) + 1:])

            if name in contacts:
                number = contacts[name]
                speak(f"Sending message to {name}")

                now = datetime.datetime.now()
                hour = now.hour
                minute = now.minute + 1

                pywhatkit.sendwhatmsg(number, message, hour, minute)
            else:
                speak("Contact not found")

        except Exception as e:
            print(e)
            speak("Error sending message")

    
    # -------- CAMERA --------
    elif "open camera" in command:
        os.system("start microsoft.windows.camera:")

    elif "take photo" in command:
        cam = cv2.VideoCapture(0)
        time.sleep(2)
        ret, frame = cam.read()

        if ret:
            cv2.imwrite("photo.png", frame)
            speak("Photo saved 📸")
        else:
            speak("Camera failed 😢")

        cam.release()

    # -------- SCREENSHOT --------
    elif "screenshot" in command:
        img = pyautogui.screenshot()
        img.save("screenshot.png")
        speak("Screenshot taken 📸")

    # -------- SYSTEM --------
    elif "shutdown" in command:
        speak("Shutting down system 💀")
        os.system("shutdown /s /t 5")

    elif "restart" in command:
        speak("Restarting system 🔄")
        os.system("shutdown /r /t 5")

    elif "sleep" in command:
        speak("Going to sleep 😴")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    elif "lock" in command:
        speak("Locking system 🔒")
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

    elif "brightness decrease" in command:
        sbc.set_brightness(30)

    # -------- WEATHER & TIME --------
    elif "weather" in command:
        city = "Hyderabad"
        weather = requests.get(f"https://wttr.in/{city}?format=3").text
        speak(weather)

    elif "time" in command:
        speak("Time is " + datetime.datetime.now().strftime("%H:%M"))

    # -------- CALCULATOR --------
    elif any(word in command for word in ["calculate","what is","plus","minus","times","divided","into","x"]):
        try:
            exp = command.replace("what is","").replace("calculate","")
            exp = exp.replace("plus","+").replace("minus","-")
            exp = exp.replace("times","*").replace("x","*")
            exp = exp.replace("divided by","/")
            exp = exp.strip()

            if "sin" in exp:
                result = math.sin(math.radians(float(exp.replace("sin",""))))
            elif "cos" in exp:
                result = math.cos(math.radians(float(exp.replace("cos",""))))
            elif "tan" in exp:
                result = math.tan(math.radians(float(exp.replace("tan",""))))
            else:
                result = eval(exp)

            speak("Answer is " + str(result))
        except:
            speak("Cannot calculate 😵")

    # -------- CLOSE APPS --------
    elif "close notepad" in command:
        os.system("taskkill /f /im notepad.exe")

    elif "close chrome" in command or "close youtube" in command:
        os.system("taskkill /f /im chrome.exe")

    elif "close calculator" in command:
        os.system("taskkill /f /im CalculatorApp.exe")

    elif "close cmd" in command:
        os.system("taskkill /f /im cmd.exe")

    elif "close excel" in command:
        os.system("taskkill /f /im excel.exe")

    elif "close powerpoint" in command:
        os.system("taskkill /f /im powerpnt.exe")

    elif "close file explorer" in command:
        os.system("taskkill /f /im explorer.exe")

    # -------- FUN --------
    elif "tell me a joke" in command or "joke" in command:
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs 😄",
            "Why did Python go to school? To improve its class 🐍",
            "Debugging is like being a detective 😂"
        ]
        speak(random.choice(jokes))

    elif "who made you" in command:
        speak("I was created by a brilliant student 😎")

    elif "are you smart" in command:
        speak("Of course 😏")

    elif "who are you" in command:
        speak("I am your desktop assistant 🤖")

    elif "make me laugh" in command:
        speak("Haha 😂")

    elif "do you like me" in command:
        speak("Of course boss ❤️")

    elif "motivate me" in command:
        speak("Keep working hard 💪🔥")

    # -------- EXIT --------
    elif "exit" in command:
        speak("Goodbye boss 👋")
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
root.title("Desktop Voice Assistant")
root.geometry("600x400")

tk.Label(root, text="Desktop Voice Automation", font=("Arial",16)).pack()
tk.Button(root, text="Start Listening", command=start_assistant).pack()

output_box = tk.Text(root, height=20)
output_box.pack()

root.mainloop()