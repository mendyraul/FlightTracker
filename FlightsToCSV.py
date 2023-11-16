import requests
import csv

# Read API Key
with open('apikey.txt', 'r') as file:
    api_key = file.read().strip()

# API Endpoints for Departing and Arriving Flights
dep_iata = 'MIA'
dep_url = f'https://airlabs.co/api/v9/schedules?dep_iata={dep_iata}&api_key={api_key}'
arr_iata = 'MIA'
arr_url = f'https://airlabs.co/api/v9/schedules?arr_iata={arr_iata}&api_key={api_key}'

# Function to process API response
def process_flights(response):
    flights = []
    for schedule in response['response']:
        flight_info = {
            'airline_iata': schedule.get('airline_iata'),
            'flight_iata': schedule.get('flight_iata'),
            'status': schedule.get('status'),
            'dep_iata': schedule.get('dep_iata'),
            'dep_time': schedule.get('dep_time'),
            'dep_estimated': schedule.get('dep_estimated'),
            'dep_actual': schedule.get('dep_actual'),
            'arr_iata': schedule.get('arr_iata'),
            'arr_time': schedule.get('arr_time'),
            'arr_estimated': schedule.get('arr_estimated'),
            'arr_actual': schedule.get('arr_actual'),
            'dep_delayed': schedule.get('dep_delayed'),
            'arr_delayed': schedule.get('arr_delayed'),
            'duration': schedule.get('duration')
        }
        flights.append(flight_info)
    return flights


# Retrieve Departing Flights Data
dep_result = requests.get(dep_url)
if dep_result.status_code == 200:
    flights_dep = process_flights(dep_result.json())
else:
    print(f"Failed to retrieve departing flights. Status code: {dep_result.status_code}")
    print(dep_result.text)
    flights_dep = []

# Retrieve Arriving Flights Data
arr_result = requests.get(arr_url)
if arr_result.status_code == 200:
    flights_arr = process_flights(arr_result.json())
else:
    print(f"Failed to retrieve arriving flights. Status code: {arr_result.status_code}")
    print(arr_result.text)
    flights_arr = []

# Write to CSV file
with open('flights.csv', 'w', newline='') as csvfile:
    csv_columns = ['dep_iata', 'airline_iata', 'flight_iata', 'dep_time', 'dep_estimated', 'dep_actual',
                   'arr_iata', 'arr_time', 'arr_estimated', 'arr_actual', 'status', 'dep_delayed', 'arr_delayed']
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for flight_info in flights_dep + flights_arr:
        writer.writerow(flight_info)

# Initialize counters for different statuses
scheduled_count = 0
active_count = 0
cancelled_count = 0
landed_count = 0

# Update counters based on status
for flight_info in flights_dep + flights_arr:
    if flight_info['status'] == 'scheduled':
        scheduled_count += 1
    elif flight_info['status'] == 'active':
        active_count += 1
    elif flight_info['status'] == 'cancelled':
        cancelled_count += 1
    elif flight_info['status'] == 'landed':
        landed_count += 1

# Print summary
print(f"Total Number of Flights: {len(flights_dep + flights_arr)}")
print(f"Total Scheduled Flights: {scheduled_count}")
print(f"Total Active Flights: {active_count}")
print(f"Total Cancelled Flights: {cancelled_count}")
print(f"Total Landed Flights: {landed_count}")
