# NOTE: I worked with my TA, Jay Yu, on this homework during a joint homework help session on April 9, 2021. 

from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
from scrape_mars import mars_scrape

# Create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# Route to render index.html
@app.route('/')
def index():
    mars = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars_html=mars)

# Route that will trigger the scrape function
@app.route('/scrape_mars')
def scrape():

    # Run the scrape function
    mars = mongo.db.mars
    mars_data = mars_scrape()

    # Update the Mongo database using update and upsert=True
    mars.update({}, mars_data, upsert=True)

    # Redirect to the index 
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
