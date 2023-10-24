from flask import Flask, render_template
import sqlite3
from flask_sqlalchemy import SQLAlchemy

with open('username', 'r') as file:
    username = file.read()
    
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + username + '@flight-tracker-402620:us-east4:flights'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(10), nullable=False)
    origin_destination = db.Column(db.String(50), nullable=False)
    departure_time = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    delay = db.Column(db.Integer, default=0)

# Create the database tables
db.create_all()

# Sample data
sample_flights = [
    {'flight_number': 'FL123', 'origin_destination': 'New York', 'departure_time': '2023-10-11 12:00', 'status': 'On Time', 'delay': 0},
    # Add more sample flights as needed
]

# Insert sample data into the database
for flight_data in sample_flights:
    flight = Flight(**flight_data)
    db.session.add(flight)

db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/flights')
def flights():
    flights = Flight.query.all()
    return render_template('flights.html', flights=flights)

if __name__ == '__main__':
    app.run(debug=True)
    app = flask(__name__)



 