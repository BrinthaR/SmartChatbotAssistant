import json
import re
import random_responses


# Load JSON data
def load_json(file):
    with open(file) as bot_responses:
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses)


# Store JSON data
response_data = load_json("bot.json")


def get_response(input_string):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = []
    response_type = None # initialize response type

    # Determine response type based on user input
    for response in response_data:
        if any(word in split_message for word in response["user_input"]):
            response_type = response["response_type"]
            break  # Stop iterating once response type is determined

    if response_type is None:
        return random_responses.random_string()

    # Filter responses based on response type
    filtered_responses = [response for response in response_data if response["response_type"] == response_type]

    # Check all the filtered responses
    for response in filtered_responses:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        # Check if there are any required words
        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

            # Amount of required words should match the required score
            if required_score == len(required_words):

                # Check each word the user has typed
                for word in split_message:
                    # If the word is in the response, add to the score
                    if word in response["user_input"]:
                        response_score += 1

                # Add score to list
                score_list.append(response_score)
                # Debugging: Find the best phrase

    # Check if input is empty
    if input_string == "":
        return "Please type something so we can chat :("

    # If there is no good response, return a random one.
    if score_list:
        best_response = max(score_list)
        response_index = score_list.index(best_response)
        return response_data[response_index]['bot_response']
    else:
        return random_responses.random_string()


# usage example
while True:
    user_input = input("You: ")
    print("Bot:", get_response(user_input))
