from clarifai.rest import ClarifaiApp

clarafai_model_debug = False;

def determine_ingredient(photo):
    app = ClarifaiApp()
    model = app.models.get('food')
    response = model.predict_by_url(url=photo);

    concepts = response['outputs'][0]['data']['concepts']
    if (clarafai_model_debug == True):
        for concept in concepts:
            print(concept['name'], concept['value'])
        
    probableIngredient = concepts[0]['name'];
    return probableIngredient



