import random

r_feeling = "I don't have feelings because I'm a ChatBot and I am not yet equipped with such human qualities."

def unknown():
    response = ['Could you please re-phrase that?',
                '. . .',
                'Please give me more details.',
                'What does that mean?'][random.randrange(4)]
    return response