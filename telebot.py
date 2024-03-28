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
        logger.debug(f"Saving message {message.id} in chat {message.chat.id}")
        messagesDAO.put(Message(message.chat.id, message.id, message.from_user.id, message.text))
        # self.m_count += 1
        # print(f'Total messages: {self.m_count}')

    def on_message_reaction(self, message_reaction):  # called on every message
        logger.debug(f"Updating reactions for {message_reaction.user.id} in chat {message_reaction.chat.id}")
        from db import messagesDAO
        new_emojii = message_reaction.new_reaction[0].emoji if len(message_reaction.new_reaction) > 0 else ''
        update_result = messagesDAO.set_user_reaction(message_reaction.chat.id, message_reaction.message_id,
                                                      message_reaction.user.id,
                                                      new_emojii)

        reactions_count = dict()
        if ('Attributes' in update_result
                and update_result['Attributes'] is not None
                and update_result['Attributes']['reactions'] is not None):
            count = 0
            for user, reaction in update_result['Attributes']['reactions'].items():
                if reaction in reactions_count:
                    reactions_count[reaction] += 1
                else:
                    reactions_count[reaction] = 1

        logger.debug(f"Summarized the reactions: {str(reactions_count)}")

        if (new_emojii != '' and new_emojii in reactions_count
                and reactions_count[new_emojii] > (1 if message_reaction.chat.id < 0 else 0) and 'text' in update_result['Attributes']):
            # joker.get_joke()
            logger.info(
                "We have received {}, {} reactions for message: {} in chat: {}".format(new_emojii,
                                                                                       reactions_count[new_emojii],
                                                                                       message_reaction.message_id,
                                                                                       message_reaction.chat.id))
            input = update_result['Attributes']['text']
            output = None
            if new_emojii == '👀':
                output = joker.get_spanish(input)
            elif new_emojii == '🦄':
                output = joker.get_joke(input)

            if output is not None:
                bot.send_message(message_reaction.chat.id, output, reply_to_message_id=message_reaction.message_id)

    def on_command_failure(self, message, err=None):  # When command fails
        if err is None:
            self.bot.send_message(message.chat.id,
                                  'Command failed to bind arguments!')
        else:
            self.bot.send_message(message.chat.id,
                                  f'Error in command:\n{err}')


bot = OrigamiBot(os.environ['TELEGRAM_TOKEN'])
bot.add_listener(MessageListener(bot))
