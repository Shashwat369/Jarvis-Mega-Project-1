import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import openai

# Initialize the recognizer
r = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "pub_62490d48d857ce91cbe252536f336418517e0"

def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def aiProcess(command):
    openai.api_key = "your_openai api key"
# Create a chat completion
    completion = openai.ChatCompletion.create(
         model="gpt-3.5-turbo",  # Or use 'gpt-4' if available
         messages=[
             {"role": "system", "content": "You are a helpful assistant."},
             {"role": "user", "content": command}
    ]
    )

# Print the response
    return completion.choice[0].message.content
    
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("http://google.com")
        
    elif "open facebook" in c.lower():
        webbrowser.open("http://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("http://youtube.com")
    elif "open hotstar" in c.lower():
        webbrowser.open("http://hotstar.com")
    elif "open whatsapp" in c.lower():
        webbrowser.open("http://whatsapp.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("http://linkedin.com")
    elif "open jiotv" in c.lower():
        webbrowser.open("http://jiotv.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ", 1)[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find the song {song}.")

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={newsapi}")
        if r.status_code == 200:
           data = r.json()
           articles = data.get('articles', [])
           for article in articles:
                speak(article['title'])
        else:
             speak("Unable to fetch news at the moment.")

            
    elif "stop listening" in c.lower():
        speak("Goodbye!")
        exit()

            
    else:
        output = aiProcess(c)
        speak(output)
       
    
# Use the microphone as the audio source
if __name__== '__main__':
    speak("Initializing Jarvis...")
    while True:
        r=sr.Recognizer()

        try:
            with sr.Microphone() as source:
                print("Listening To Your Command Master...")  # Prompt the user to speak
                audio = r.listen(source , timeout=2 , phrase_time_limit=1) 
                r.adjust_for_ambient_noise(source, duration=1)  
                command = r.recognize_google(audio) 
                if(command.lower()== "jarvis"):
                    speak("Ya")
                    with sr.Microphone() as source:
                         print("Listening...")  # Prompt the user to speak
                         audio = r.listen(source , timeout=2) 
                         r.adjust_for_ambient_noise(source, duration=1)  
                         command = r.recognize_google(audio)
                        
                         processCommand(command)

        except Exception as e:
            print(f"Could not request results; {e}")
        print("Recognizing...")

