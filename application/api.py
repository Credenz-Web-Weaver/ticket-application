from flask import jsonify, request
from main import app, db
from models import User,Venue,Show,Booking

# USER CRUD APIs
# CREATE operation
@app.route('/api/users', methods=['POST'])
def api_create_user():
    data = request.get_json()
    user = User(username=data['username'], email=data['email'], password=data['password'], isAdmin=data['isAdmin'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!'})

# READ operation
@app.route('/api/users', methods=['GET'])
def api_get_all_users():
    users = User.query.all()
    user_data_object = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['isAdmin'] = user.isAdmin
        user_data_object.append(user_data)
    return jsonify({'users': user_data_object})

@app.route('/api/users/<int:user_id>', methods=['GET'])
def api_get_user(user_id):
    user = User.query.get_or_404(user_id)
    user_data = {}
    user_data['id'] = user.id
    user_data['username'] = user.username
    user_data['email'] = user.email
    user_data['password'] = user.password
    user_data['isAdmin'] = user.isAdmin
    return jsonify({'user': user_data})

# UPDATE operation
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def api_update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.username = data['username']
    user.email = data['email']
    user.password = data['password']
    user.isAdmin = data['isAdmin']
    db.session.commit()
    return jsonify({'message': 'User updated successfully!'})

# DELETE operation
@app.route('/users/<int:user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully!'})

# Venue CRUD operations
# To create a venue
@app.route('/api/venues', methods=['POST'])
def api_create_venue():
    data = request.get_json()
    venue = Venue(venue_name=data['venue_name'], venue_address=data['venue_address'], venue_capacity=data['venue_capacity'])
    db.session.add(venue)
    db.session.commit()
    return jsonify({'message': 'Venue created successfully!'})

# Return all venues
@app.route('/api/venues', methods=['GET'])
def api_get_all_venues():
    venues = Venue.query.all()
    venue_data_object = []
    for venue in venues:
        venue_data = {}
        venue_data['venue_id'] = venue.venue_id
        venue_data['venue_name'] = venue.venue_name
        venue_data['venue_address'] = venue.venue_address
        venue_data['venue_capacity'] = venue.venue_capacity
        venue_data_object.append(venue_data)
    return jsonify({'venues': venue_data_object})

@app.route('/api/venues/<int:venue_id>', methods=['GET'])
def api_get_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    venue_data = {}
    venue_data['venue_id'] = venue.venue_id
    venue_data['venue_name'] = venue.venue_name
    venue_data['venue_address'] = venue.venue_address
    venue_data['venue_capacity'] = venue.venue_capacity
    return jsonify({'venue': venue_data})

@app.route('/api/venues/<int:venue_id>', methods=['PUT'])
def api_update_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    data = request.get_json()
    venue.venue_name = data['venue_name']
    venue.venue_address = data['venue_address']
    venue.venue_capacity = data['venue_capacity']
    db.session.commit()
    return jsonify({'message': 'Venue updated successfully!'})

@app.route('/api/venues/<int:venue_id>', methods=['DELETE'])
def api_delete_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    db.session.delete(venue)
    db.session.commit()
    return jsonify({'message': 'Venue deleted successfully!'})

@app.route('/api/shows', methods=['POST'])
def api_create_show():
    data = request.get_json()
    show = Show(show_name=data['show_name'], venue_id=data['venue_id'], show_rating=data['show_rating'], show_ticket_price=data['show_ticket_price'])
    db.session.add(show)
    db.session.commit()
    return jsonify({'message': 'Show created successfully!'})

@app.route('/api/shows', methods=['GET'])
def api_get_all_shows():
    shows = Show.query.all()
    show_data_object = []
    for show in shows:
        show_data = {}
        show_data['show_id'] = show.show_id
        show_data['show_name'] = show.show_name
        show_data['venue_id'] = show.venue_id
        show_data['show_rating'] = show.show_rating
        show_data['show_ticket_price'] = show.show_ticket_price
        show_data_object.append(show_data)
    return jsonify({'shows': show_data_object})

@app.route('/api/shows/<int:show_id>', methods=['GET'])
def api_get_show(show_id):
    show = Show.query.get_or_404(show_id)
    show_data = {}
    show_data['show_id'] = show.show_id
    show_data['show_name'] = show.show_name
    show_data['venue_id'] = show.venue_id
    show_data['show_rating'] = show.show_rating
    show_data['show_ticket_price'] = show.show_ticket_price
    return jsonify({'show': show_data})

@app.route('api/shows/<int:show_id>', methods=['PUT'])
def api_update_show(show_id):
    show = Show.query.get_or_404(show_id)
    data = request.get_json()
    show.show_name = data['show_name']
    show.venue_id = data['venue_id']
    show.show_rating = data['show_rating']
    show.show_ticket_price = data['show_ticket_price']
    db.session.commit()
    return jsonify({'message': 'Show updated successfully!'})

@app.route('/api/shows/<int:show_id>', methods=['DELETE'])
def api_delete_show(show_id):
    show = Show.query.get_or_404(show_id)
    db.session.delete(show)
    db.session.commit()
    return jsonify({'message': 'Show deleted successfully!'})