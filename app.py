from flask import Flask, render_template
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import requests
import csv

app = Flask(__name__)
# with open('username', 'r') as file:
#     username = file.read()

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + username + '@flight-tracker-402620:us-east4:flights'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# class Flight(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     flight_number = db.Column(db.String(10), nullable=False)
#     origin_destination = db.Column(db.String(50), nullable=False)
#     departure_time = db.Column(db.String(20), nullable=False)
#     status = db.Column(db.String(20), nullable=False)
#     delay = db.Column(db.Integer, default=0)

# # Create the database tables
# db.create_all()

# # Insert sample data into the database
# for flight_data in sample_flights:
#     flight = Flight(**flight_data)
#     db.session.add(flight)

# db.session.commit()



class Flight:
    def __init__(self, dep_iata, airline_iata, flight_iata, dep_time, dep_estimated, dep_actual, arr_iata, arr_time, arr_estimated, arr_actual, status, dep_delayed, arr_delayed):
        self.dep_iata = dep_iata
        self.airline_iata = airline_iata
        self.flight_iata = flight_iata
        self.dep_time = dep_time
        self.dep_estimated = dep_estimated
        self.dep_actual = dep_actual
        self.arr_iata = arr_iata
        self.arr_time = arr_time
        self.arr_estimated = arr_estimated
        self.arr_actual = arr_actual
        self.status = status
        self.dep_delayed = dep_delayed
        self.arr_delayed = arr_delayed

def read_csv(file_path):
    flights = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            flight = Flight(
                dep_iata=row['dep_iata'],
                airline_iata=row['airline_iata'],
                flight_iata=row['flight_iata'],
                dep_time=row['dep_time'],
                dep_estimated=row['dep_estimated'],
                dep_actual=row['dep_actual'],
                arr_iata = row['arr_iata'],
                arr_time=row['arr_time'],
                arr_estimated=row['arr_estimated'],
                arr_actual=row['arr_actual'],
                status=row['status'],
                dep_delayed=row['dep_delayed'],
                arr_delayed=row['arr_delayed']
            )
            flights.append(flight)
    return flights

flight_data = read_csv('flights.csv')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/flights')
def flights():
    # flights = Flight.query.all()
    return render_template('flights.html', flights=flight_data)

if __name__ == '__main__':
    app.run(debug=True)
    

 