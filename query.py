import requests
import json
from flask import Flask, render_template, request, session
import ast
import numpy
import validate

firstdrink = ""
mixer = ""
index = 0
################################################################################################################################
###############################################CLASSES##########################################################################
################################################################################################################################
#this is the query class that allows us to instantiate a query object and query with the string
class genericQuery:
    initialQuery = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?i="
    ingredient = ""
    finalQuery = ""

    def __init__(self, ingredientString):
        self.ingredient = ingredientString
        self.finalQuery = self.initialQuery + self.ingredient

    def queryData(self):
        requestData = requests.get(self.finalQuery)
        requestJson = requestData.json()
        # session.clear()
        return requestJson;

#this queries based on the drink name and then returns the list of ingredients
class nameQuery:
    initialQuery = "https://www.thecocktaildb.com/api/json/v1/1/search.php?s="
    cocktailName = ""
    finalQuery = ""

    def __init__(self, cocktail):
        self.cocktailName = cocktail
        self.finalQuery = self.initialQuery + self.cocktailName

    def queryData(self):
        requestData = requests.get(self.finalQuery)
        requestJson = requestData.json()
        return requestJson;

################################################################################################################################
################################################################################################################################
################################################################################################################################

app = Flask(__name__)
@app.route('/')
def index():
   return render_template('init.html')

################################################################################################################################
################################################################################################################################
################################################################################################################################

@app.route('/', methods=['GET', 'POST'])
def my_form_post():
    #sets variables equal to those in the html form, need to find a better way to handle these arguments
    firstdrink = request.form['firstdrink']
    mixer = request.form['mixer']

    #instantiate query objects with the dropdown names
    firstIngredient = genericQuery(firstdrink)
    secondIngredient = genericQuery(mixer)

    #query data into alcohol and mixing variables
    alcohol = firstIngredient.queryData()
    mixing = secondIngredient.queryData()

    # Testing validity of queried data
    # validate.validateGenericDrink(firstdrink, alcohol)
    # validate.validateGenericDrink(mixer, mixing)

    listofIngredients = []
    listOfDrinkNames = []
    drinkImages = []

    # This is the intersection between the common elements between the alcohol and mixer queries
    intersection = [x for x in alcohol["drinks"] if x in mixing["drinks"]]
    index = len(intersection)-1
    #loop through and get all the names of the drinks
    while(index >= 0):
        listOfDrinkNames.append(intersection[index]["strDrink"])
        drinkImages.append(intersection[index]["strDrinkThumb"])
        index = index -1
    index = len(intersection)-1

    return render_template('init.html', value=json.dumps(drinkImages), names=json.dumps(listOfDrinkNames), length=index)
    # return render_template('test.html', value=listOfDrinkNames)
    # return render_template('test.html', value=drinkImages)
    # return render_template('test.html', value=alcohol)
    # return render_template('test.html', value=mixing)



################################################################################################################################
################################################################################################################################
################################################################################################################################

@app.route('/getIngredient', methods=['GET', 'POST'])
def ingredient():
    if request.method == 'POST':
        cocktailNumber = request.form['cocktail']
        cocktailNumber = cocktailNumber.replace('****', ' ')
        # cocktailNumber = int(cocktailNumber)
        ingredientsData = None
        ingredients = []
        index = 0
        keys = []
        values = []
        ingredientsDataObject = nameQuery(cocktailNumber)
        ingredientsData = ingredientsDataObject.queryData()
        #here we want to grab all the ingredients
        ingredients = [x for x in ingredientsData["drinks"]]

        for key, value in ingredients[0].items():
            keys.append(key)
            values.append(value)

        ingredients = []
        measurements = []
        instructions = ''

        index = len(keys)-1
        while(index >= 0):
            if("strIngredient" in keys[index]):
                ingredients.append(values[index])
            if("strMeasure" in keys[index]):
                measurements.append(values[index])
            if("Instructions" in keys[index]):
                instructions = values[index]
            index = index - 1
        index = len(ingredients)-1
    return render_template('test.html', instructions=instructions, ingredients=ingredients, measurements=measurements, nameofdrink=cocktailNumber, num=index)

################################################################################################################################
################################################################################################################################
################################################################################################################################

if __name__ == '__main__':
   app.run(debug=True)
