# Foodify

Usually, the hardest thing about cooking is figuring out what you want to make. At the grocery store or at home, you're provided with many ingredients but have no idea what to do with them.
Because of this, we developed Foodify, a chat bot that receives inputs that are either strings or images and uses that information to generate recipes through the ingredients that you've chosen.

## How it Works

Through the use of Twilio, we were able to receive inputs from the user through text. The user would text the chat bot images of ingredients or names of ingredients.
The ingredients would then be processed through Clarifai's api and return the names of the ingredients that were given to it. After the ingredient names were determined,
using the food2fork api we received the top 3 results for recipes that include all the ingredients mentioned.
The information is then processed and a text message with the name of the recipe and the url is sent to the user.

## Built With
* [Twilio](https://www.twilio.com/sms/api) - Enabled two-way communication between app and user
* [Flask](http://flask.pocoo.org/) - Used to host application, faciliatate communication between APIs and parse data.
* [Clarifai](https://www.clarifai.com/) - Used custom model trained to recognize ingredients
* [Food2Fork](https://food2fork.com/about/api) - Used to lookup recipes based on ingredients
* [MongoDB](https://www.mongodb.com) - Database to store user data
