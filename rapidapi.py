import requests
import speech_recognition as sr
import pyttsx3

def get_definition(word):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        print("Definition for", word)
        definitions = []
        for entry in data:
            for meaning in entry['meanings']:
                definitions.append(f"- {meaning['partOfSpeech']}: {meaning['definitions'][0]['definition']}")
                print(definitions[-1])

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
        print("Please say a word:")
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

if __name__ == "__main__":
    user_input = speech_to_text()

    if user_input:
        definitions = get_definition(user_input)

        if definitions:
            response_text = " ".join(definitions)
            print("Response:", response_text)
            text_to_speech(response_text)
