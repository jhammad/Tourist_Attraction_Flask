from flask import Flask, render_template, request, redirect, url_for
from locations import Locations
from forms import AddLocationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_PROJECT'

visit = Locations()
categories = {"recommended": "Recommended", "tovisit": "Places To Go", "visited": "Visited!!!", }

UP_ACTION = "Move"
DEL_ACTION = "Delete"

@app.route("/<category>", methods=["GET", "POST"])
def locations(category):
  locations = visit.get_list_by_category(category)
  ## Check the request for form data and process
  if request.method == "POST":    
    # We grab the form data from the request object including the hidden tags
    data_from_the_form = request.form.items()
    # make a list with the data form
    list_from_the_form = list(
      item for item in data_from_the_form
    )
    # Extract the tuple with the name and action from the list (secind element of the list)
    name_and_action_list = list_from_the_form[1]
    print(name_and_action_list)
    # Assign the values of the tuple name and action to the values of the new tuple from the form
    (name, action) = name_and_action_list
    print(name)
    print(action)
    if action == UP_ACTION:
      visit.moveup(name)
    elif action == DEL_ACTION:
      visit.delete(name)
  ## Return the main template with variables
  return render_template("locations.html", category=category, categories=categories, locations=locations, add_location=AddLocationForm())

@app.route("/add_location", methods=["POST"])
def add_location():
  ## Validate and collect the form data
  add_form = AddLocationForm()
  if add_form.validate_on_submit():
      name=add_form.name.data
      description=add_form.description.data
      category=add_form.category.data
      visit.add(name, description, category)      

  ## Redirect to locations route function
  return redirect(url_for("locations", category=category, _external=True, _scheme="https"))

@app.route("/")
def index():

  ## Redirect to locations route function
  return redirect(url_for("locations", category="recommended", _external=True, _scheme="https"))
