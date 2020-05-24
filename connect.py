from pywebostv.discovery import *    # Because I'm lazy, don't do this.
from pywebostv.connection import *
from pywebostv.controls import *
#import speech_recognition as s
#r=s.Recognizer()
import time
import bs4, requests
import yaml
import os
#import keyboard
# key init
if 'store.yaml' in os.listdir():
    with open('store.yaml', 'rt') as file:
        store = yaml.safe_load(file)
else:
    store = {}
client = WebOSClient("192.168.100.8")
client.connect()
for status in client.register(store):
    if status == WebOSClient.PROMPTED:
        print("Please accept the connect on the TV!")
    elif status == WebOSClient.REGISTERED:
        print("Registration successful!")
with open('store.yaml', 'wt') as file:
    yaml.safe_dump(store, file)
app = ApplicationControl(client)
apps = app.list_apps()          # Returns a list of `Application` instances.
media = MediaControl(client)
system = SystemControl(client)
tv_control = TvControl(client)
inp = InputControl(client)
# Let's launch YouTube!
yt = [x for x in apps if "youtube" in x["title"].lower()][0]
while True:
    x=input(">> ")
    x=x.lower()
    try:
        if "play" in x:
            x=x.replace("play ", "")       
            name = x
            print(f"Name: {name}")
            fullcontent = ('http://www.youtube.com/results?search_query=' + name)
            text = requests.get(fullcontent).text
            soup = bs4.BeautifulSoup(text, 'html.parser')
            img = soup.find_all('img')
            div = [ d for d in soup.find_all('div') if d.has_attr('class') and 'yt-lockup-dismissable' in d['class']]
            a = [ x for x in div[0].find_all('a') if x.has_attr('title') ]
            title = (a[0]['title'])
            print(f"About to play: {title}")
            a0 = [ x for x in div[0].find_all('a') if x.has_attr('title') ][0]
            a0["href"]=a0["href"].replace("/watch?v=","")
            launch_info = app.launch(yt, content_id=a0["href"])
        if "search" == x:
            with s.Microphone() as source:
                while True:
                    if not keyboard.is_pressed("q"):
                        print("Say out the query")
                        audio=r.listen(source)
                        try:
                            text=r.recognize_google(audio)
                            print(f"Searching for {text}")
                            fullcontent = ('http://www.youtube.com/results?search_query=' + text)
                            text = requests.get(fullcontent).text
                            soup = bs4.BeautifulSoup(text, 'html.parser')
                            img = soup.find_all('img')
                            div = [ d for d in soup.find_all('div') if d.has_attr('class') and 'yt-lockup-dismissable' in d['class']]
                            a = [ x for x in div[0].find_all('a') if x.has_attr('title') ]
                            title = (a[0]['title'])
                            print(f"About to play: {title}")
                            a0 = [ x for x in div[0].find_all('a') if x.has_attr('title') ][0]
                            a0["href"]=a0["href"].replace("/watch?v=","")
                            launch_info = app.launch(yt, content_id=a0["href"])
                            break
                        except:
                            print("Sorry Couldn't get that")
                    else:
                        break
        if "volume" == x:
            while True:
                if keyboard.is_pressed("w"):
                    media.volume_up()
                    time.sleep(0.1)
                if keyboard.is_pressed("s"):                    
                    media.volume_down()
                    time.sleep(0.1)
                if keyboard.is_pressed("q"):
                    break
        if "volume" in x:
            x=x.split(" ")
            if x[1] == "+" or x[1] == "up":
                media.volume_up()
            if x[1] == "-" or x[1] == "down":
                media.volume_down()
        if "close" in x:
            app.close(launch_info)
        if "next" == x:
            tv_control.channel_up()
        if "back" == x:
            tv_control.channel_down()
        if "notify" in x:
            x=x.replace("notify ", "")
            system.notify(x)
        if "controls" in x:
            inp.connect_input()
            while True:            
                if keyboard.is_pressed("a"):                    
                    inp.left()
                if keyboard.is_pressed("d"):                    
                    inp.right()
                if keyboard.is_pressed("q"):
                    inp.disconnect_input()
                    break                    
        if "move" == x:
            inp.connect_input()
            while True:
                if keyboard.is_pressed("w"):
                    inp.move(0, -1)                    
                if keyboard.is_pressed("s"):                    
                    inp.move(0, 1)                   
                if keyboard.is_pressed("a"):                    
                    inp.move(-1, 0)
                if keyboard.is_pressed("d"):                    
                    inp.move(1, 0)
                if keyboard.is_pressed("enter"):                    
                    inp.click()
                    time.sleep(0.1)
                if keyboard.is_pressed("q"):
                    inp.disconnect_input()
                    break
    except Exception as ex:
        print(f"Error >> {ex}")
'''media = MediaControl(client)
time.sleep(1)
for i in range(1, 21):
    media.volume_up()
    print(i)
    time.sleep(1)
    media.volume_down()
    time.sleep(1)'''
#system = SystemControl(client)
#system.notify("This is a notification message!")
