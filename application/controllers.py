from flask import Flask, request, flash,url_for, redirect
from flask import render_template
from flask import current_app as app
from .forms import RegistrationForm,LoginForm, CreateVenueForm, CreateShowForm, UpdateShowForm, UpdateVenueForm, BookingForm
from main import bcrypt,db
from application.models import User,Venue, Show, Booking
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")

@app.route("/register",methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('login'))
    return render_template("register.html",title="Register",form=form)

@app.route("/admin-register",methods=["GET", "POST"])
def admin_register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password,isAdmin=True)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('admin_login'))
    return render_template("admin-register.html",title="Admin Register",form=form)


@app.route("/login",methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/admin-login",methods=["GET", "POST"])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if not user.isAdmin:
                flash('Login Unsuccessful. Not an admin', 'danger')
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route("/create-venue",methods=["GET","POST"])
@login_required
def create_venue():
    if not current_user.isAdmin:
        return redirect(url_for('admin_only'))
    form = CreateVenueForm()
    if form.validate_on_submit():
        venue = Venue(venue_name=form.venue_name.data,venue_address=form.venue_address.data,venue_capacity=form.venue_capacity.data)
        db.session.add(venue)
        db.session.commit()
        flash(f'Venue created {form.venue_name.data}!','success')
        return redirect(url_for('create_venue'))
    return render_template("create-venue.html",title="Create Venue",form=form)

@app.route('/venues/<int:venue_id>/update', methods=['GET', 'POST'])
@login_required
def update_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    if not current_user.isAdmin:
        return redirect(url_for('admin_only'))
    form = UpdateVenueForm()
    if form.validate_on_submit():
        venue.venue_name = form.venue_name.data
        venue.venue_address = form.venue_address.data
        venue.venue_capacity = form.venue_capacity.data
        db.session.commit()
        flash('The venue has been updated successfully!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.venue_name.data = venue.venue_name
        form.venue_address.data = venue.venue_address
        form.venue_capacity.data = venue.venue_capacity
    return render_template('update-venue.html', title='Update Venue', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/delete', methods=['GET'])
@login_required
def delete_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    if not current_user.isAdmin:
        return redirect(url_for('admin_only'))
    db.session.delete(venue)
    db.session.commit()
    flash(f'Venue {venue.venue_name} has been deleted.', 'success')
    return redirect(url_for('home'))

@app.route("/create-show",methods=["GET","POST"])
@login_required
def create_show():
    if not current_user.isAdmin:
        return redirect(url_for('admin_only'))
    form = CreateShowForm()
    if form.validate_on_submit():
        show = Show(show_name=form.show_name.data,venue_id=form.venue_id.data,show_rating=form.show_rating.data, show_ticket_price=form.show_ticket_price.data)
        db.session.add(show)
        db.session.commit()
        flash(f'Show created {form.show_name.data}!','success')
        return redirect(url_for('create_show'))
    return render_template("create-show.html",title="Create Show",form=form)

@app.route('/shows/<int:show_id>/update', methods=['GET', 'POST'])
@login_required
def update_show(show_id):
    show = Show.query.get_or_404(show_id)
    if not current_user.isAdmin:
        return redirect(url_for('admin_only'))
    form = UpdateShowForm()
    if form.validate_on_submit():
        show.venue_id = form.venue_id.data
        show.show_name = form.show_name.data
        show.show_rating = form.show_rating.data
        show.show_ticket_price = form.show_ticket_price.data
        db.session.commit()
        flash('The show information has been updated successfully!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.venue_id.data = show.venue_id
        form.show_name.data = show.show_name
        form.show_rating.data = show.show_rating
        form.show_ticket_price.data = show.show_ticket_price
    return render_template('update-show.html', title='Update Show', form=form, show=show)

@app.route('/shows/<int:show_id>/delete', methods=['GET'])
@login_required
def delete_show(show_id):
    show = Show.query.get_or_404(show_id)
    if not current_user.isAdmin:
        return redirect(url_for('admin_only'))
    db.session.delete(show)
    db.session.commit()
    flash(f'Show {show.show_name} has been deleted.', 'success')
    return redirect(url_for('home'))

@app.route("/admin-only-allowed",methods=["GET","POST"])
@login_required
def admin_only():
    return render_template("admin-only-allowed.html")

@app.route("/book-show",methods=["GET","POST"])
@login_required
def book_show():
    form = BookingForm()
    if form.validate_on_submit():
        show = Show.query.filter_by(show_id=form.show_id.data).first()
        venue = Venue.query.filter_by(venue_id = show.venue_id).first()
        no_of_tickets = form.quantity.data
        if no_of_tickets > venue.venue_capacity:
            flash('Show is housefull!', 'danger')
            return redirect(url_for('home'))
        venue.venue_capacity -= no_of_tickets
        booking = Booking(user_id=current_user.id,show_id=form.show_id.data, quantity=form.quantity.data)
        db.session.add(booking)
        db.session.commit()
        flash(f'Booking created {form.show_id.data} , {form.quantity}!','success')
        return redirect(url_for('book_show'))
    return render_template("book-show.html",title="Book Show",form=form)

@app.route("/profile",methods=["GET"])
@login_required
def profile():
    user = User.query.filter_by(email=current_user.email).first()
    bookingList = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template("profile.html",user=user,bookingList=bookingList)

@app.route("/admin-profile",methods=["GET"])
@login_required
def admin_profile():
    user = User.query.filter_by(email=current_user.email).first()
    if not current_user.isAdmin:
        return redirect(url_for('admin_only'))
    venueList = Venue.query.all()
    showList = Show.query.all()
    return render_template("admin-profile.html",user=user,venueList=venueList,showList=showList)


@app.route("/venue",methods=["GET"])
def venue():
    venueList = Venue.query.all()
    return render_template("venue.html",venueList=venueList)

@app.route("/show",methods=["GET"])
def show():
    showList = Show.query.all()
    return render_template("show.html",showList=showList)