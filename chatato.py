import json
from difflib import get_close_matches
import pyttsx3
import speech_recognition as sr

def load_voice_bot(talk_speed: int, voice_id: int): # Return voice engine
    engine = pyttsx3.init()
    engine.setProperty("rate", talk_speed)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)
    return engine

def load_knowledge_base (file_path : str): # Return dict
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]): #Return str or None
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6) #n = number answers returned, cutoff= % similarity
    return matches[0] if matches else None

def get_answer(question: str, knowledge_base: dict): # return str or None
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return (q["multi-option"], q['answer'])

def listen_for_input(r): # Return str
    while(1):    
    # Exception handling to handle
    # exceptions at the runtime
        try: 
            # use the microphone as source for input.
            with sr.Microphone() as source2:   
                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level 
                r.adjust_for_ambient_noise(source2, duration=0.2)   
                #listens for the user's input 
                print("Listening...")
                audio2 = r.listen(source2)
                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                return MyText        
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))        
        except sr.UnknownValueError:
            print("unknown error occurred")

def speak(engine, response): # Return None
    print('Bot: ' + response)
    engine.say(response)
    engine.runAndWait()
    engine.stop()       
    
def is_multi_option(response):
    # List of keywords that indicate a multi-option response
    multi_option_keywords = ["options", "choices", "list", "all", "every", "any", "various", "different", "several", "many", "multiple"]

    # Convert the response to lowercase and split it into words
    response_words = response.lower().split()

    # Check if any of the multi-option keywords are in the response
    for word in response_words:
        if word in multi_option_keywords:
            return True

    # If no multi-option keywords are found, return False
    return False
def chat_bot():
    engine = load_voice_bot(200, 1)
    r = sr.Recognizer() 
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    speak(engine, "Greetings!  I am Chatato, human-cyborg relations!  What would you like to ask? Or you can say \"quit\"")
    while True:
        user_input = listen_for_input(r)
        print("You: " + user_input)
        #user_input: str = input('You: ')

        if user_input.lower() == 'quit':
            speak(engine, "I see.  I hope I was of service!  Goodbye!")
            break

        best_match: str | None = find_best_match(user_input, [q['question'] for q in knowledge_base['questions']])

        if best_match:
            answer = get_answer(best_match, knowledge_base)
            if knowledge_base["questions"][best_match]["multi_option"]:
                options = knowledge_base["questions"][best_match]["answer"]
                for option in options:
                    speak(engine, option)
                    user_input = listen_for_input(r)
                    print("You: " + user_input)
                    #user_input: str = input('You: ')
                    if user_input.lower() == 'next':
                        continue
                    else:
                        break
                
            else:
                speak(engine, answer)
        else:
            if is_multi_option(user_input):
                speak(engine, "I don\'t know the answer.  But it sounds like there can be multiple choices.  Can you teach me some responses? Or just say \"skip\"")
                new_answer = listen_for_input(r)
                print("You: " + new_answer)
                #new_answer: str = input('Type the answer or "skip" to skip: ')
                if new_answer.lower() != 'skip':
                    choices = []
                    while new_answer.lower() != 'no':
                        choices.append(new_answer)
                        speak(engine, "I see!  Any other responses? Or just say \"no\"")
                    knowledge_base["questions"].append({"question": user_input, "answer": new_answer, "multi-option": True})
                    save_knowledge_base('knowledge_base.json', knowledge_base)
                    speak(engine, "I see.  I will remember those responses.  Anything else you would like to ask?  Or you can say \"quit\"")
                else:
                    speak(engine, "I see.  I will proceed to forget what you said.  Anything else you would like to ask? Or you can say \"quit\"")
                
            else:
                speak(engine, "I don\'t know the answer.  Can you teach me? Or just say \"skip\"")
                new_answer = listen_for_input(r)
                print("You: " + new_answer)
                #new_answer: str = input('Type the answer or "skip" to skip: ')

                if new_answer.lower() != 'skip':
                    knowledge_base["questions"].append({"question": user_input, "answer": new_answer, "multi-option": False})
                    save_knowledge_base('knowledge_base.json', knowledge_base)
                    speak(engine, "Thank you! I learned a new response!  Anything else you would like to ask?")
                else:
                    speak(engine, "I see.  I will proceed to forget what you said.  Anything else you would like to ask? Or you can say \"quit\"")

if __name__ == '__main__':
    chat_bot()