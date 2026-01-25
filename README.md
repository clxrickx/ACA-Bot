# ACA-Bot

## DUMBED DOWN VERSION:
Air Canada bot that takes data from the ATC24 API to calculate the distance. This distance is then calculated using a formula to find the amount of points/miles to give the pilot. Then it sends a request to the points bot, which gives the points. 

You also have the option to insert flight time for a planned flight(in the ACA server), and another formula is used to calculate the amount of points to compensate the crew. The request to the points bot is sent again.

## Technical Version:
Data from 24API is accessed from an HTTP backend server, which is then sent to the main backend. From the 24API, the backend finds the total distance using speed and time, as well as points for numerical check. If both values are within a set range/margin, the result is sent to the formula, which evaluates the amount of points to compensate. This is then sent as an output to the Points Bot, which rewards the crew member with points.

Note: we are not SWE's. I(clxrickx) am in no way certified to make something like this; I'm just doing my best. Please don't flame us for the horrible optimization or overhead lol.
