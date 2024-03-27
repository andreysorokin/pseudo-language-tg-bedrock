class Message:
    def __init__(self, chat_id, message_id, user_id, text, reactions=None):
        if reactions is None:
            reactions = dict()
        if reactions is None:
            reactions = {}
        self.chat_id = chat_id
        self.message_id = message_id
        self.user_id = user_id
        self.text = text
        self.reactions = reactions


from .base import BaseDAO


class MessagesDAO(BaseDAO):
    def to_item(self, message):
        """Converts a Message object to a DynamoDB item."""
        return {
            'chatId': message.chat_id,
            'messageId': message.message_id,
            'userId': message.user_id,
            'text': message.text,
            'reactions': message.reactions
        }

    def from_item(self, item):
        """Converts a DynamoDB item to a User object."""
        return Message(
            chat_id=item['chatId'],
            message_id=item['messageId'],
            user_id=item['userId'],
            text=item['text'],
            reactions=item['reactions']
        )

    def set_user_reaction(self, chat_id, message_id, user_id, reaction_type):
        key = {'chatId': chat_id, 'messageId': message_id}
        text_record = self.get(key)
        if text_record is None:
            return {}
        return self.update(key,
                    f"set reactions.#userId = :reactionType",
                    expression_attribute_names={'#userId': str(user_id)},
                    expression_attribute_values={":reactionType": str(reaction_type)},
                    return_values='ALL_NEW'
                )

