import requests
from clarifai_request import *
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient()
db = client.test

@app.route("/", methods=['GET', 'POST'])


def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    user_number = request.values.get('From', None)
    body = request.values.get('Body', None).lower().strip();
    media_url = request.values.get('MediaUrl0', None);
    key = open("apikey.txt").read().replace("\n", "")
    ingredients_to_query = ""
    print(request.values)
    if (body == 'search'): #user request a search using the ingredients they have inputed
        user = db.users.find_one({'phone_number':user_number})
        ingredients = user['ingredients']
        for ingredients in ingredients:
            ingredients_to_query += ingredients + " "

        responses = requests.get("https://community-food2fork.p.mashape.com/search?key=" + key + "&q=" + ingredients_to_query,
                            headers={
                            "X-Mashape-Key": "rjq7HBFHZTmshDawy37VfzQb0HNKp118a2Jjsnp4pTmBWsnAO7",
                            "Accept": "application/json"
                            }).json()


        # Start our TwiML response
        resp = MessagingResponse()
        print(responses)
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

        db.users.remove({"phone_number" : user_number});

        return str(resp)

    #
    #db.users.insert({'phone_number':user_number, 'ingredients':[body]})
    #print("determined_ingredient:" + ingredient)

    if (media_url != None):
        ingredient = determine_ingredient(media_url)
    else:
        ingredient = body

    if (db.users.count({'phone_number':user_number}) == 0):
        db.users.insert({'phone_number':user_number, 'ingredients':[ingredient]})
    else:
        result = db.users.update_one({'phone_number':user_number}, {"$push":{'ingredients':ingredient}})


    return("hello");





def request_recipe():
    response = requests.get("https://community-food2fork.p.mashape.com/search?key=" + key + "&q=" + body,
        headers={
        "X-Mashape-Key": "rjq7HBFHZTmshDawy37VfzQb0HNKp118a2Jjsnp4pTmBWsnAO7",
        "Accept": "application/json"
        }
    ).json()






if __name__ == "__main__":
    app.run(debug=True)

# def returnRecipes(input):
#     query = ""
#
#     for item in input:
#         query += item + ","
#
#     query = query.lower().replace(" ","+").replace(",","%2C")
#     key = open("apikey.txt").read().replace("\n", "")
#
#     response = requests.get("https://community-food2fork.p.mashape.com/search?key=" + key + "&q=" + query,
#         headers={
#         "X-Mashape-Key": "rjq7HBFHZTmshDawy37VfzQb0HNKp118a2Jjsnp4pTmBWsnAO7",
#         "Accept": "application/json"
#         }
#     ).body
#
#     return recipes[response["recipes"][i]["title"]] + " " +  response["recipes"][i]["source_url"]

# def returnRecipes(input):
#     query = ""
#
#     for item in input:
#         query += item + ","
#
#     query = query.lower().replace(" ","+").replace(",","%2C")
#     key = open("apikey.txt").read().replace("\n", "")
_#
#     response = requests.get("https://community-food2fork.p.mashape.com/search?key=" + key + "&q=" + query,
#         headers={
#         "X-Mashape-Key": "rjq7HBFHZTmshDawy37VfzQb0HNKp118a2Jjsnp4pTmBWsnAO7",
#         "Accept": "application/json"
#         }
#     ).body
#
#     return recipes[response["recipes"][i]["title"]] + " " +  response["recipes"][i]["source_url"]
    # recipes = {}
    #
    # for i in range(5):
    #     recipes[response["recipes"][i]["title"]] = response["recipes"][i]["source_url"]
    #
    # return recipes

#test case
#       for i in range(5):
#       print recipes.popitem()
