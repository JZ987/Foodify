import unirest

def returnRecipes(input):
    query = ""

    for item in input:
        query += item + ","

    query = query.lower().replace(" ","+").replace(",","%2C")
    key = open("apikey.txt").read().replace("\n", "")

    response = unirest.get("https://community-food2fork.p.mashape.com/search?key=" + key + "&q=" + query,
        headers={
        "X-Mashape-Key": "rjq7HBFHZTmshDawy37VfzQb0HNKp118a2Jjsnp4pTmBWsnAO7",
        "Accept": "application/json"
        }
    ).body

    recipes = {}

    for i in range(5):
        recipes[response["recipes"][i]["title"]] = response["recipes"][i]["source_url"]

#test case 
#       for i in range(5):
#       print recipes.popitem()
