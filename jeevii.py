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

engine = pyttsx3.init()
typing_mode = False

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
        return ""

# ---------------- COMMANDS ----------------
def execute_command(command):
    global typing_mode

    # -------- GREETING --------
    if "hello assistant" in command:
        speak("Hello boss, how can I help you 😎")

    # -------- TYPING MODE --------
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
        webbrowser.open("https://www.google.com/search?q=" + query)

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")

    elif "play" in command:
        pywhatkit.playonyt(command.replace("play",""))

    elif "open calculator" in command:
        os.system("calc")

    elif "open notepad" in command:
        os.system("notepad")

    elif "open cmd" in command:
        os.system("start cmd")

    elif "open file explorer" in command:
        os.system("explorer")

    elif "open wordpad" in command:
        os.system("write")

    elif "open excel" in command:
        os.system("start excel")

    elif "open powerpoint" in command:
        os.system("start powerpnt")

    elif "open gmail" in command:
        webbrowser.open("https://mail.google.com")

    # -------- WHATSAPP --------
    elif "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")

    elif "send whatsapp message" in command:
        speak("Tell me number with country code")
        number = listen()

        speak("What message?")
        msg = listen()

        try:
            pywhatkit.sendwhatmsg_instantly(number, msg)
            speak("Message sent")
        except:
            speak("Failed to send")

    # -------- CAMERA --------
    elif "open camera" in command:
        os.system("start shell:AppsFolder\\Microsoft.WindowsCamera_8wekyb3d8bbwe!App")

    elif "take photo" in command:
        cam = cv2.VideoCapture(0)
        time.sleep(2)
        ret, frame = cam.read()
        if ret:
            cv2.imwrite("photo.png", frame)
            speak("Photo saved")
        cam.release()

    # -------- FILE SEARCH --------
    elif "open file" in command or "open folder" in command:
        speak("Tell name")
        name = listen()
        found = False

        for root_dir, dirs, files in os.walk("C:\\Users"):
            for file in files:
                if name in file.lower():
                    os.startfile(os.path.join(root_dir, file))
                    found = True
                    break

            for folder in dirs:
                if name in folder.lower():
                    os.startfile(os.path.join(root_dir, folder))
                    found = True
                    break

            if found:
                break

        if not found:
            speak("Not found")

    # -------- SCREENSHOT --------
    elif "screenshot" in command:
        img = pyautogui.screenshot()
        img.save("screenshot.png")
        speak("Screenshot taken")

    # -------- CALCULATOR --------
    elif any(word in command for word in ["calculate","what is","plus","minus","times","divided","into","x"]):
        try:
            exp = command.replace("what is","").replace("calculate","")
            exp = exp.replace("plus","+").replace("minus","-")
            exp = exp.replace("times","*").replace("x","*")
            exp = exp.replace("divided by","/")
            exp = exp.strip()

            if "sin" in exp:
                num = float(exp.replace("sin",""))
                result = math.sin(math.radians(num))
            elif "cos" in exp:
                num = float(exp.replace("cos",""))
                result = math.cos(math.radians(num))
            elif "tan" in exp:
                num = float(exp.replace("tan",""))
                result = math.tan(math.radians(num))
            else:
                result = eval(exp)

            speak("Answer is " + str(result))
        except:
            speak("Cannot calculate")

    # -------- FUN --------
    elif "joke" in command:
        speak("Why programmers hate sunlight? Because bugs love it 😄")

    elif "who are you" in command:
        speak("I am your smart assistant 😎")

    elif "motivate me" in command:
        speak("Don't stop until you are proud 💪")

    # -------- EXIT --------
    elif "exit" in command:
        speak("Goodbye boss")
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