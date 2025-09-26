-- Top 5 Most Used Aircraft Models
select 
	a.model AS aircraft_model,
	COUNT(*) AS usage_count
from flights f
join aircrafts_data a
	on f.aircraft_code = a.aircraft_code
group by a.model
order by usage_count desc
limit 5;

-- Top 5 Total Amount Spent by Passengers on Flights
SELECT * FROM bookings
WHERE total_amount > 100000
ORDER BY total_amount ASC
limit 10;

-- Top 5 Busiest Airports by Number of Arrivals
SELECT 
    arrival_airport,
    COUNT(*) AS arrival_count
FROM flights
GROUP BY arrival_airport
ORDER BY arrival_count DESC
LIMIT 1;

-- Top 5 Busiest Airports by Number of Departures
SELECT 
    departure_airport,
    COUNT(*) AS departure_count
FROM flights
GROUP BY departure_airport
ORDER BY departure_count DESC
LIMIT 1;

-- Top 3 Longest Range Aircraft Models
SELECT 
    model,
    range
FROM aircrafts_data
ORDER BY range DESC
LIMIT 3;

-- Top 5 Aircaft Models with the Highest Number of Passengers
SELECT 
    a.model AS aircraft_model,
    COUNT(s.seat_no) AS total_seats
FROM seats s
JOIN aircrafts_data a
    ON s.aircraft_code = a.aircraft_code
GROUP BY a.model
ORDER BY total_seats DESC
LIMIT 5;

-- Top 5 Flights with the Highest Number of Business Classes Booked
SELECT 
    a.model AS aircraft_model,
    COUNT(*) AS business_seat_count
FROM seats s
JOIN aircrafts_data a
    ON s.aircraft_code = a.aircraft_code
WHERE s.fare_conditions = 'Business'
GROUP BY a.model
ORDER BY business_seat_count DESC
LIMIT 5;

-- Top 5 Flights with the Highest Number of Economy Classes Booked
SELECT 
    a.model AS aircraft_model,
    COUNT(*) AS economy_seat_count
FROM seats s
JOIN aircrafts_data a
    ON s.aircraft_code = a.aircraft_code
WHERE s.fare_conditions = 'Economy'
GROUP BY a.model
ORDER BY economy_seat_count DESC
LIMIT 5;

-- Sum of Cancelled Flights
SELECT COUNT(*) AS cancelled_flights
FROM flights
WHERE status = 'Cancelled';

-- Sum of On-Time Flights
SELECT COUNT(*) AS on_time_flights
FROM flights
WHERE status = 'On Time';

