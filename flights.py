import os
import requests
import psycopg2
from psycopg2 import sql

# Your API Key
with open('apikey.txt','r') as file:
    api_key = file.read().strip()

# Departure IATA code for MIA
dep_iata = 'MIA'

# API Endpoint
url = f'https://airlabs.co/api/v9/schedules?dep_iata={dep_iata}&api_key={api_key}'

# Send GET request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Database connection parameters
    db_params = {
        'dbname': 'dbFlights',
        'user': 'flights',
        'password': 'Balls123!',
        'host': '34.86.115.0',
        'port': '5432',
    }
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # SQL query to create the table
    create_table_query = """
        CREATE TABLE IF NOT EXISTS flight_schedule (
            id SERIAL PRIMARY KEY,
            airline_iata VARCHAR(5),
            flight_iata VARCHAR(10),
            dep_time TIMESTAMP,
            dep_estimated TIMESTAMP,
            dep_actual TIMESTAMP,
            arr_time TIMESTAMP,
            arr_estimated TIMESTAMP,
            arr_actual TIMESTAMP,
            status VARCHAR(20),
            dep_delayed INTEGER,
            arr_delayed INTEGER
        )
    """

    # Execute the table creation query
    cursor.execute(create_table_query)

    insert_query = sql.SQL("""
        INSERT INTO flight_schedule (
            airline_iata, flight_iata, dep_time, dep_estimated, dep_actual,
            arr_time, arr_estimated, arr_actual, status, dep_delayed, arr_delayed
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """)
    # Create a list to collect data for analysis
    flights_data = []

    # Initialize counters for different statuses
    scheduled_count = 0
    active_count = 0
    cancelled_count = 0
    landed_count = 0
    
    # Iterate through the flight schedules
    for schedule in data['response']:
        # Extract relevant information
        flight_info = {
            'airline_iata': schedule.get('airline_iata', 'N/A'),
            'flight_iata': schedule.get('flight_iata', 'N/A'),
            'dep_time': schedule.get('dep_time', 'N/A'),
            'dep_estimated': schedule.get('dep_estimated', 'N/A'),
            'dep_actual': schedule.get('dep_actual', 'N/A'),
            'arr_time': schedule.get('arr_time', 'N/A'),
            'arr_estimated': schedule.get('arr_estimated', 'N/A'),
            'arr_actual': schedule.get('arr_actual', 'N/A'),
            'status': schedule.get('status', 'N/A'),
            'dep_delayed': schedule.get('dep_delayed', 'N/A'),
            'arr_delayed': schedule.get('arr_delayed', 'N/A')
        }
        cursor.execute(insert_query, flight_info)

        
        # Append to list
        flights_data.append(flight_info)
        


    # Commit the changes to the database
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()


else:
    print(f"Failed to retrieve flight schedules. Status code: {response.status_code}")