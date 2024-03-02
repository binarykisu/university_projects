# Importing the necessary libraries
from flask import Flask, request
from flask_restful import Api, Resource
from datetime import datetime

# Initializing API
app = Flask(__name__)
api = Api(app)

def calculate_delivery_fee(cart_value:int, delivery_dist:int, num_items:int, time:str):
  """This function calculates the delivery fee.
  Returns the fee in JSON format."""
  delivery_fee = 0 
  surcharge = 0
  
  # Delivery fee requirements:
  # Cart value over 200€ = 0€ delivery fee
  if cart_value < 20000:  
    
    # Is delivery at least 10€?
    if cart_value < 1000:
      surcharge = 1000 - cart_value
      delivery_fee += surcharge
      
    # Is delivery distance > 1000m?
    if delivery_dist <= 1000:
      delivery_fee += 200
    else:
      extra = ((delivery_dist - 1000) // 500) + 1
      delivery_fee += (2 + extra)*100 
    
    # Are there 5 or more items?
    if num_items >= 5:
      surcharge = ((num_items - 4) * 50)
      if num_items > 12:
        surcharge += 120
      delivery_fee += surcharge
    
    # Is the time Friday 15:00-19:00 UTC?
    if time.weekday() == 4: #0=Monday-6=Sunday (4=Friday)
      if time.hour >= 15 and time.hour < 19:
        delivery_fee *= 1.2
    
    # Is the total delivery fee over 15€?
    if delivery_fee >= 1500:
      delivery_fee = 1500
  
  # Returning to post method (in JSON format)
  return {"delivery_fee": int(delivery_fee)}

def check_values(cart_value:int, delivery_dist:int, num_items:int, time:str):
  """This function checks for errors. Returns delivery info if no errors."""
  try:
    # Checking for all positive integers
    if not all(type(value) == int and value > 0 for value in [cart_value, delivery_dist, num_items]):
      raise ValueError
  
  except ValueError:
    raise ValueError("Cart value, delivery distance, and number of items must be positive integers.")  
  
  try:  
    # Turning the delivery time into a datetime object
    # Checking for correct time format
    time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")

  except ValueError:
    raise ValueError("Invalid time format. Use YYYY-MM-DDTHH:MM:SSZ.")   
  
  # If no errors
  return cart_value, delivery_dist, num_items, time

# Creating a resource that handles delivery info
class Calculator(Resource):
  def post(self):
    # Getting delivery_info from test.py
    delivery_info = request.get_json()
    
    # Extracting and defining the info
    cart_value = delivery_info.get("cart_value")
    delivery_dist = delivery_info.get("delivery_distance")
    num_items = delivery_info.get("number_of_items")
    time = delivery_info.get("time")
    
    # Performing error and formatting checks on the values before calculating the delivery fee
    cart_value, delivery_dist, num_items, time = check_values(cart_value, delivery_dist, num_items, time)
    
    # Calling the function to calculate fees
    delivery_fee = calculate_delivery_fee(cart_value, delivery_dist, num_items, time)
    
    # Returning the delivery fee back to the user
    return delivery_fee
  
# Registering the resource
api.add_resource(Calculator, "/delivery")

# Starting the Flask server (in debug mode)
if __name__ == "__main__":
  app.run(debug=True)