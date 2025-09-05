from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from models import db, House, Users, Booking

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///house.db'
app.config['SECRET_KEY'] = 'secret_key1234'
db.init_app(app)

@app.route('/')
def index():
    houses = House.query.all()
    return render_template('index.html', houses=houses)

@app.route('/house/<int:house_id>')
def house_details(house_id):
    house = House.query.get_or_404(house_id)
    return render_template('house_details.html', house=house)

@app.route('/book/<int:house_id>', methods=['GET', 'POST'])
def book_house(house_id):
    house = House.query.get_or_404(house_id)
    if request.method == 'POST':
        price = request.form['price']
        reservation = request.form['reservation']
        reservation_time = request.form['reservation_time']
        user_id = request.form['user_id']
        booking = Booking(price=price, reservation=reservation, reservation_time=reservation_time, user_id=user_id, house_id=house.id)
        db.session.add(booking)
        db.session.commit()
        flash('Booking successful!', 'success')
        return redirect(url_for('index'))
    return render_template('book.html', house=house)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = Users(username=username, email=email, phone=phone, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('User registered successfully!', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            flash('Error occurred while registering user.', 'danger')

    return render_template('registration.html')

@app.route('/information')
def information():
    users = Users.query.all()
    houses = House.query.all()
    bookings = Booking.query.all()
    return render_template('information.html', users=users, houses=houses, bookings=bookings)

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Create users
        user1 = Users(username='john_doe', email='john@example.com', phone='1234567890', password=generate_password_hash('password', method='pbkdf2:sha256'))
        user2 = Users(username='jane_doe', email='jane@example.com', phone='0987654321', password=generate_password_hash('password', method='pbkdf2:sha256'))
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        # Create houses
        house1 = House(country='USA', city='New York', type='Apartment', price=500000, size=80, rooms=2, description='A cozy apartment in NYC.', image_url='images/house1.jpg', owner_id=user1.id)
        house2 = House(country='France', city='Paris', type='Condo', price=750000, size=120, rooms=3, description='A luxurious condo in Paris.', image_url='images/house2.jpg', owner_id=user2.id)
        house3 = House(country='Canada', city='Toronto', type='Family House', price=650000, size=150, rooms=4, description='A spacious family house in Toronto.', image_url='images/house3.jpg', owner_id=user1.id)
        house4 = House(country='Italy', city='Rome', type='Villa', price=1200000, size=200, rooms=5, description='A beautiful villa in Rome.', image_url='images/house4.jpg', owner_id=user2.id)
        house5 = House(country='Australia', city='Sydney', type='Beach House', price=900000, size=160, rooms=3, description='A stunning beach house in Sydney.', image_url='images/house5.jpg', owner_id=user1.id)

        db.session.add(house1)
        db.session.add(house2)
        db.session.add(house3)
        db.session.add(house4)
        db.session.add(house5)
        db.session.commit()
    app.run(debug=True)
