import requests
import speech_recognition as sr
import pyttsx3
from Task import InputExecution
from Task import NonInputExecution
from Speak import Say
from Listen import Listen
import random
import json
import torch
from Brain import NeuralNet
from NeuralNetwork import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open("intents.json", "r",  encoding='utf-8') as json_data:
    intents = json.load(json_data)

FILE = "TrainData.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

Name = "MadMax"

def web_search(query):
    # Replace 'YOUR_SEARCH_URL' with the actual URL you want to search
    search_url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{query}'

    try:
        response = requests.get(search_url)
        response.raise_for_status()
        
        data = response.json()
        print(f"Definitions for {query}:")
        definitions = []

        for entry in data:
            for meaning in entry['meanings']:
                definition_text = f"- {meaning['partOfSpeech']}: {meaning['definitions'][0]['definition']}"
                definitions.append(definition_text)
                print(definition_text)

        return definitions

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
    return None

def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Please say something:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio)
        print("You said:", user_input)
        return user_input
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def Main():
    listening = False  # Flag to indicate whether to listen or not

    while True:
        sentence = Listen()
        result = str(sentence)

        if sentence.lower() == 'mad max':
            Say("Listening started.")
            listening = True
            continue  # Skip the rest of the loop and go to the next iteration

        if sentence.lower() == 'stop':
            Say("Listening stopped.")
            break  # Exit the loop and end the program

        if not listening:
            # If not in listening mode, continue to the next iteration
            continue

        # Process the user input when in listening mode
        sentence = tokenize(sentence)
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)

        _, predicted = torch.max(output, dim=1)

        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    reply = random.choice(intent["responses"])

                    if "time" in reply:
                        NonInputExecution(reply)

                    elif "date" in reply:
                        NonInputExecution(reply)

                    elif "wikipedia" in reply:
                        InputExecution(reply, sentence)

                    elif "google" in reply:
                        InputExecution(reply, result)

                    elif "youtube" in reply:
                        NonInputExecution(reply)

                    elif "temperature" in reply:
                        InputExecution(reply, result)

                    elif "command prompt" in reply:
                        NonInputExecution(reply)
                    elif "word" in reply:
                        NonInputExecution(reply)
                    elif "vs code" in reply:
                        NonInputExecution(reply)


                    else:
                        Say(reply)

        else:
            Say("I'm not sure. Let me look that up for you.")
            search_result = web_search(result)

            if search_result:
                # print("Search Result:", search_result)
                text_to_speech(" ".join(search_result))  # Speak out the search result
            else:
                print("No search results found.")

# Example usage:
Main()
