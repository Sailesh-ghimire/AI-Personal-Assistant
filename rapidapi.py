import requests

def get_definition(word):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        data = response.json()
        print("Definition for", word)
        for entry in data:
            for meaning in entry['meanings']:
                print(f"- {meaning['partOfSpeech']}: {meaning['definitions'][0]['definition']}")
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    user_input = input("Enter a word: ")
    get_definition(user_input)
