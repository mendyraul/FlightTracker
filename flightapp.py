import requests
import csv

# Your API Key
with open('apikey.txt','r') as file:
    api_key = file.read().strip()

# Departure IATA code for MIA
dep_iata = 'MIA'

# API Endpoint
url = f'https://airlabs.co/api/v9/schedules?dep_iata={dep_iata}&api_key={api_key}'

# Send GET request
dep_result = requests.get(url)

# Check if the request was successful
if dep_result.status_code == 200:
    dep_data = dep_result.json()
    # Create a list to collect data for analysis
    flights_dep = []
    # Iterate through the flight schedules
    for schedule in dep_data['response']:
        # Extract relevant information
        flight_info = {
            'dep_iata' : schedule.get('dep_iata','N/A'),
            'airline_iata': schedule.get('airline_iata', 'N/A'),
            'flight_iata': schedule.get('flight_iata', 'N/A'),
            'dep_time': schedule.get('dep_time', 'N/A'),
            'dep_estimated': schedule.get('dep_estimated', 'N/A'),
            'dep_actual': schedule.get('dep_actual', 'N/A'),
            'arr_iata' : schedule.get('arr_iata', 'N/A'),
            'arr_time': schedule.get('arr_time', 'N/A'),
            'arr_estimated': schedule.get('arr_estimated', 'N/A'),
            'arr_actual': schedule.get('arr_actual', 'N/A'),
            'status': schedule.get('status', 'N/A'),
            'dep_delayed': schedule.get('dep_delayed', 'N/A'),
            'arr_delayed': schedule.get('arr_delayed', 'N/A')
        }
        # Append to list
        flights_dep.append(flight_info)
    with open('flights.csv', 'w', newline='') as csvfile:
        # Write to CSV file
        csv_columns = ['dep_iata','airline_iata', 'flight_iata', 'dep_time', 'dep_estimated', 'dep_actual',
                'arr_iata','arr_time', 'arr_estimated', 'arr_actual', 'status', 'dep_delayed', 'arr_delayed']
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        # Write header
        writer.writeheader()
        # Write data
        for flight_info in flights_dep:
            writer.writerow(flight_info)

    # Now, make a request for arriving flights
    arr_iata = 'MIA'  # Replace with the appropriate IATA code for arrivals
    arr_url = f'http://airlabs.co/api/v9/schedules?arr_iata={arr_iata}&api_key={api_key}'
    arr_result = requests.get(arr_url)
    # Check if the request for arriving flights was successful
    if arr_result.status_code == 200:
        arr_data = arr_result.json()
        # Create a list to collect data for analysis
        flights_arr = []
        # Iterate through the flight schedules
        for schedule in arr_data['response']:
            # Extract relevant information
            flight_info = {
                'dep_iata' : schedule.get('dep_iata','N/A'),
                'airline_iata': schedule.get('airline_iata', 'N/A'),
                'flight_iata': schedule.get('flight_iata', 'N/A'),
                'dep_time': schedule.get('dep_time', 'N/A'),
                'dep_estimated': schedule.get('dep_estimated', 'N/A'),
                'dep_actual': schedule.get('dep_actual', 'N/A'),
                'arr_iata' : schedule.get('arr_iata', 'N/A'),
                'arr_time': schedule.get('arr_time', 'N/A'),
                'arr_estimated': schedule.get('arr_estimated', 'N/A'),
                'arr_actual': schedule.get('arr_actual', 'N/A'),
                'status': schedule.get('status', 'N/A'),
                'dep_delayed': schedule.get('dep_delayed', 'N/A'),
                'arr_delayed': schedule.get('arr_delayed', 'N/A')
            }
            # Append to list
            flights_arr.append(flight_info)
            # Save arriving flights CSV data to a file
                # Write to CSV file
        with open('flights.csv', 'a', newline='') as csvfile:
            csv_columns = ['dep_iata','airline_iata', 'flight_iata', 'dep_time', 'dep_estimated', 'dep_actual',
                    'arr_iata','arr_time', 'arr_estimated', 'arr_actual', 'status', 'dep_delayed', 'arr_delayed']
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            # Write header
            writer.writeheader()
            # Write data
            for flight_info in flights_arr:
                writer.writerow(flight_info)
            print("Arriving flights CSV data has been saved.")
    else:
        print(f"Failed to retrieve arriving flights. Status code: {arr_result.status_code}")
        print(arr_result.text)  
else:
    print(f"Failed to retrieve departing flights. Status code: {dep_result.status_code}")
    print(dep_result.text)  


# Initialize counters for different statuses
scheduled_count = 0
active_count = 0
cancelled_count = 0
landed_count = 0



# Update counters based on status
if flight_info['status'] == 'scheduled':
    scheduled_count += 1
elif flight_info['status'] == 'active':
    active_count += 1
elif flight_info['status'] == 'cancelled':
    cancelled_count += 1
elif flight_info['status'] == 'landed':
    landed_count += 1




# Print the length of flights_data
print(f"Total Number of Flights: {len(flights_arr + flights_dep)}")
print(f"Total Scheduled Flights: {scheduled_count}")
print(f"Total Active Flights: {active_count}")
print(f"Total Cancelled Flights: {cancelled_count}")
print(f"Total Landed Flights: {landed_count}")




