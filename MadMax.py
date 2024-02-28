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
with open("intents.json", "r") as json_data:
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


# def Main():
#     while True:


#         sentence = Listen()
#         result = str(sentence)

#         if sentence == 'stop':
#     #     exit()

#             Say("Goodbye!")
#             break

#     sentence = tokenize(sentence)
#     X = bag_of_words(sentence, all_words)
#     X = X.reshape(1, X.shape[0])
#     X = torch.from_numpy(X).to(device)

#     output = model(X)

#     _, predicted = torch.max(output, dim=1)

#     tag = tags[predicted.item()]

#     probs = torch.softmax(output, dim=1)
#     prob = probs[0][predicted.item()]

#     if prob.item() > 0.75:
#         for intent in intents['intents']:
#             if tag == intent["tag"]:
#                 reply = random.choice(intent["responses"])

#                 if "time" in reply:
#                     NonInputExecution(reply)

#                 elif "date" in reply:
#                     NonInputExecution(reply)

#                 elif "wikipedia" in reply:
#                     InputExecution(reply, sentence)

#                 elif "google" in reply:
#                     InputExecution(reply, result)

#                 elif "youtube" in reply:
#                     NonInputExecution(reply)

#                 elif "temperature" in reply:
#                     InputExecution(reply, result)

#                 else:
#                     Say(reply)


# while True:
#     Main()

def Main():
    listening = False  # Flag to indicate whether to listen or not

    while True:
        sentence = Listen()
        result = str(sentence)

        if sentence.lower() == 'start':
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

                    else:
                        Say(reply)

# Example usage:
Main()

