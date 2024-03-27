import os

from origamibot import OrigamiBot
from origamibot.listener import Listener
from llm import joker
from logger import logger

class MessageListener(Listener):  # Event listener must inherit Listener
    def __init__(self, bot: OrigamiBot):
        self.bot = bot
        self.m_count = 0

    def on_message(self, message):  # called on every message
        from db import messagesDAO
        from db.messages import Message
        logger.debug(f"Saving message { message.id} in chat {message.chat.id}")
        messagesDAO.put(Message(message.chat.id, message.id, message.from_user.id, message.text))
        # self.m_count += 1
        # print(f'Total messages: {self.m_count}')

    def on_message_reaction(self, message_reaction):  # called on every message
        logger.debug(f"Updating reactions for {message_reaction.user.id} in chat {message_reaction.chat.id}")
        from db import messagesDAO
        update_result = messagesDAO.set_user_reaction(message_reaction.chat.id, message_reaction.message_id,
                                      message_reaction.user.id,
                                      message_reaction.new_reaction[0].emoji if len(message_reaction.new_reaction) > 0 else '')

        if ('Attributes' in update_result
                and update_result['Attributes'] is not None
                and update_result['Attributes']['reactions'] is not None):
            count = 0
            for user, reaction in update_result['Attributes']['reactions'].items():
                count += len(reaction)
            if count > 1:
                # joker.get_joke()
                logger.info("We have received {} reactions for message: {} in chat: {}".format(count, message_reaction.message_id, message_reaction.chat.id))
                if 'text' in update_result['Attributes']:
                    # TBD - add async here
                    joke_input = update_result['Attributes']['text']
                    joke_output = joker.get_joke(joke_input)
                    bot.send_message(message_reaction.chat.id, joke_output)



    def on_command_failure(self, message, err=None):  # When command fails
        if err is None:
            self.bot.send_message(message.chat.id,
                                  'Command failed to bind arguments!')
        else:
            self.bot.send_message(message.chat.id,
                                  f'Error in command:\n{err}')

bot = OrigamiBot(os.environ['TELEGRAM_TOKEN'])
bot.add_listener(MessageListener(bot))