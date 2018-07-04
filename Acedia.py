import pyttsx3
import speech_recognition as sr
import webbrowser
from PyDictionary import PyDictionary
import re
import urllib.request
import urllib.parse
import imaplib
import email
import time
from bs4 import BeautifulSoup
import requests
from googlesearch import search
import os
import threading
from multiprocessing import Process

def getTextFromURL(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return text


def onStart(name):
   print('starting', name)


def onWord(name, location, length):
   print('word', name, location, length)


def onEnd(name, completed):
   print('finishing', name, completed)


def lungime_text(mesaj):
    nr = 0
    for i in mesaj.split():
        nr = nr + 1
    return nr


url = "https://www.google.ro/#q="
url2 = "https://www.youtube.com/results?search_query="
url3 = "https://www.youtube.com/watch?v="
google_api = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
dictionary = PyDictionary()

def close_web():
    browserExe = "chrome.exe"
    os.system("taskkill /f /im " + browserExe)


def close_loop():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source, phrase_time_limit=5)
        message = r.recognize_google(audio)
        if "close" in message:
            close_web()


def e_mail():

    mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    mail.login('raresarv1@gmail.com', 'rgthb4tpj')


    print(mail.list())
    print(mail.select('INBOX'))

    result, data = mail.uid('search', None, "(UNSEEN)")
    i = len(data[0].split())
    for x in range(i):
        latest_email_uid = data[0].split()[x]

        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')

        raw_email = email_data[0][1]

        raw_email_string = raw_email.decode('utf-8')

        email_message = email.message_from_string(raw_email_string)

        i = 0
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":  # ignore attachments/html
                body = part.get_payload(decode=True)
                i = i + 1
                engine = pyttsx3.init()
                print("Unseen email %s" % i)
                engine.say("Unseen email %s" % i)
                print("from " + email_message['From'])
                engine.say("from " + email_message['From'])
                if email_message['Subject'] == '':
                    print("with subject blank")
                    engine.say("with subject blank")
                else:
                    print("with subject " + email_message['Subject'])
                    engine.say("with subject " + email_message['Subject'])
                time.sleep(1)
                engine.say(body.decode('utf-8'))
                print(body.decode('utf-8'))
                engine.runAndWait()
    mail.logout()


def youtube_helper():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        print("Ce doriti sa cautati?")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source, phrase_time_limit=5)

        query_string = urllib.parse.urlencode({"search_query": audio})
        html_content = urllib.request.urlopen(url2 + r.recognize_google(audio))
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        print(search_results)
    try:
        webbrowser.get(google_api).open_new(url3 + search_results[0])
    except:
        pass
    return 0


def search_google():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        engine = pyttsx3.init()
        mesaj_question = "What do you wish to search?"
        engine.say(mesaj_question)
        print(mesaj_question)
        engine.runAndWait()
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source, phrase_time_limit=5)
        query = r.recognize_google(audio)
        web_query = []
        for j in search(query, tld="co.in", num=10, stop=1, pause=2):
            web_query.append(j)
        #print(web_query)
    try:
        #webbrowser.get(google_api).open_new(url + r.recognize_google(audio))
        engine = pyttsx3.init()
        print(getTextFromURL(web_query[0]))
        engine.say(getTextFromURL(web_query[0]))
        engine.runAndWait()
    except:
        pass


