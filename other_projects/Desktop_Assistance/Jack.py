import subprocess
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
from colorama import Fore
import webbrowser
import os
import smtp_mail

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# print(voices[0].id)
b = True
hour = datetime.datetime.now().hour


def take_command():
    # take mice input from user
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("Input:", query)

    except Exception as e:
        print(e)
        print("can you repeat please...")
        return "None"
    return query


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def intro_wish():
    speak("hello Boss")
    if 5 <= hour <= 12:
        speak("good morning")
    elif 12 < hour <= 18:
        speak("good afternoon !")
    elif 18 < hour <= 24:
        speak("Good evening !")


if __name__ == "__main__":
    intro_wish()

    while True:
        try:
            command = take_command().lower()
            if command.endswith("wikipedia"):
                result = wikipedia.summary(command[:-9], sentences=2)
                speak("Available Information on wikipedia")
                print("Available Information on wikipedia:")
                speak(result)
            elif "open youtube" in command:
                webbrowser.open("https://www.youtube.com/")
            elif "hello jack" in command:
                speak("hello boss")
            elif "open email" in command or "open mail" in command:
                webbrowser.open("https://mail.google.com/mail/u/0")
            elif "open google" in command:
                webbrowser.open("https://www.google.com/")
            elif "play music" in command:
                music_dir = "D:/DCIM/"
                songs = os.listdir(music_dir)
                print(songs)
                os.startfile(os.path.join(music_dir, songs[14]))
            elif "what is time" in command:
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f'current time is {current_time}')
                print(f'current time is {current_time}')
            elif "open vs code" in command or "open visual studio code" in command:
                file_path = "C:\\Users\\AFTAB SAMA\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                os.startfile(file_path)
            elif "open gallery" in command or "open photos" in command:
                subprocess.run('start ms-photos:', shell=True)
            elif "send mail" in command or "send email" in command:
                print(Fore.GREEN, "Enter email details...")
                print("if you want to type email say:text")
                print("if you want to speak email say:voice")
                send_to = 'test@gmail.com'
                sub = 'Sub'
                a1 = 'voice'
                while True:
                    try:
                        a1 = take_command()
                        if "text" in a1:
                            a1 = "text"
                            break
                        elif "voice" in a1:
                            a1 = "voice"
                            break
                        else:
                            print("sorry i didn't understand can you repeat!")
                    except KeyboardInterrupt as e1:
                        print("KeyboardInterrupt Exiting...")
                        break

                if a1 == "text":
                    send_to = input("send email to=")
                    sub = input("Subject=")
                    mail_content = input("email body=")
                    with open("D:/samples/mail_content-smtp-mail-python.txt", 'w') as f:
                        f.write(mail_content)
                    smtp_mail.send_email(send_to, sub)
                elif a1 == "voice":
                    while True:
                        try:
                            print("send email to=")
                            send_to = take_command().lower()
                            send_to = send_to.replace("at the rate", "@")
                            send_to = send_to.replace(" ", "")
                            print(f'send to:{send_to}')
                            print("Done ?")
                            s1 = take_command()          # say done or yes to move to next one
                            if "done" in s1 or "yes" in s1:
                                break
                        except KeyboardInterrupt as e1:
                            print("KeyboardInterrupt Exiting...")
                            break
                    while True:
                        try:
                            print("Subject =")
                            sub = take_command()
                            print(f'Subject:{sub}')
                            print("Done ?")
                            s1 = take_command()           # say done or yes to move to next one
                            if "done" in s1 or "yes" in s1:
                                break
                        except KeyboardInterrupt as e1:
                            print("KeyboardInterrupt Exiting...")
                            break
                    while True:
                        try:
                            print("Body =")
                            mail_content = take_command()
                            print(f'Body:{mail_content}')
                            print("Done ?")
                            s1 = take_command()           # say done to move to next one
                            if "done" in s1:
                                with open("D:/samples/mail_content-smtp-mail-python.txt", 'w') as f:
                                    f.write(mail_content)
                                break
                        except KeyboardInterrupt as e1:
                            print("KeyboardInterrupt Exiting...")
                            break
                    smtp_mail.send_email(send_to, sub)
            pass
        except KeyboardInterrupt as e1:
            print("KeyboardInterrupt Exiting...")
            break
