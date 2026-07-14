import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import pywhatkit
import wikipedia
import requests
import datetime
import pyautogui
import smtplib
import psutil

engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print("You said:", command)
    except:
        return ""
    return command.lower()

# ========== MAIN PROGRAM ==========
speak("Desktop Voice Assistant Started")

while True:
    command = take_command()
