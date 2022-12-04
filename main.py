from tkinter import *
import os
import urllib.request
import json
#import pyttsx3
from gtts import gTTS
import os,time
import speech_recognition
import threading
import quickstart
import datetime as dt


def api_response(msg):
    query = ("+".join(msg.split()))
    source = urllib.request.urlopen('http://ec2-44-201-111-213.compute-1.amazonaws.com/?query='+query).read()
    list_of_data = json.loads(source)
    return list_of_data['reply']

def botReply():
    question=questionField.get()
    question=question.capitalize()
    reply=api_response(question)
    if reply=="all_classes":
        events = quickstart.main()
        all_events = []
        for event in events:
            #all_events.append()
            
            d= event['start'].split('T',1)[0]
            t_half= event['start'].split('T',1)[1]
            t= t_half.split('+')[0]
            all_events.append({"date":d,"time":t,"title":event['summary']})
            
        s="All your events are "
        for event in all_events:
            s+=str(event['title'])+" at "+str(event['time'])+" "+str(event['date'])+","
        answer = s
    elif reply == "today_schedule":
        events = quickstart.main()
        today = dt.datetime.today().strftime('%Y-%m-%d')
        first_event_time = events[0]['start']
        first_event_time = first_event_time.split('T',1)[0]
        todays_events = []
        for event in events:
            d= event['start'].split('T',1)[0]
            t_half= event['start'].split('T',1)[1]
            t= t_half.split('+')[0]
            if d==first_event_time:
                todays_events.append({"date":d,"time":t,"title":event['summary']})
        if len(todays_events)>1:
            s= "Today's events are "
        else:
            s="Today's event is "
        for event in todays_events:
            s+=str(event['title'])+" at "+str(event['time'])+" "+str(event['date'])+","
        answer = s
        
        
        #answer = str(events[0]['summary'])
    else:
        answer = reply
    textarea.insert(END,'You: '+question+'\n\n')
    textarea.insert(END,'Bot: '+str(answer)+'\n\n')
    myobj = gTTS(text=str(answer),slow= False)
    myobj.save("voice.mp3")
    os.system("mpg123 voice.mp3")
    questionField.delete(0,END)

def audioToText():
    sr = speech_recognition.Recognizer()
    while True:
        try:
            with speech_recognition.Microphone(device_index=0) as m:
                sr.adjust_for_ambient_noise(m,duration=0.5)
                audio = sr.listen(m)
                query= sr.recognize_google(audio)
                
                questionField.delete(0,END)
                questionField.insert(0,query)
            botReply()
        except Exception as e:
            print(e)


root=Tk()

root.geometry('500x570+100+30')
root.title('Clementine')
root.config(bg='deep pink')

logoPic=PhotoImage(file='pic.png')

logoPicLabel=Label(root,image=logoPic,bg='deep pink')
logoPicLabel.pack(pady=5)

centerFrame=Frame(root)
centerFrame.pack()

scrollbar=Scrollbar(centerFrame)
scrollbar.pack(side=RIGHT)

textarea=Text(centerFrame,font=('times new roman',16,'bold'),height=10,yscrollcommand=scrollbar.set
              ,wrap='word')
textarea.pack(side=LEFT)
scrollbar.config(command=textarea.yview)

questionField=Entry(root,font=('verdana',16,'bold'))
questionField.pack(pady=15,fill=X)

askPic=PhotoImage(file='ask.png')


askButton=Button(root,image=askPic,command=botReply)
askButton.pack()

def click(event):
    askButton.invoke()


root.bind('<Return>',click)

root.mainloop()
