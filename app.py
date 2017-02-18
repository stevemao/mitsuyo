#!/usr/bin/env python

from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import urllib.request, urllib.parse, urllib.error
import json
import os

from flask import Flask
from flask import request
from flask import make_response
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Flask app should start in global layout
app = Flask(__name__)

chatbot = ChatBot(
    'mitsuyo',
    storage_adapter={
        'import_path': "chatterbot.storage.MongoDatabaseAdapter",
        'database_uri': os.getenv('MONGODB_URI', '127.0.0.1:27017'),
        'database': 'heroku_sm0n0l18',
    },
    # trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

# Train based on the corpus
# chatbot.train("chatterbot.corpus.english")
# chatbot.train("chatterbot.corpus.chinese")

chatbot.set_trainer(ListTrainer)

chatbot.train([

])

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    speech = chatbot.get_response(req.get('result').get('resolvedQuery'))
    speech = str(speech)

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "ichat-us"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
