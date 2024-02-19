# Importing the necessary libraries
import random
import math

# A class for creating instances of passenger objects
# Keeps track of passenger's seat number, position, and busy status
class Passenger:
  def __init__(self, seat: int, position: int):
    self.seat = seat
    self.timer = 0
    self.position = position
    self.row = seat // 10
    self.column = seat % 10
    
  def get_position(self) -> int:
    """Getter method that returns the current position of the passenger"""
    return self.position
    
  def is_busy(self) -> bool:
    """Checks to see if the passenger is currently busy"""
    return self.timer > 0
    
  def tick(self, time_step: float):
    """Decreases the passenger's timer by the specified time step"""
    self.timer -= time_step
    
  def get_row(self) -> int:
    """Returns the row number of the passenger's seat"""
    return self.row
    
  def get_column(self) -> int:
    """Returns the column number of the passenger's seat"""
    return self.column
    
  def get_seat(self) -> int:
    """Returns the seat number of the passenger"""
    return self.seat
    
  def set_delay(self, delay: float) -> float:
    """Increases the passenger's timer by the specified delay"""
    self.timer += delay
    
  def advance(self, distance: float):
    """Advances the passenger's position by an amount"""
    self.position += distance

# Function that simulates the boarding process and calculates the mean/variance
class BoardingProcess():
  def __init__(self):
    # All units of time are in seconds, position in meters
    self.num_rows = 28 # Number of rows in the plane
    self.half_row = True  # First row has 3 seats only
    self.num_cols = 6 # Number of columns in each row
    self.gate = -25 # Starting position of the passengers
    self.delta_seats = 1 # Distance between seats in a row
    self.delta_passengers = 0.5 # Distance between passengers in a queue
    self.passenger_speed = 0.5 # Speed at which passengers move
    self.time_step = 0.25 # Time step used in simulation
    self.delay_aisle = 25 # Delay for passengers in the aisle
    self.delay_swap = 11 # Delay for passengers swapping seats
    self.delay_double = 22 # Delay for passengers swapping seats with two already-seated passengers
    self.num_simulations = 100 # Number of boardings simulated
    
    # If you would like reproducability, uncomment this
    # random.seed(5) # Initialize random seed

  def seat_assignment(self) -> list[Passenger]:
    """Assigns seats to passengers in a random order;
    Returns a list of passengers with assigned seats"""
    passengers = []
    
    # Use seat numbering seat = 10*row + column
    seats = [(i + 1) * 10 + j + 1 for i in range(self.num_rows) for j in range(self.num_cols)]
    random.shuffle(seats)

    # Assign passengers in queue (starting at gate) 
    # Distance of delta_passengers should increase every time
    for i in range(self.num_rows * self.num_cols):
      assigned_seat = seats.pop()
      if (not self.half_row) or (assigned_seat < 14) or (assigned_seat > 16):
        passengers.append(Passenger(assigned_seat, self.gate - i * self.delta_passengers))
    return passengers

  def boarding_process(self, passengers: list[Passenger]) -> float:
    """Simulates the boarding process for a list of passengers;
    Returns the total time taken for all passengers to board"""
    clock = 0
    seated = {}
    
    # Start boarding
    while passengers:
      passenger_index = 0
      clock += self.time_step
      while passenger_index < len(passengers):
        passenger = passengers[passenger_index] # Working with one passenger at a time
        if passenger.is_busy(): # If passenger is busy, reduce timer
          passenger.tick(self.time_step)
        if not passenger.is_busy(): # If passenger is not busy
          if passenger.get_position() == (passenger.get_row() - 1) * self.delta_seats: 
            seated[passenger.get_seat()] = True # If passenger is at correct row, sit down
            passengers.pop(passenger_index)
            continue
          # If passenger ahead is not within delta_passengers, move on
          elif passenger_index == 0 or (passengers[passenger_index - 1].get_position() - passenger.get_position() - self.passenger_speed * self.time_step >= self.delta_passengers):
            passenger.advance(self.passenger_speed * self.time_step)
          # Correct row found, checking if swap is needed
          if passenger.get_position() == (passenger.get_row() - 1) * self.delta_seats:
            offset = self.is_swap_needed(passenger, seated)
            passenger.set_delay(self.delay_aisle + offset)
        passenger_index += 1  
    return clock         
             
  def is_swap_needed(self, passenger: Passenger, seated: dict) -> int:
    """Checks if a passenger needs to swap seats with another passenger;
    Returns the delay time if a swap is needed"""           
    offset = 0
    # The numbers 1-6 refer to the columns in the plane
    if passenger.get_column() == 2 and seated.get(10 * passenger.get_row() + 3):
      offset = self.delay_swap
    if passenger.get_column() == 5 and seated.get(10 * passenger.get_row() + 4):
      offset = self.delay_swap
    if passenger.get_column() == 1:
      if seated.get(10 * passenger.get_row() + 2) and seated.get(10 * passenger.get_row() + 3):
        offset = self.delay_double  # Two passengers already seated
      elif seated.get(10 * passenger.get_row() + 2) != seated.get(10 * passenger.get_row() + 3):
        offset = self.delay_swap  # One other person already seated
    if passenger.get_column() == 6:
      if seated.get(10 * passenger.get_row() + 4) and seated.get(10 * passenger.get_row() + 5):
        offset = self.delay_double
      elif seated.get(10 * passenger.get_row() + 4) != seated.get(10 * passenger.get_row() + 5):
        offset = self.delay_swap
    return offset                  
              
  def boarding_simulation(self) -> list:
    """Simulates the boarding process for a number of times specified by num_simulations;
    Returns a list of times taken for each simulation"""
    times = []
    for _ in range(self.num_simulations):
      passengers = self.seat_assignment()
      clock = self.boarding_process(passengers)
      times.append(clock)
    return times
    
  def calculate_statistics(self, times: list) -> tuple:
    """Calculates the mean and variance of a list of times;
    Returns the mean and variance"""
    mean = sum(times) / self.num_simulations
    var = sum((t - mean) ** 2 for t in times) / (self.num_simulations - 1)
    return mean, var

  def run_boarding_process(self) -> None:
    """Runs the boarding simulation and calculates statistics;
    Prints the mean and standard deviation of the times taken for all simulations"""
    times = self.boarding_simulation()
    mean, var = self.calculate_statistics(times)
    if not self.half_row:
      print(f"The plane has {self.num_rows} rows with {self.num_cols} seats each.")
    else:
      print(f"The plane has {self.num_rows} rows with {self.num_cols} seats each, except the first row, which has only 3 seats.")
    print(f"Over {self.num_simulations} simulations, the average time for all passengers to board the plane is {mean:.1f} +- {math.sqrt(var):.1f} seconds.")

if __name__ == "__main__":
    boarding_process = BoardingProcess()
    boarding_process.run_boarding_process()
