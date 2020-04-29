from flask import Flask ,render_template, request,redirect, url_for,flash,jsonify
app = Flask(__name__)
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/')
def restaurant():
	restaurant = session.query(Restaurant).all()
	return render_template('displayrestaurant.html', restaurant = restaurant)
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
	return render_template('menu.html', restaurant = restaurant, items = items)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
	return jsonify(MenuItems=[i.serialize for i in items])
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def restaurantMenuItemJSON(restaurant_id,menu_id):
	
	menuitem = session.query(MenuItem).filter_by(id = menu_id).one()
	return jsonify(MenuItem = menuitem.serialize)

@app.route('/restaurant/new/',methods=['GET','POST'])
def newRestaurant():
	if request.method == 'POST':
		newItem = Restaurant(name = request.form['name'])
		session.add(newItem)
		session.commit()
		flash("new menu item created!")
		return redirect(url_for('restaurant'))
	else:
		return render_template('newRestaurant.html')
@app.route('/restaurant/<int:restaurant_id>/new/',methods=['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'],restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		flash("new menu item created!")
		return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
	else:
		return render_template('newmenuitem.html',restaurant_id = restaurant_id)
@app.route('/restaurant/<int:restaurant_id>/edit/',methods=['GET','POST'])
def editRestaurantItem(restaurant_id):
	editedItem = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		session.add(editedItem)
		session.commit()
		flash("item has been edited")
		return redirect(url_for('restaurant',restaurant_id = restaurant_id))
	else:
		return render_template('editRestaurant.html',restaurant_id = restaurant_id,item =editedItem)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/',methods=['GET','POST'])
def editMenuItem(restaurant_id,menu_id):
	editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		session.add(editedItem)
		session.commit()
		flash("item has been edited")
		return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
	else:
		return render_template('editmenuitem.html',restaurant_id = restaurant_id, menu_id= menu_id ,item =editedItem)
	
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET','POST'])

def deleteRestaurant(restaurant_id):
    itemToDelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Item has been deleted")
        return redirect(url_for('restaurant', restaurant_id=restaurant_id))
    else:
        return render_template('deleteRestaurant.html',restaurant_id = restaurant_id,item=itemToDelete)
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Item has been deleted")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html',restaurant_id = restaurant_id, menu_id= menu_id , item=itemToDelete)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug =True
	app.run(host = '0.0.0.0', port = 5000)