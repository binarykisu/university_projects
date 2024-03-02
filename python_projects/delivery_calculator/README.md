# Delivery Fee Calculator

## Introduction

For this assignment, the task was to write a delivery fee calculator which can be used when a customer orders from a restaurant online and needs to know how much their delivery fee will cost. In particular, this code uses an HTTP API (with a single POST endpoint) to calculate the delivery fee based on factors such as the the cart value, number of items in the cart, time of the order, and delivery distance. It then returns the calculated delivery fee in the response payload (in JSON format). 

## Requirements & Setup

First, be sure to download Python and have your text editor of choice pulled up. To download the necessary Python libraries that are used in this code, make sure you have created a virtual environment for your workspace! I personally enjoy working with Visual Studio Code, but here is a [helpful video](https://youtu.be/IAvAlS0CuxI?si=Mr8fw0p2Ydv69kdv) for creating a virtual environment if you are using something different. 

Next, use the ```pip install``` command and install the following libraries:
- Flask
- Flask-RESTful
- requests

There are plenty of other useful libraries to install when working with Flask, but this is all that was used for this assignment. Now your computer should be ready to run the delivery calculator! :partying_face:

## Running the code

The file _calculator.py_ contains the main Flask API, and the other file _test.py_ is for running the tests. Start by running the _calculator.py_ file to initialize the Flask server. In the _test.py_ file, ensure that the HTTP link written for the ```url``` variable matches the HTTP given to you in the terminal by Flask after the server is initialized. It should say something like:
> *Running on http://127.0.0.1:5000/

Then, in another terminal, simply run the test file with the command ```python3 test.py``` (or just use ```python test.py``` for Windows).

### Functions

The code consists of a Calculator resource, where the data from the request payload is sorted and sent to the ```check_values``` function to ensure that everything is formatted correctly. If this is the case, the data then gets sent to the ```calculate_delivery_fee``` function to perform the delivery fee calculations.

You can make changes to the values in the ```delivery_info``` variable in _test.py_ to get different results for the delivery cost. Note that each time a change is made, you will probably have to run the test file again so the server can refresh with the new data. The response will show up in JSON format in a separate terminal (the one that is not running the Flask server). As an example, if the user request looks like this: 

```
{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 13, "time": "2024-01-19T16:00:00Z"}
```
The response payload looks like this: 
```
{"delivery_fee": 1500}
```

### Error handling
It should also be noted that, if the data in the request payload is written in the wrong format, one of these errors will occur:
```
ValueError: Cart value, delivery distance, and number of items must be positive integers.
```
```
ValueError: Invalid time format. Use YYYY-MM-DDTHH:MM:SSZ.
```

## Extra Notes
Just for documentation, the libraries imported at the top of this code are:
- ```flask (Flask, request)```
- ```flask_restful (Api, Resource)```
- ```datetime (datetime)```
- ```requests```
- ```unittest```

Additionally, there is a third file titled _test_calc.py_ which is used for simple unit testing both of the functions in _calculator.py_. I added this third file because if this project is ever expanded upon, unit testing should ensure each of the functions still work properly and there are no new bugs introduced. The unit testing can be performed by typing the command ```python3 -m unittest test_calc.py``` into the terminal.

Lastly, the Flask server is being run in debug mode since it is being tested. This can be seen in the _calculator.py_ file:
```
if __name__ == "__main__":
  app.run(debug=True)
```
This should **not** be in debug mode if it were going to be used in a production environment.

Hopefully this document provides instructions that are clear and easy to follow. That's all for now! 

