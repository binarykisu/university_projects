# Airplane Boarding Simulation using Monte Carlo method

## Introduction

This project is one from my statistical methods university courses, but it is generally a popular, practical, and thought-provoking problem that is good for improving one's coding skills. This exercise has been worked through 
by using Monte Carlo methods to examine the boarding of passengers onto an Airbus A320 ([like this one](https://www.seatguru.com/airlines/Finnair/Finnair_Airbus_A320.php)). 

## The goal

The idea is to simulate 100 boardings of passengers, where the passengers start off by standing in the line at the gate/terminal in some random order. Additionally, the seats are randomly pre-assigned to each passenger.
At the end of the simulations, we want to know the average total boarding time (including the standard deviation) - in other words, the time between the first passenger in line starting to walk from the gate to the last 
passenger sitting down in their seat.

## Variables and rules

Here are the "givens" for this problem, or the rules that we have to follow:

- There are $165$ passengers.
- Passengers must queue at the gate with a $0.5 m$ distance between any other passengers.
- The distance from the gate to the first seat row is $25 m$.
- People are randomly seated.
- Everyone walks at a speed of $0.5 m/s$.
- Seat rows on the plane are $1 m$ apart from each other.

- The plane is assumed to be $100 %$ full (no empty seats).
- Row interference must be considered - a passenger cannot sit in their window or aisle seat if other passengers are already seated in the seats closer to the aisle, so they must swap seats.
  -  Swapping with one passenger takes $11 s$ to complete.
  -  Swapping with two passengers takes $22 s$ to complete.
- Aisle interference must be considered - a passenger cannot get through to their row if another passenger is standing in the aisle to put their luggage in the overhead compartment.
  - Aisle interference takes $25 s$ to complete.

## Results

After everyone has been seated, the time on the clock is stored. After performing 100 boarding simulations, the mean/average boarding time and
the standard deviation of the times is calculated. For this project, I found that the average boarding time takes $t \approx 1402 \pm 72$ seconds (or $\approx 23 \pm 1$ minutes) to complete.

That's all for now!
