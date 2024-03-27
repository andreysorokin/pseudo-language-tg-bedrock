from flask import Flask, jsonify, make_response, request

from telebot import bot
from logger import logger

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
async def webhook():
    update_json = request.get_json()
    logger.info(f"Processing request {update_json}")
    # Log the update (just for demonstration purposes)

    from telegram import Update
    update = Update.de_json(update_json, bot)
    # Due to some weird incompatibility in API.
    # Bot attribute is now immutable
    if update.message_reaction:
        # not supported in origami
        bot._call_listeners('on_message_reaction', update.message_reaction)
    else:
        bot._call_listeners(
            'on_message',
            update.effective_message)
        bot._handle_message(update.effective_message)

    # Respond to Telegram that the update was received successfully
    return jsonify({"ok": True})


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
