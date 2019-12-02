from flask import Flask, render_template
# * for database manipulations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(engine)
session = DBSession()


app = Flask(__name__)

#@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurants = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(\
        restaurant_id = restaurant_id)
    
    output = ''
    for item in items:
        output += item.name + '</br>'
        output += item.price + '</br>'
        output += item.description + '</br>'
        output += '</br>'


@app.route('/')
@app.route('/restaurant')
def viewAll():
    '''
    restaurants = session.query(Restaurant).all()
    output = ''
    for item in restaurants:
        output += item.name + "</br>"
    '''
    menuItems = session.query(MenuItem).all()
    output = ''
    for item in menuItems:
        output += item.name + "</br>"
        output += item.price + "</br>"
        output += item.description + "</br></br>"
    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host ='0.0.0.0',port = 5000)