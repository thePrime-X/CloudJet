import time
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from config import DB_URI 

engine = create_engine(DB_URI, echo=False)

def auto_insert_flights(interval: int = 10):
    departure_airports = ['SVO', 'LED', 'DME', 'ULY', 'IAR', 'MQF', 'NYM', 'EGO', 'NFG']
    arrival_airports = ['KZN', 'ROV', 'KUF', 'KVX', 'IJK', 'RTW', 'PEE']
    aircraft_codes = ['773', '319', '320', '319', 'CN1']

    flight_id = 40000  # start here
    base_date = datetime(2017, 9, 20, 0, 0, 0)  # Fixed start date

    print("[STARTED] Auto flight insertion loop...")

    try:
        while flight_id <= 50000:  # optional upper limit
            flight_no = f"FN{random.randint(1000, 9999)}"
            departure_airport = random.choice(departure_airports)
            arrival_airport = random.choice([a for a in arrival_airports if a != departure_airport])

            scheduled_departure = base_date + timedelta(hours=(flight_id - 40000))
            scheduled_arrival = scheduled_departure + timedelta(hours=random.randint(1, 5))
            aircraft_code = random.choice(aircraft_codes)

            insert_query = text("""
                INSERT INTO flights (
                    flight_id,
                    flight_no, 
                    scheduled_departure, 
                    scheduled_arrival, 
                    departure_airport, 
                    arrival_airport, 
                    aircraft_code, 
                    status
                )
                VALUES (:flight_id, :flight_no, :sd, :sa, :dep, :arr, :air, 'Scheduled');
            """)

            with engine.begin() as conn:
                conn.execute(insert_query, {
                    'flight_id': flight_id,
                    'flight_no': flight_no,
                    'sd': scheduled_departure,
                    'sa': scheduled_arrival,
                    'dep': departure_airport,
                    'arr': arrival_airport,
                    'air': aircraft_code
                })

            print(f"[INSERTED] flight_id={flight_id} {flight_no} ({departure_airport} → {arrival_airport}) at {scheduled_departure:%Y-%m-%d %H:%M:%S}")

            flight_id += 1
            time.sleep(interval)

        print("Reached the maximum flight_id limit.")

    except KeyboardInterrupt:
        print("\n[STOPPED] Flight insertion stopped by user.")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    auto_insert_flights(interval=5)
