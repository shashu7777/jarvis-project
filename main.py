import pyttsx3
import speech_recognition as sr
import webbrowser
import subprocess
from openai import OpenAI
from config import apikey, news_api_key
import os
import requests

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)

chatst = " "
news_audio = ""


def news(query):
    # print("ggggg")
    country_code = 'in'
    result = ""

    url = 'https://newsapi.org/v2/top-headlines'
    params = {'q': query, 'apiKey': news_api_key, 'pageSize': 1,
              'country': country_code}  # Example query for news related to Python

    response = requests.get(url, params=params)

    if response.status_code == 200:
        # print("wwwww")
        news_data = response.json()
        articles = news_data['articles']
        for article in articles:
            result += f"Title: {article['title']}\n Description: {article['description']}\n "

            ''' print(f"Title: {article['title']}")
            print(f"Description: {article['description']}")
            print("\n")'''
        speak(result)
    else:
        print(f"Error......")


def chat(query):
    global chatst
    client = OpenAI(api_key=apikey)
    chatst += f"Shashank :{query}\n Jarvis :"
    response = client.completions.create(
        model="text-davinci-003",
        prompt=chatst,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # print(response)

    speak(response.choices[0].text)
    chatst += f"{response.choices[0].text}\n"
    return response.choices[0].text

    # if not os.path.exists("openai"):
    #   os.mkdir("openai")

    # with open(f"openai/{''.join(prompt.split('intelligence')[1:])}.txt", "w") as f:
    #   f.write(text)


def ai(prompt):
    client = OpenAI(api_key=apikey)
    text = f"OpenAi response for Prompt:{prompt} \n ************************\n\n"
    # openai.api_key = apikey

    response = client.completions.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # print(response)

    print("hiiii")
    # print(response["choices"][0]["text"])
    # text += response["choices"][0]["text"]
    text += response.choices[0].text
    print("biiii")

    if not os.path.exists("openai"):
        os.mkdir("openai")

    with open(f"openai/{''.join(prompt.split('intelligence')[1:])}.txt", "w") as f:
        f.write(text)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("jarvis : Listening...")  # Prompt the user
        r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = r.listen(source)

    try:
       # print("Recognizing...")
        query = r.recognize_google(audio, language='en-US')  # Adjust the language as needed
        print("User said:", query)
        return query
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
    except sr.RequestError as e:
        print(f"Sorry, there was an error with the request: {e}")
    return ""


if __name__ == '__main__':
    while True:
        print("\n")
        print("Tell me something...")
        audio = takeCommand()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"], ["open chrome"]]
        for site in sites:

            if f"open {site[0]}".lower() in audio.lower():
                speak(f"opening {site[0]} sir...")
                webbrowser.open(site[1])
            elif site[0].lower() in audio.lower():
                speak(f"opening chrome sir..")
                subprocess.Popen(["C:\Program Files\Google\Chrome\Application\chrome.exe"])


        if "Using artificial intelligence".lower() in audio.lower():
            ai(prompt=audio)

        elif "jarvis quit".lower() in audio.lower():
            speak("ok have a good day")
            exit()

        elif "reset chat ".lower() in audio.lower():
            chatst = " "

        if "news".lower() in audio.lower():
            speak("which news do you want..")
            news_audio = takeCommand()
            news(news_audio)

        else:
            print("jarvis: chatting......")
            chat(audio)

        # if audio:
        # speak(audio)
