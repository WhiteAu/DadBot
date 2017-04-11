from __future__ import print_function

import random


class Joke():
    def __init__(self, jokes=[]):
        self.jokes = jokes
        self.learned_new_joke = False


    def get_random_joke(self):
        return random.choice(self.jokes)


    def add_joke(self, new_joke):
        self.jokes.append(new_joke)
        self.learned_new_joke = True

        return "Thanks! I'll tell my kids this one: \n {0}".format(new_joke)


    def save_jokes(self, file_loc):
        if self.learned_new_joke is False:
            return "I haven't heard any new jokes!"

        with open(file_loc, 'w') as fp:
            for joke in self.jokes:
                fp.write("{0}".format(joke))
        fp.close()
        
        self.learned_new_joke = False

        return "You're right I don't want to forget all these good jokes!"
