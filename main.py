import requests
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
    body = request.values.get('Body', None).lower();
    key = open("apikey.txt").read().replace("\n", "")
    ingredients_to_query = ""
    print(request.values)
    if (body == 'search'):
        user = db.users.find_one({'phone_number':user_number})
        ingredients = user['ingredients']
        for ingredients in ingredients:
            ingredients_to_query += ingredients + " "

        db.users.remove({"phone_number" : user_number});
    else:
        if (db.users.count({'phone_number':user_number}) == 0):
            db.users.insert({'phone_number':user_number, 'ingredients':[body]})
        else:
            result = db.users.update_one({'phone_number':user_number}, {"$push":{'ingredients':body}})


    response = requests.get("https://community-food2fork.p.mashape.com/search?key=" + key + "&q=" + ingredients_to_query,
        headers={
        "X-Mashape-Key": "rjq7HBFHZTmshDawy37VfzQb0HNKp118a2Jjsnp4pTmBWsnAO7",
        "Accept": "application/json"
        }).json()


    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    resp.message(response["recipes"][0]["title"] + " " +  response["recipes"][0]["source_url"])


    return str(resp)

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
