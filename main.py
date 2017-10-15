import requests
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])

def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    key = open("apikey.txt").read().replace("\n", "")
    if body == None:
        body = "chicken"
    response = requests.get("https://community-food2fork.p.mashape.com/search?key=" + key + "&q=" + body,
        headers={
        "X-Mashape-Key": "rjq7HBFHZTmshDawy37VfzQb0HNKp118a2Jjsnp4pTmBWsnAO7",
        "Accept": "application/json"
        }
    ).json()
    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    resp.message(response["recipes"][0]["title"] + " " +  response["recipes"][0]["source_url"])

    return str(resp)

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
#
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