def cauta_dex():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        engine = pyttsx3.init()
        mesaj_question = "What do you wish to search?"
        engine.say(mesaj_question)
        print(mesaj_question)
        engine.runAndWait()
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source, phrase_time_limit=5)
        message = r.recognize_google(audio)
        print("You: " + message)
    if lungime_text(message) == 1:
        try:
            bot_response = dictionary.meaning(message)
            print(bot_response)
            if not bot_response:
                query = r.recognize_google(audio)
                web_query = []
                for j in search(query, tld="co.in", num=10, stop=1, pause=2):
                    web_query.append(j)
                # print(web_query)
                webbrowser.get(google_api).open_new(url + r.recognize_google(audio))
                engine = pyttsx3.init()
                print(getTextFromURL(web_query[0]))
                engine.say(getTextFromURL(web_query[0]))
                engine.runAndWait()
            else:
                engine = pyttsx3.init()
                engine.say(bot_response)
                print(bot_response)
                engine.runAndWait()
        except (IndexError, ValueError):
            query = r.recognize_google(audio)
            web_query = []
            for j in search(query, tld="co.in", num=10, stop=1, pause=2):
                web_query.append(j)
            # print(web_query)
            webbrowser.get(google_api).open_new(url + r.recognize_google(audio))
            engine = pyttsx3.init()
            print(getTextFromURL(web_query[0]))
            engine.say(getTextFromURL(web_query[0]))
            engine.runAndWait()
    elif lungime_text(message) > 1:
        try:
            query = r.recognize_google(audio)
            web_query = []
            for j in search(query, tld="co.in", num=10, stop=1, pause=2):
                web_query.append(j)
            # print(web_query)
            webbrowser.get(google_api).open_new(url + r.recognize_google(audio))
            engine = pyttsx3.init()
            print(getTextFromURL(web_query[0]))
            engine.say(getTextFromURL(web_query[0]))
            engine.runAndWait()
        except:
            pass


def menu_menu():
    engine = pyttsx3.init()
    mesaj_open1 = "Hello, welcome to the menu! "
    engine.say(mesaj_open1)
    print(mesaj_open1)
    mesaj_open1 = "Now i will read you all the available commands! "
    engine.say(mesaj_open1)
    print(mesaj_open1)
    mesaj_open1 = "If you want to access Youtube, say youtube ! "
    engine.say(mesaj_open1)
    print(mesaj_open1)
    mesaj_open1 = "If you want to search for a web-page, say search ! "
    engine.say(mesaj_open1)
    print(mesaj_open1)
    mesaj_open1 = "If you want to search for a word in dictionary, say dex ! "
    engine.say(mesaj_open1)
    print(mesaj_open1)
    mesaj_open1 = "If you want me to read your emails, say email ! "
    engine.say(mesaj_open1)
    print(mesaj_open1)
    mesaj_open1 = "If you want me to close your webbrowser, say close ! "
    engine.say(mesaj_open1)
    print(mesaj_open1)
    mesaj_open1 = "If you want to close me, say quit ! "
    engine.say(mesaj_open1)
    print(mesaj_open1)
    engine.runAndWait()


def main():
    engine = pyttsx3.init()
    mesaj_open1 = "Welcome to Acedia! "
    engine.say(mesaj_open1)
    print(mesaj_open1)
    mesaj_open2 = "This program will help you work with online environment! "
    engine.say(mesaj_open2)
    print(mesaj_open2)
    mesaj_open3 = "If you wish to seek further help, simply say menu! "
    engine.say(mesaj_open3)
    print(mesaj_open3)

    engine.runAndWait()
    while True:

        r = sr.Recognizer()
        with sr.Microphone(device_index=0) as source:
            engine = pyttsx3.init()
            mesaj_open = "Say something!"
            print("Say something!")
            engine.say(mesaj_open)
            engine.runAndWait()
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, phrase_time_limit=5)

        try:
            message = r.recognize_google(audio)
            print("You: " + message)
            if "quit" in message:
                exit()
            elif "menu" in message:
                menu_menu()
            elif "YouTube" in message:
                youtube_helper()
            elif "search" in message:
                search_google()
            elif "Dex" in message:
                cauta_dex()
            elif "email" in message:
                e_mail()
            elif "close" in message:
                close_web()
            else:
                engine = pyttsx3.init()
                engine.runAndWait()

        except sr.UnknownValueError as e:
            engine = pyttsx3.init()
            mesaj_eroare = "Please, repeat words!"
            engine.say(mesaj_eroare)
            print(mesaj_eroare)
            engine.runAndWait()
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

main()