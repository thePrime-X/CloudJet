<<<<<<< HEAD
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

-- Top 5 Busiest Destinations by Number of Flights
SELECT a.city AS city_name, COUNT(f.flight_id) AS total_arrivals
FROM flights f
JOIN airports_data a ON f.arrival_airport = a.airport_code
GROUP BY a.city
ORDER BY total_arrivals DESC
LIMIT 5;

-- Top 3 Most prefered aircrafts model for business class
SELECT ad.model, COUNT(*) AS business_class_passengers
FROM ticket_flights tf
JOIN flights f ON tf.flight_id = f.flight_id
JOIN aircrafts_data ad ON f.aircraft_code = ad.aircraft_code
WHERE tf.fare_conditions = 'Business'
GROUP BY ad.model
ORDER BY business_class_passengers DESC
Limit 3;

-- Top 3 Most prefered aircrafts model for economy class
SELECT ad.model, COUNT(*) AS economy_class_passengers
FROM ticket_flights tf
JOIN flights f ON tf.flight_id = f.flight_id
JOIN aircrafts_data ad ON f.aircraft_code = ad.aircraft_code
WHERE tf.fare_conditions = 'Economy'
GROUP BY ad.model
ORDER BY business_class_passengers DESC
limit 3;

-- Hottest Destinations by Number of Passengers
SELECT a.city, COUNT(*) AS total_passengers
FROM ticket_flights tf
JOIN flights f ON tf.flight_id = f.flight_id
JOIN airports_data a ON f.arrival_airport = a.airport_code
GROUP BY a.city
ORDER BY total_passengers DESC
Limit 5

-- Top 5 Longest Flights by Duration
WITH flight_durations AS (
    SELECT 
        flight_no,
        flight_id,
        departure_airport,
        arrival_airport,
        scheduled_departure,
        scheduled_arrival,
        EXTRACT(EPOCH FROM (scheduled_arrival - scheduled_departure)) / 60 AS duration_minutes
    FROM flights
    WHERE scheduled_departure IS NOT NULL AND scheduled_arrival IS NOT NULL
),
ranked_flights AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY flight_no ORDER BY duration_minutes DESC) AS rn
    FROM flight_durations
)
SELECT 
    rf.flight_no,
    ad.city AS departure_city,
    aa.city AS arrival_city,
    rf.duration_minutes
FROM ranked_flights rf
JOIN airports_data ad ON rf.departure_airport = ad.airport_code
JOIN airports_data aa ON rf.arrival_airport = aa.airport_code
WHERE rf.rn = 1
ORDER BY rf.duration_minutes DESC
LIMIT 5;

-- Top 5 Destinations with the Highest Number of Business Class Passengers
SELECT 
    a.city AS destination_city,
    COUNT(*) AS business_class_passenger_count
FROM ticket_flights tf
JOIN flights f ON tf.flight_id = f.flight_id
JOIN airports_data a ON f.arrival_airport = a.airport_code
WHERE tf.fare_conditions = 'Business'
GROUP BY a.city
ORDER BY business_class_passenger_count DESC
LIMIT 5;

=======
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

>>>>>>> 6ef4326ef850aac2dd48065c6a27603489434d10
