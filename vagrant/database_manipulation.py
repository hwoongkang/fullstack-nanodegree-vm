from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(engine)

session = DBSession()
myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()
print(session.query(Restaurant).all())

cheesepizza = MenuItem(name = "Cheese Pizza", price = "$8.99",description = "tasty",course = "Entree", restaurant = myFirstRestaurant)
session.add(cheesepizza)
session.commit()
print(session.query(MenuItem).all())