import requests
from clarifai_request import *
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient


app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])

client = MongoClient()
db = client.test

def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    user_number = request.values.get('From', None)
    body = request.values.get('Body', None).lower().strip();
    media_url = request.values.get('MediaUrl0', None);
    if (body == 'search'): #user request a search using the ingredients they have inputed
        user = db.users.find_one({'phone_number':user_number})
        ingredients = user['ingredients']
        responses = request_recipes(ingredients) 
        resp = format_response_to_user(responses); 
        db.users.remove({"phone_number" : user_number})
        return str(resp)

    if (media_url != None):
        ingredient = determine_ingredient(media_url)
    else:
        ingredient = body

    store_ingredient(user_number, ingredient);
    return("hello");


def store_ingredient(user_number, ingredient):
    """
    Stores ingredient into the database
    If user is new, new document is created
    If user already exists, ingredient is appended to the user's array of ingredients
    
    Arguments:
    user_number: phone number of user
    ingredient: ingredient to be stored
    """
    if (db.users.count({'phone_number':user_number}) == 0):
        db.users.insert({'phone_number':user_number, 'ingredients':[ingredient]})
    else:
        db.users.update_one({'phone_number':user_number}, {"$push":{'ingredients':ingredient}})
    

def request_recipes(ingredients):
    """
    Requests recipes from recipes api
    
    Arguments:
    ingredients: array of ingredients to search

    Returns:
    Reponse from the kitchen api in json format
    """
    key = open("apikey.txt").read().replace("\n", "")
    ingredients_to_query = ""
    for ingredients in ingredients:
        ingredients_to_query += ingredients + " "
    return requests.get("https://community-food2fork.p.mashape.com/search?key=" + key + "&q=" + ingredients_to_query,
                        headers={"X-Mashape-Key": "rjq7HBFHZTmshDawy37VfzQb0HNKp118a2Jjsnp4pTmBWsnAO7","Accept": "application/json"}).json()

def format_response_to_user(responses):
    """
    Formats recipes into response to user
    
    Arguments:
    responses: recipe responses from the recipes api

    Return:
    A MessagingResponse() object to be sent back to Twilio
    """
    # Start our TwiML response
    resp = MessagingResponse()
    # Determine the right reply for this message
    reply = ""
    if responses['count'] == 0:
        reply += "No results found"
    elif responses['count'] < 3:
        for response in range(1, len(responses) + 1):
            reply += "{}). ".format(response) + responses["recipes"][response]["title"] + " " +  responses["recipes"][response]["source_url"] + "\n"
    else:
        for response in range(1, 4):
            reply += "{}). ".format(response) + responses["recipes"][response]["title"] + " " +  responses["recipes"][response]["source_url"] + "\n"

    resp.message(reply)
    return(resp);

if __name__ == "__main__":
    app.run(debug=True)

