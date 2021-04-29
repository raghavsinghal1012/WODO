import pyttsx3 
import speech_recognition as sr 
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import requests
import numpy as np

weather_key = os.environ['weather_key']
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def weather():
    speak("Please tell me the city name")
    city_name = takeCommand()
    url = "https://api.openweathermap.org/data/2.5/weather?q="+city_name+"&appid="+weather_key
    read_url = requests.get(url)
    NewsDocument = read_url.json()
    Country = NewsDocument['sys']['country']
    Description = NewsDocument['weather'][0]['description']
    Min_Temp = "{:.2f}".format(NewsDocument['main']['temp_min'] - 273.15)
    Max_Temp = "{:.2f}".format(NewsDocument['main']['temp_max'] - 273.15)
    Humidity = NewsDocument['main']['humidity']
    print(f"Country : India")
    print(f"Description: {Description}")
    print(f"Minimum Temperature is : {Min_Temp}°C")
    print(f"Maximum Temperature is : {Max_Temp}°C")
    print(f"Humidity is : {Humidity}%")
    speak(f"Country : India")
    speak(f"Description: {Description}")
    speak(f"Minimum Temperature is : {Min_Temp} degree Celcius")
    speak(f"Maximum Temperature is : {Max_Temp} degree Celcius")
    speak(f"Humidity is : {Humidity} percent")
    
   

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")  

    else:
        speak("Good Evening!")  

    speak("I am woodoo Sir. Please tell me how may I help you")      

def takeCommand():
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query


def sendEmail(to,content):
    my_email=os.environ['my_email']
    my_pass=os.environ['my_pass']
    server =smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(my_email , my_pass)
    server.sendmail(my_email, to, content)
    server.close()
def verification():
    my_email=os.environ['my_email']
    my_pass=os.environ['my_pass']
    flag = 1
    while(flag == 1):
        a = np.random.randint(100000,999999)
        otp="OTP is "+str(a)
        server =smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(my_email , my_pass)
        server.sendmail(my_email,my_email,otp)
        speak("please proceed to otp verification")
        print("speak your OTP that you have recieved on your E-mail ID:")
        speak("speak your OTP that you have recieved on your E-mail ID:")
        b=takeCommand()
        b=b.replace(" ","")
        b=int(b)
        print(b)
        if (b == a):
            print("OTP verfied.\n Now you can send an email.\n Please speak what should I send")
            speak("OTP verfied")
            speak("Now you can send an email.")
            speak("Please speak what should I send")
            server.close()
            flag=0
        else:
            print("Wrong OTP please try again")
            print("We have resent the new OTP")
    

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
            break

        elif 'open youtube' in query:
            speak("what do you want to search")
            s=takeCommand()
            webbrowser.open("https://www.youtube.com/results?search_query="+s)
            break

        elif 'open google' in query:
            speak("what do you want to search")
            s2=takeCommand()
            s2=s2.replace(" ","+")
            webbrowser.open("https://www.google.com/search?q="+s2+"&rlz=1C1CHBF_enIN949IN949&oq="+s2+"&aqs=chrome.0.69i59j0l3j0i131i433i457j0i20i263i395j0i395i433l4.1917j1j9&sourceid=chrome&ie=UTF-8")
            break
        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")  
            break
        elif 'weather' in query:
            weather()
            break
        elif 'play music' in query:
            speak("what do you want to listen")
            s1=takeCommand()
            s1=s1.replace(" ","%20")
            webbrowser.open("https://music.amazon.in/search/"+s1+"?filter=IsLibrary%7Cfalse&sc=none")
            break
            

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            print(f"Sir, the time is {strTime}")
            speak(f"Sir, the time is {strTime}")
            break
        
        elif 'send an email' in query:
            try:
                verification()
                to ="vermasumit923@gmail.com"
                content = takeCommand()
                sendEmail(to,content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send this email, please try again")    
        elif 'exit' in query:
            break
