from flask import Flask, render_template, request, redirect, url_for
import json
import xml.etree.ElementTree as ET

#saved configuration
CONFIG_FILE = "config.json"

#allowable color options
COLOR_LIST = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]


#Button class
class Button:
    def __init__(self, name, color, xml_element, status = 0):
        self.status = status
        self.name = name
        self.color = color
        self.xml_element = xml_element


#load function
def loadConfig():
    global button_list
    try:
        with open(CONFIG_FILE, "r") as jsonFile:

            #decodes dictionary back into Button object from the json file
            button_list = [Button(**button) for button in json.load(jsonFile)]

    except (json.decoder.JSONDecodeError, FileNotFoundError) as e:

        #handle error
        print(f"CONFIG File Error: {e}")

        #if no json file found create empty list
        button_list = []

    return button_list


#sets list based on json data
button_list = loadConfig()


#Define variable as a Flask class
dashApp = Flask(__name__)


#---------------------------------------------- XML HANDLING ----------------------------------------------
#Elements will be sub of dashRoot

def toXML():
    global button_list

    #Define variable as root element
    dashRoot = ET.Element("info")
    
    for button in button_list:
        buttonElement = ET.SubElement(dashRoot, button.xml_element)
        buttonElement.text = str(button.status)

        newTree = ET.ElementTree(dashRoot)
        newTree.write("dash.xml")

#---------------------------------------------------------------------------------------------------------

#---------------------------------------------- HTML HANDLING --------------------------------------------
#GET = Server ---> HTML
#POST = HTML ---> Server
#Decorator so that when user accesses the base url, the index() function is run
#Says the HTTP methodds GET and POST will be used
        
@dashApp.route("/", methods = ["GET", "POST"])
def index():

    global button_list

    if request.method == "POST":

        for button in button_list:

            if button.name in request.form:

                button.status = int(request.form[button.name])

    #overwrites XML           
    toXML()

    return render_template("main.html", button_list = button_list)


#same as index decorator, but for config page
@dashApp.route("/config", methods = ["GET", "POST"])
def configure():

    #explicitly says we are using the global button_list variable
    global button_list
    global COLOR_LIST

    if request.method == "POST":

        #Get form data from webpage
        button_name = request.form.get("button_name")
        button_color = request.form.get("button_color")
        xml_element = request.form.get("xml_element")

        #get user inputted name of dash
        dashName = request.form.get("dashName")

        #set an instance of Button class using received form data
        new_button = Button(button_name, button_color, xml_element)
        new_button.status = 0

        #add object to buttons list
        button_list.append(new_button)

        #update json
        saveConfig()

    return render_template("config.html", button_list = button_list, COLOR_LIST = COLOR_LIST)


@dashApp.route("/remove", methods = ["POST"])
def remove():
    global button_list

    if request.method == "POST":

        to_remove_name = request.form.get("remove")
        #overwrites button_list with only objects in which .name doesn't match the remove name
        button_list = [button for button in button_list if button.name != to_remove_name]

        #update json
        saveConfig()

    #refresh page
    return redirect(url_for("configure"))        

#---------------------------------------------------------------------------------------------------------


#save function
def saveConfig():
    global button_list

    with open(CONFIG_FILE, "w") as jsonFile:

        #converts button object into a dictionary, then dumps to our json file
        json.dump([button.__dict__ for button in button_list], jsonFile)

#ensures script only runs when triggered directly
if __name__ == "__main__":

    #flask debug (debug = True)
    dashApp.run()