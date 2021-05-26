import pyttsx3 
import speech_recognition as sr 
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import requests
import numpy as np
import time
import winsound
from plyer import notification
import facebook as fb


weather_key = os.environ['weather_key']
insta_ID=os.environ['insta_ID']
insta_pass=os.environ['insta_pass']
facebook_key="EAADUAmQfjacBAFikAYuIZBGMbM3OaiHZCcolPG4tABDZCV4UyIi9Vqy2UpCIZByNQ2ZCWQdmu9byzUbfP1C3nahS6mnkrJ0nH4Rfn2oBKsL75aR8w611FUdBz1xARAElKWrLvT4ricLiiIqOah8xCiy1hwjxXAZAEHIiU4NyGeFelbOTO4ZBCZAqMBQ7KPgkZChJdhmZBDUQqn6nM0KWZCncuzC"
el=fb.GraphAPI(facebook_key)
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def notify(interval,Title,Message):
    time.sleep(interval)
    winsound.Beep(2500,2000)
    notification.notify(
        title = Title,
 	message = Message,
 	app_icon =r"C:\Users\owner\Desktop\RAGHAV\icon.ico",
 	timeout= 12
 	)

def converter(hour,minutes,title,Message):
    current_time=time.time()
    current_time=time.ctime(current_time).split()[3].split(":")
    c_hour=int(current_time[0])
    c_minute=int(current_time[1])
    c_second=int(current_time[2])
    r_second=(hour*60*60)+(minutes*60)
    if (c_hour<=hour):
        c_second=(c_hour*60*60)+(c_minute*60)+c_second
        r_second=r_second-c_second
        if(r_second>0):
            notify(r_second,title,Message)
            return 1
    return -1


def std_time(hour,minutes,parity,title,Message):
    if(parity=='a' or parity=='A'):
        if (hour=='12'):
            hour=0
            minutes=int(minutes)
        else:
            hour=int(hour)
            minutes=int(minutes)
    else:
        if(hour=='12'):
            hour=int(hour)
            minutes=int(minutes)
        else:
            hour=int(hour)+12
            minutes=int(minutes)

    return converter(hour,minutes,title,Message)


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


def insta(photoname,caption):
    bot.login(username=insta_ID,password=insta_pass)
    bot.upload_photo("C:\\Users\\owner\\Desktop\\RAGHAV\\"+photoname+".jpg",caption=caption)

def facebook(photoname,caption):
    el.put_photo(open("C:\\Users\\owner\\Desktop\\RAGHAV\\"+photoname+".jpg","rb"),message=caption)
    

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
            print(f"Sir, the time is {strTime} IST")
            speak(f"Sir, the time is {strTime} I S T")
            break
        elif (('instagram' in query)):
            from instabot import Bot

            bot=Bot()
            speak("what is the name of the photo")
            print("what is the name of the photo?")
            photoname=takeCommand()
            photoname=photoname.lower()
            speak("what should be the caption")
            print("what should be the caption?")
            caption=takeCommand()
            print(caption)
            insta(photoname,caption)

        elif ('facebook' in query):
            speak("what is the name of the photo")
            print("what is the name of the photo?")
            photoname=takeCommand()
            photoname=photoname.lower()
            speak("what should be the caption")
            print("what should be the caption?")
            caption=takeCommand()
            print(caption)
            facebook(photoname,caption)

        elif(('reminder' in query) or ('remind me' in query)):
            speak("at what time you want me to remind you")
            print("At what time you want me to remind you?")
            remind_time=takeCommand().lower()
            print(remind_time)
            remind_time=remind_time.split()
            hour=remind_time[0]
            minutes=remind_time[2]
            parity=remind_time[4][0]
            title='!! Reminder !!'
            speak("what should be the reminder")
            print("What should be the reminder?")
            message=takeCommand()
            print("Reminder")
            print(message)
            if (std_time(hour,minutes,parity,title,message)==1):
                pass
            else:
                print("Wrong time input")
                
        
        elif 'send an email' in query:
            try:
                verification()
                to =os.environ['my_email']
                content = takeCommand()
                sendEmail(to,content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send this email, please try again")    
        elif 'exit' in query:
            break
