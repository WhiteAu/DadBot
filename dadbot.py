import configparser
import os
import time

from dadbot.commands.advice import Advice
from dadbot.commands.joke import Joke

from slackclient import SlackClient

config = configparser.ConfigParser()
configFilePath = 'config'
config.read(configFilePath)

setup=config['setup']

BOT_NAME=setup['botname']
slack_client = SlackClient(os.environ.get(setup['token_var']))

BOT_ID = os.environ.get(setup['id_var'])

AT_BOT = "<@" + BOT_ID + ">"

'''
Bot Commands
'''
JOKE_COMMAND = "joke"
TELL_COMMAND = "listen"
WISDOM_COMMAND = "advice"

joke_list=List = open("jokes.txt").readlines()
joke_cmd = Joke(joke_list)
advice_cmd = Advice()

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. " + \
               "Do you want me to tell you a *" + JOKE_COMMAND +"?"
    if command.startswith(JOKE_COMMAND):
        response = joke_cmd.get_random_joke()
    elif command.startswith(TELL_COMMAND):
        _, _, new_joke = command.partition(TELL_COMMAND)
        response = joke_cmd.add_joke(new_joke)
    elif command.startswith(WISDOM_COMMAND):
        response = advice_cmd.get_random_advice()
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("DadBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
