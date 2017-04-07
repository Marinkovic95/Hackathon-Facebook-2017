from flask import Flask, request
import requests

app = Flask(__name__)

ACCESS_TOKEN = "EAAbCANkytUYBADk2BrjgqsD09qoXjYfBp7ZClb4CfSP5OZA7fpUFudovmXcoLnnsGvSjqC8crUxPvvehtuZBdarhHwoZC3z5Gm2fTLtUJ7bQaKlCAumOepe1BfUyNNWS21px1rDYsMPgjaiEZCyzylC4C4CRVdnW6RBi7InVxBgZDZD"


def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post(
        "https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN,
        json=data)
    print (resp.content)


def process_message(sender, message):
    words = message.split()
    reply(sender, "tus palabras fueron: {}".format(words))


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']

    process_message(sender, message)
    return "ok"


if __name__ == '__main__':
    app.run(debug=True)
