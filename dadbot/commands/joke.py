import random


class Joke():
    def __init__(self, jokes=[]):
        self.jokes = jokes

    def get_random_joke(self):
        return random.choice(self.jokes)

    def add_joke(self, new_joke):
        self.jokes.append(new_joke)
        return "Thanks! I'll tell my kids this one: \n {0}".format(new_joke)
