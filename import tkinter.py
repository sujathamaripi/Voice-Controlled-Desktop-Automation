import tkinter as tk
import pyttsx3
import speech_recognition as sr
import pywhatkit
import datetime
import os

# ---------------- TEXT TO SPEECH ---------------- #
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ---------------- LISTEN FUNCTION ---------------- #
def take_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        listener.adjust_for_ambient_noise(source)
        audio = listener.listen(source)

    try:
        command = listener.recognize_google(audio)
        command = command.lower()
        print("You said:", command)
        return command
    except:
        speak("Sorry, I did not understand.")
        return ""

# ---------------- MAIN COMMAND FUNCTION ---------------- #
def run_assistant():
    command = take_command()

    if "youtube" in command:
        speak("Opening YouTube")
        pywhatkit.playonyt("youtube")

    elif "google" in command:
        speak("Opening Google")
        os.system("start https://www.google.com")

    elif "chat gpt" in command or "chatgpt" in command:
        speak("Opening ChatGPT")
        os.system("start https://chat.openai.com")

    elif "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak("Current time is " + time)

    elif "shutdown" in command:
        speak("Shutting down system")
        os.system("shutdown /s /t 5")

    elif command == "":
        pass

    else:
        speak("Command not recognized")

# ---------------- GUI PART ---------------- #
root = tk.Tk()
root.title("Voice Controlled Desktop Automation")
root.geometry("500x400")

label = tk.Label(root, text="Voice Assistant Running...", font=("Arial", 16))
label.pack(pady=20)

button = tk.Button(root, text="Start Listening", font=("Arial", 14), command=run_assistant)
button.pack(pady=20)

root.mainloop()