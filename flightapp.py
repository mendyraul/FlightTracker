import requests

# Your API Key
api_key = '2f222ffa-6ceb-4261-ae17-4369ebca0eca'

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

        # Update counters based on status
        if flight_info['status'] == 'scheduled':
            scheduled_count += 1
        elif flight_info['status'] == 'active':
            active_count += 1
        elif flight_info['status'] == 'cancelled':
            cancelled_count += 1
        elif flight_info['status'] == 'landed':
            landed_count += 1
        
        # Append to list
        flights_data.append(flight_info)
        
        # For demonstration, print extracted data
        print(f"Airline: {flight_info['airline_iata']}, Flight: {flight_info['flight_iata']}")
        print(f"Departure Time: {flight_info['dep_time']}, Estimated: {flight_info['dep_estimated']}, Actual: {flight_info['dep_actual']}")
        print(f"Arrival Time: {flight_info['arr_time']}, Estimated: {flight_info['arr_estimated']}, Actual: {flight_info['arr_actual']}")
        print(f"Status: {flight_info['status']}")
        print(f"Departure Delay: {flight_info['dep_delayed']}")
        print(f"Arrival Delay: {flight_info['arr_delayed']}")
        print("=" * 50)

        # Print the length of flights_data
    print(f"Total Number of Flights: {len(flights_data)}")
    print(f"Total Scheduled Flights: {scheduled_count}")
    print(f"Total Active Flights: {active_count}")
    print(f"Total Cancelled Flights: {cancelled_count}")
    print(f"Total Landed Flights: {landed_count}")

else:
    print(f"Failed to retrieve flight schedules. Status code: {response.status_code}")
