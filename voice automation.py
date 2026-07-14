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

    # OPEN APPLICATIONS
    if "open chrome" in command:
        os.system("start chrome")

    elif "open notepad" in command:
        os.system("notepad")

    elif "open excel" in command:
        os.system("start excel")

    elif "open word" in command:
        os.system("start winword")

    elif "open powerpoint" in command:
        os.system("start powerpnt")

    elif "open vs code" in command:
        os.system("code")

    # YOUTUBE SEARCH
    elif "search youtube" in command:
        speak("What should I search?")
        query = take_command()
        pywhatkit.playonyt(query)

    # WHATSAPP MESSAGE
    elif "send whatsapp message" in command:
        speak("Tell the message")
        msg = take_command()
        pywhatkit.sendwhatmsg_instantly("+91XXXXXXXXXX", msg)

    # SEND EMAIL
    elif "send email" in command:
        try:
            speak("What is the message?")
            content = take_command()

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("your_email@gmail.com", "your_password")
            server.sendmail("your_email@gmail.com",
                            "receiver@gmail.com", content)
            server.close()
            speak("Email sent successfully")
        except:
            speak("Error sending email")

    # READ NEWS
    elif "news" in command:
        url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=YOUR_API_KEY"
        news = requests.get(url).json()
        for article in news["articles"][:5]:
            speak(article["title"])

    # WEATHER
    elif "weather" in command:
        speak("Tell city name")
        city = take_command()
        api_key = "YOUR_API_KEY"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        data = requests.get(url).json()
        temp = data["main"]["temp"]
        speak(f"Temperature is {temp} kelvin")

    # SCREENSHOT
    elif "screenshot" in command:
        img = pyautogui.screenshot()
        img.save("screenshot.png")
        speak("Screenshot taken")

    # VOLUME CONTROL
    elif "increase volume" in command:
        pyautogui.press("volumeup")

    elif "decrease volume" in command:
        pyautogui.press("volumedown")

    elif "mute volume" in command:
        pyautogui.press("volumemute")

    # SYSTEM CONTROL
    elif "shutdown" in command:
        os.system("shutdown /s /t 5")

    elif "restart" in command:
        os.system("shutdown /r /t 5")

    elif "sleep" in command:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    elif "lock system" in command:
        os.system("rundll32.exe user32.dll,LockWorkStation")

    # OPEN GOOGLE MEET
    elif "open meet" in command:
        webbrowser.open("https://meet.google.com")

    # SEARCH FILE
    elif "search file" in command:
        speak("Tell file name")
        filename = take_command()
        for root, dirs, files in os.walk("C:\\"):
            for file in files:
                if filename in file:
                    speak("File found")
                    os.startfile(os.path.join(root, file))
                    break

    # EXIT
    elif "exit" in command:
        speak("Goodbye")
        break