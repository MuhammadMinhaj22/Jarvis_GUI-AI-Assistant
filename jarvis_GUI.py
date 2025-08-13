import os
import random
import datetime
import wikipedia
import webbrowser
import requests
from gtts import gTTS
from playsound import playsound
import time
import tkinter as tk
from tkinter import scrolledtext


user_name = "Minhaj"
music = {
    "zehra": "https://www.youtube.com/watch?v=-xSEVqi_jVk",
    "believer": "https://www.youtube.com/watch?v=7wtfhZwyrcc",
    "faded": "https://www.youtube.com/watch?v=60ItHLz5WEA"
}


def speak(text):
    try:
        chunks = [text[i:i+100] for i in range(0, len(text), 100)]
        for chunk in chunks:
            filename = f"voice_{random.randint(1, 100000)}.mp3"
            tts = gTTS(text=chunk, lang='en')
            tts.save(filename)
            playsound(filename)
            os.remove(filename)
            time.sleep(0.5)
    except Exception as e:
        output.insert(tk.END, f"\n[Error] {e}\n")


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        greeting = "Good Morning!"
    elif hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"
    speak(greeting + " I am Jarvis. Please type your command.")
    output.insert(tk.END, f"{greeting} I am Jarvis. Please type your command.\n")


def get_weather(city):
    try:
        api_key = "your_OpenWeather_api_key"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        res = requests.get(url).json()
        if res["cod"] == 200:
            temp = res["main"]["temp"]
            desc = res["weather"][0]["description"]
            return f"The temperature in {city} is {temp}°C with {desc}."
        else:
            return "City not found."
    except:
        return "Unable to fetch weather."


def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the computer catch a cold? Because it had too many bugs.",
        "Parallel lines have so much in common... it’s a shame they’ll never meet."
    ]
    joke = random.choice(jokes)
    speak(joke)
    output.insert(tk.END, f"{joke}\n")


def calculator(expr):
    try:
        result = eval(expr)
        speak(f"The result is {result}")
        output.insert(tk.END, f"Result: {result}\n")
    except:
        speak("Sorry, I couldn't calculate that.")
        output.insert(tk.END, "Sorry, I couldn't calculate that.\n")


def process_command():
    global user_name
    query = command_entry.get().lower()
    output.insert(tk.END, f"\n>>> {query}\n")
    command_entry.delete(0, tk.END)

    if "my name is" in query:
        user_name = query.replace("my name is", "").strip()
        speak(f"Nice to meet you, {user_name}!")

    elif "what is my name" in query:
        speak(f"Your name is {user_name}")

    elif "wikipedia" in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        try:
            result = wikipedia.summary(query, sentences=2)
            output.insert(tk.END, result + "\n")
            speak(result)
        except:
            speak("No result found.")

    elif "open youtube" in query:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")

    elif "open google" in query:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")

    elif "open linkedin" in query:
        webbrowser.open("https://www.linkedin.com")
        speak("Opening LinkedIn.")

    elif "open instagram" in query:
        webbrowser.open("https://www.instagram.com")
        speak("Opening Instagram.")

    elif "play" in query:
        song_name = query.replace("play", "").strip()
        if song_name in music:
            speak(f"Playing {song_name}")
            webbrowser.open(music[song_name])
        else:
            speak("Sorry, I couldn't find that song.")

    elif "search" in query:
        search = query.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={search}")
        speak(f"Searching Google for {search}")

    elif "time" in query:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {now}")
        output.insert(tk.END, f"Time: {now}\n")

    elif "date" in query:
        today = datetime.date.today().strftime("%B %d, %Y")
        speak(f"Today's date is {today}")
        output.insert(tk.END, f"Date: {today}\n")

    elif "weather in" in query:
        city = query.replace("weather in", "").strip()
        weather = get_weather(city)
        speak(weather)
        output.insert(tk.END, weather + "\n")

    elif "joke" in query:
        tell_joke()

    elif "calculate" in query:
        expr = query.replace("calculate", "").strip()
        calculator(expr)

    elif "exit" in query or "quit" in query or "bye" in query:
        speak("Goodbye! Have a nice day.")
        root.destroy()

    else:
        speak("Sorry, I didn't understand that.")
        output.insert(tk.END, "Sorry, I didn't understand that.\n")


root = tk.Tk()
root.title("JARVIS Assistant")
root.state("zoomed")  
root.config(bg="#1e1e1e")


heading = tk.Label(root, text="Welcome to JARVIS", font=("Arial", 20, "bold"), bg="#1e1e1e", fg="cyan")
heading.pack(pady=10)


output = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12), height=20, bg="#252526", fg="white")
output.pack(padx=10, pady=5, expand=True, fill=tk.BOTH)


command_entry = tk.Entry(root, font=("Arial", 14), bg="#333", fg="white", width=40)
command_entry.pack(pady=10)


submit_button = tk.Button(root, text="Submit", command=process_command, font=("Arial", 12), bg="cyan", fg="black")
submit_button.pack()


root.after(1000, wishMe)



root.mainloop()
