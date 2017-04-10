import random


class Advice():
    def __init__(self):
        self.advice = ["Never spit into the wind."]

    def get_random_advice(self):
        return random.choice(self.advice)
