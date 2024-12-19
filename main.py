import re
import long_responses as long
from typing import List


# Function to calculate message probability based on recognized and required words
def message_probability(user_message: List[str], recognized_words: List[str],
                        single_response: bool = False, required_words: List[str] = None) -> int:
    """
    Calculates the probability that a user's message matches certain recognized words and required words.
    It returns a percentage value based on how many recognized words are present in the message.

    Parameters:
    - user_message (List[str]): A list of words from the user's message.
    - recognized_words (List[str]): A list of words that the bot recognizes.
    - single_response (bool, optional): If True, the function returns the probability even without required words.
    - required_words (List[str], optional): A list of words that must appear in the message for a valid match.

    Returns:
    - int: The probability (as a percentage) that the user's message matches the recognized words.

    Example:
    >>> message_probability(['hello', 'how', 'are', 'you'], ['hello', 'hey', 'hi'])
    33
    """
    if required_words is None:
        required_words = []

    message_certainty: int = 0
    has_required_words: bool = True

    # Count recognized words in the user message
    for word in user_message:
        if word in recognized_words:
            message_certainty += 1

    # Calculate the percentage of recognized words
    percentage: float = float(message_certainty) / float(len(recognized_words))

    # Check for required words in the user message
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Return percentage if all conditions are met
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message: List[str]) -> str:
    """
    Checks all possible responses for a given message and returns the one with the highest probability.
    It uses the message_probability function to calculate the probability of a match with recognized words.

    Parameters:
    - message (List[str]): A list of words from the user's message.

    Returns:
    - str: The best matching response based on the highest probability, or a default response if no match is found.

    Example:
    >>> check_all_messages(['hello', 'how', 'are', 'you'])
    'Hello!'
    """
    highest_prob_list: dict[str, int] = {}

    # Function to calculate response probabilities
    def calculate_response_probability(bot_response: str, list_of_words: List[str], single_response: bool = False,
                                       required_words: List[str] = None):
        if required_words is None:
            required_words = []
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Add different potential responses
    calculate_response_probability('Hello!', ['hy', 'hello', 'hey', 'aloha'], single_response=True)
    calculate_response_probability('I am doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    calculate_response_probability('You are welcome', ['thank', 'you', 'for', 'you\'re', 'help'],
                                   required_words=['thank', 'you'])
    calculate_response_probability(long.r_feeling, ['do', 'you', 'have', 'feelings'], required_words=['feelings'])

    # Find the response with the highest probability
    best_match: str = max(highest_prob_list, key=highest_prob_list.get)

    # Return the best match or a default response if no match is found
    return long.unknown() if highest_prob_list[best_match] < 1 else best_match


# Function to process user input and get a response
def get_response(user_input: str) -> str:
    """
    Processes the user's input, splits it into words, and passes it to check_all_messages to get the best response.

    Parameters:
    - user_input (str): The message input by the user.

    Returns:
    - str: The response generated based on the user's input.

    Example:
    >>> get_response("Hello, how are you?")
    'Hello!'
    """
    # Split the user input into words and make it lowercase
    split_message: List[str] = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response: str = check_all_messages(split_message)

    return response


# Testing the response system
while True:
    print('Bot: ' + get_response(input('You: ')))
