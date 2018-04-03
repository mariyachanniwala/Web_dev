from app import flaskApp
from flask import render_template, flash, redirect, url_for, request, jsonify, send_from_directory
from app.forms import LoginForm
from twilio.rest import Client
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
import requests
import os
from pymongo import MongoClient

mongoClient = MongoClient(
    '')
db = mongoClient['new']

account_sid = ""
auth_token = ""
subscription_key = ""
# assert subscription_key
text_analytics_base_url = "https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/"
sentiment_api_url = text_analytics_base_url + "sentiment"


@flaskApp.route('/')  # decorators in python, just like annotations in java
@flaskApp.route('/index')
def index():
    return render_template('index.html', title='Home')


@flaskApp.route('/public/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join('.', 'public'), filename)


@flaskApp.route('/send', methods=['GET', 'POST'])
def send():
    client = Client(account_sid, auth_token)

    to = request.form['to']
    productType = request.form['productType']
    firstName = request.form['firstName']
    firstMessage = request.form['firstMessage']

    db.config.remove()
    configData = {
        'negativeResponse': request.form['negativeResponse'],
        'positiveResponse': request.form['positiveResponse'],
        'firstMessage': firstMessage,
        'productType': productType,
        'firstName': firstName
    }
    db.config.insert_one(configData)

    client.api.account.messages.create(
        to="+1" + to,
        from_="+14248887756",
        body=firstMessage.replace('<firstName>', firstName).replace('<productType>', productType))
    return jsonify({'status': "SMS sent successfully"})


@flaskApp.route('/receiveMessage', methods=['GET', 'POST'])
def receiveMessage():
    body = request.values.get('Body', None)
    fromNumber = request.values.get('From', None)
    msgID = request.values.get('MessageSid', None)

    # Do sentiment analysis
    documents = {'documents': [
        {'id': '1', 'language': 'en',
         'text': body}
    ]}
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    response = requests.post(sentiment_api_url, headers=headers, json=documents)
    sentiments = response.json()

    # Store user response with sentiment in mongodb
    sms = db.sms
    sms_data = {
        'body': body,
        'from': fromNumber,
        'msgid': msgID,
        'sentiments': sentiments["documents"][0]['score']
    }
    sms.insert_one(sms_data)

    config = db.config.find_one()
    productType = config['productType']
    firstName = config['firstName']

    response = MessagingResponse()
    message = Message()
    for i in sentiments["documents"]:
        if i['score'] >= 0.5:
            message.body(
                config['positiveResponse'].replace('<firstName>', firstName).replace('<productType>', productType))
        else:
            message.body(
                config['negativeResponse'].replace('<firstName>', firstName).replace('<productType>', productType))

    response.append(message)
    return str(response)
