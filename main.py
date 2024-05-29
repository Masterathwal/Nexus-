import speech_recognition as sr
import win32com.client
import webbrowser
import pywhatkit
import pyautogui
import os
import datetime
import requests
import streamlit as st
from streamlit_chat import message
from streamlit_lottie import st_lottie
import itertools
import wolframalpha
from bardapi import Bard

os.environ["_BARD_API_KEY"] = "XQg-gkLZvRlAhRMJtYGexOKX9caTb7p2AwINXnMUNJLTxpsHcxG53LIEf8NydU7lEz2q6w."
client = wolframalpha.Client('LRWXK2-Y7YLTJRWT6')

counter = itertools.count()

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()

lottie_coding=load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_ok9cq9zj.json")
def wishMe():

    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speaknex("Good Morning!")

    elif hour>=12 and hour<17:
        speaknex("Good Afternoon!")

    else:
        speaknex("Good Evening!")

def speaknex(sampletext, max_length=200):

    if len(sampletext) <= max_length:
        speaker = win32com.client.Dispatch("SAPI.Spvoice")
        speaker.Speak(sampletext)
    else:
        speaker = win32com.client.Dispatch("SAPI.Spvoice")
        speaker.Speak(sampletext[:max_length])
        speaker.Speak("And you can read rest of the Information")
def commandnex():

    r = sr.Recognizer()

    with sr.Microphone(device_index=2) as source:

        r.pause_threshold = 0.6
        audio = r.listen(source)

        try:
            query = r.recognize_google(audio, language="en-in")
            return query

        except Exception as e:
            speaknex("Can you please Speak Again...")

def front(para):

    if 'generate' not in st.session_state:
        st.session_state['generate'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    if text:
        st.session_state.generate.append(para)
        st.session_state.past.append(text)

    unique_key = f"{next(counter)}"
    message(text, is_user=True, key=unique_key + '_user')
    message(para, key=unique_key)

    speaknex(para)

def decrease_volume():
    for _ in range(5):
        pyautogui.press("volumedown")
    front("Volume decreased")

def increase_volume():
    for _ in range(5):
        pyautogui.press("volumeup")
    front("Volume increased")

if _name_ == "_main_":

    st_lottie(lottie_coding,height=300,key="coding")
    st.title("Nexus A.I Voice Assistant")
    wishMe()
    greeting = "Hello I am Nexus"
    st.subheader(greeting)
    speaknex(greeting)

    while True:
        print("Listening...")
        text = commandnex()
        print("Understanding...")

        if not text:
            continue

        sites=[["youtube","https://youtube.com"],["wikipedia","https://wikipedia.com"],["Instagram","https://instagram.com"],["Twitter","https://twitter.com"],["Google","https://google.com"]]

        webcom = False

        for site in sites:
            if f"Open {site[0]}".lower() in text.lower():
                front(f"Opening {site[0]}")
                webbrowser.open(site[1])
                webcom = True

        if webcom:
            continue

        elif "play".lower() in text.lower():
            song = text.replace('play', '')
            front('playing' + song + ' On YouTube')
            pywhatkit.playonyt(song)

        elif "increase volume".lower() in text.lower():
            increase_volume()

        elif "decrease volume".lower() in text.lower():
            decrease_volume()

        elif "the time".lower() in text.lower():
            timenowhour = datetime.datetime.now().strftime("%H")
            timenowmin = datetime.datetime.now().strftime("%M")
            front(f"The time is {timenowhour} Hours {timenowmin} Minutes")

        else:
            url = f"https://api.duckduckgo.com/?q={text}&format=json"
            response = requests.get(url)

            data = response.json()
            abstract = data.get('Abstract')

            if abstract:
                front(abstract)

            else:
                try:
                    res = client.query(text)
                    output = next(res.results).text
                    front(output)

                except StopIteration or Exception as e:
                    answer = Bard().get_answer(str(text))['content']
                    front(answer)