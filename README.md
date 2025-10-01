# CloudJet
CloudJet is a US-based airline company established in 2010. Since its inception, CloudJet has expanded its operations to include both regional and international flights, serving passengers across the globe.

----------------

# Purpose of Repository
This repository contains my work on an airline dataset provided by CloudJet. The goal is to analyze, explore, and visualize the data to generate meaningful insights. Through this project, I aim to gain hands-on experience with data visualization and contribute to produce high-quality data insights for the company. 

The dataset includes eight tables: `aircrafts_data`, `airports_data`, `boarding_passes`, `bookings`, `flights`, `seats`, `ticket_flights`, and `tickets`.

### ERD Diagram of Airline Dataset
<img width="1319" height="764" alt="Screenshot 2025-09-26 165748" src="https://github.com/user-attachments/assets/7311afe8-d849-4a63-b9b5-b9883bc15619" />


## Usage of `main.py` & `queries.sql`
This project allows you to run predefined SQL queries directly from the terminal using Python, eliminating the need to manually open pgAdmin or another PostgreSQL client.
### Files
- `main.py` - Python script to execute SQL queries from the terminal.
- `queries.sql` - Contains 10 useful SQL queries related to flight and passenger data.

### How to Use
To run queries, make sure you have:
1. Access to your PostgreSQL database
2. The following database credentials
   - Username
   - Port
   - Password
   - Database name

### List of Queries:
1. Top 5 Most Used Aircraft Models
2. Top 5 Total Amount Spent by Passengers on Flights
3. Top 5 Busiest Airports by Number of Arrivals
4. Top 5 Busiest Airports by Number of Departures
5. Top 3 Longest Range Aircraft Models
6. Top 5 Aircraft Models with the Highest Number of Passengers
7. Top 5 Flights with the Highest Number of Business Classes Booked
8. Top 5 Flights with the Highest Number of Economy Classes Booked
9. Number of Cancelled Flights
10. Number of On-Time Flights

### Example Usage
`python main.py`
