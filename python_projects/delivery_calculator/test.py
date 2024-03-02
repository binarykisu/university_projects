import requests

# Test server from Flask
url = "http://127.0.0.1:5000/"

# Request payload from user
delivery_info = {
                 "cart_value": 790, 
                 "delivery_distance": 2235,
                 "number_of_items": 13, 
                 "time": "2024-01-19T16:00:00Z"
                 }

# Sending a HTTP POST request to 'http://127.0.0.1:5000/delivery'
response = requests.post(url + "delivery", json=delivery_info)
print(response.json())