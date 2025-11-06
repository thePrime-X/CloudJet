-- Top 5 Most Used Aircraft Models
select 
	a.model AS aircraft_model,
	COUNT(*) AS usage_count
from flights f
join aircrafts_data a
	on f.aircraft_code = a.aircraft_code
group by a.model
order by usage_count desc;

-- Top 5 Aircaft Models with the Highest Number of Passengers
SELECT 
    a.model AS aircraft_model,
    COUNT(s.seat_no) AS total_seats
FROM seats s
JOIN aircrafts_data a
    ON s.aircraft_code = a.aircraft_code
GROUP BY a.model
ORDER BY total_seats DESC;

-- Top 5 Flights with the Highest Number of Business Classes Booked
SELECT 
    a.model AS aircraft_model,
    COUNT(*) AS business_seat_count
FROM seats s
JOIN aircrafts_data a
    ON s.aircraft_code = a.aircraft_code
WHERE s.fare_conditions = 'Business'
GROUP BY a.model
ORDER BY business_seat_count DESC;

-- Top 5 Flights with the Highest Number of Economy Classes Booked
SELECT 
    a.model AS aircraft_model,
    COUNT(*) AS economy_seat_count
FROM seats s
JOIN aircrafts_data a
    ON s.aircraft_code = a.aircraft_code
WHERE s.fare_conditions = 'Economy'
GROUP BY a.model
ORDER BY economy_seat_count DESC;

-- Top 5 Busiest Destinations by Number of Flights
SELECT a.city AS city_name, COUNT(f.flight_id) AS total_arrivals
FROM flights f
JOIN airports_data a ON f.arrival_airport = a.airport_code
GROUP BY a.city
ORDER BY total_arrivals DESC;

-- Top 3 Most prefered aircrafts model for business class
SELECT ad.model, COUNT(*) AS business_class_passengers
FROM ticket_flights tf
JOIN flights f ON tf.flight_id = f.flight_id
JOIN aircrafts_data ad ON f.aircraft_code = ad.aircraft_code
WHERE tf.fare_conditions = 'Business'
GROUP BY ad.model
ORDER BY business_class_passengers DESC;

-- Top 3 Most prefered aircrafts model for economy class
SELECT ad.model, COUNT(*) AS economy_class_passengers
FROM ticket_flights tf
JOIN flights f ON tf.flight_id = f.flight_id
JOIN aircrafts_data ad ON f.aircraft_code = ad.aircraft_code
WHERE tf.fare_conditions = 'Economy'
GROUP BY ad.model
ORDER BY economy_class_passengers DESC;

-- Hottest Destinations by Number of Passengers
SELECT a.city, COUNT(*) AS total_passengers
FROM ticket_flights tf
JOIN flights f ON tf.flight_id = f.flight_id
JOIN airports_data a ON f.arrival_airport = a.airport_code
GROUP BY a.city
ORDER BY total_passengers DESC;

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
ORDER BY rf.duration_minutes DESC;

-- Top 5 Destinations with the Highest Number of Business Class Passengers
SELECT 
    a.city AS destination_city,
    COUNT(*) AS business_class_passenger_count
FROM ticket_flights tf
JOIN flights f ON tf.flight_id = f.flight_id
JOIN airports_data a ON f.arrival_airport = a.airport_code
WHERE tf.fare_conditions = 'Business'
GROUP BY a.city
ORDER BY business_class_passenger_count DESC;



INSERT INTO aircrafts_data (aircraft_code, model, range)
VALUES ('sampleAircraft', 'jet', 15000);


insert into ticket_flights (ticket_no, flight_id, fare_conditions, amount)
values ('zzzzzz', 990099, 'business', 15000);


insert into flights (flight_id, flight_no, aircraft_code)
values (990099, 'mmmmnnnn', 'sampleAircraft')