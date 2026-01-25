import requests
import json

# API endpoint URL
API_URL = 'http://localhost:3000/acft-data'  # will have to adjust depending on the server's port

try:
    response = requests.get(API_URL)

    # Check for successful response (status code 200)
    response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)

    # Parse the JSON response
    data = response.json()

    # Print the data (for verification)
    print("Aircraft Data:")
    print(json.dumps(data, indent=4)) # Pretty print the JSON for readability

    # Now you can use the 'data' variable in your Python code
    # For example, you could iterate through the aircraft list:
    # for aircraft in data:
    #     print(aircraft['icao24']) #Accessing a specific field

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")

# Note: Ensure that the Node.js server is running before executing this script.