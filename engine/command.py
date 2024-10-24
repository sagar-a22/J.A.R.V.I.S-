import pyttsx3
import speech_recognition as sr
import eel
import time


def speak(text):

        text = str(text)
        engine = pyttsx3.init()  
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        eel.DisplayMessage(text)
        engine.say(text)
        eel.receiverText(text)
        engine.runAndWait()

def takecommand():
        r = sr.Recognizer()

        with sr.Microphone() as source:
                print("listening...")
                eel.DisplayMessage('listening...')
                r.pause_threshold=1
                r.adjust_for_ambient_noise(source)

                audio = r.listen(source)     

        try:
                print("Recognising...")
                eel.DisplayMessage('Recognising....')
                query= r.recognize_google(audio, language='en-in')
                print(f"User said: {query}")
                eel.DisplayMessage(query)
                time.sleep(2)
                # speak(query)
                

        except Exception as e:
                print(f"Error: {str(e)}")
                return "Couldn't recognise"       

        return query.lower() 

# text= takecommand()
# speak(text)

@eel.expose
def allCommands(message=1):

        if message==1:
                query= takecommand()
                # print(query)
                eel.senderText(query)
        else:
                query=message
                eel.senderText(query)
                   
        try: 
                if "open" in query:
                        from engine.features import openCommand
                        openCommand(query)

                elif "on youtube" in query:
                        from engine.features import PlayYoutube
                        PlayYoutube(query)      

                elif "send message" in query or "phone call" in query or "video call" in query:
                    from engine.features import findContact, whatsApp
                    message = ""
                    contact_no, name = findContact(query)
                    if(contact_no != 0):

                        if "send message" in query:
                                flag = 'message'
                                speak("what message to send")
                                query = takecommand()
                                
                        elif "phone call" in query:
                                flag = 'call'
                               

                        else:
                                flag = 'video call'
                        
                        whatsApp(contact_no, query, flag, name)          

                else:
                       from engine.features import chatbot
                       chatbot(query)     
        except:
                print("error")

        eel.ShowHood()