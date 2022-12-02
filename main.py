from tkinter import *
import os
import urllib.request
import json
import pyttsx3
import speech_recognition
import threading


def api_response(msg):
    query = ("+".join(msg.split()))
    source = urllib.request.urlopen('http://ec2-54-196-248-192.compute-1.amazonaws.com/?query='+query).read()
    list_of_data = json.loads(source)
    return list_of_data['reply']

def botReply():
    question=questionField.get()
    question=question.capitalize()
    answer=api_response(question)
    textarea.insert(END,'You: '+question+'\n\n')
    textarea.insert(END,'Bot: '+str(answer)+'\n\n')
    pyttsx3.speak(answer)
    questionField.delete(0,END)

def audioToText():
    sr = speech_recognition.Recognizer()
    while True:
        try:
            with speech_recognition.Microphone() as m:
                sr.adjust_for_ambient_noise(m,duration=0.2)
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

textarea=Text(centerFrame,font=('times new roman',20,'bold'),height=10,yscrollcommand=scrollbar.set
              ,wrap='word')
textarea.pack(side=LEFT)
scrollbar.config(command=textarea.yview)

questionField=Entry(root,font=('verdana',20,'bold'))
questionField.pack(pady=15,fill=X)

askPic=PhotoImage(file='ask.png')


askButton=Button(root,image=askPic,command=botReply)
askButton.pack()

def click(event):
    askButton.invoke()


root.bind('<Return>',click)
thread = threading.Thread(target=audioToText)
thread.setDaemon(True)
thread.start()
root.mainloop()