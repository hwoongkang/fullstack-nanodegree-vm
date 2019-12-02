from flask import Flask, render_template, url_for, redirect, request, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menuItems = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)

    return render_template("menu.html", restaurant=restaurant, items=menuItems)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        newName = request.form['name']
        menuItem.name = newName
        session.add(menuItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        print("here")
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, item=menuItem)

# Task 3: Create a route for deleteMenuItem function here


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant)\
        .filter_by(id=restaurant_id).one()
    menuItem = session.query(MenuItem)\
        .filter_by(id=menu_id).one()
    if request.method == 'POST':

        session.delete(menuItem)

        session.commit()

        return redirect(url_for('restaurantMenu', restaurant_id=restaurant.id))

    else:
        return render_template('deletemenuitem.html', restaurant_id=restaurant.id, item=menuItem)


if __name__ == '__main__':
    app.secret_key = 'super_sceret_here'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
