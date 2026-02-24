"""@bruin

name: ingestion.trips
connection: duckdb-default

materialization:
  type: table
  strategy: create+replace
image: python:3.11

columns:
  - name: vendor_id
    type: BIGINT
  - name: pickup_datetime
    type: VARCHAR
  - name: dropoff_datetime
    type: VARCHAR
  - name: passenger_count
    type: BIGINT
  - name: trip_distance
    type: DOUBLE
  - name: fare_amount
    type: DOUBLE
  - name: payment_type
    type: BIGINT

@bruin"""

import pandas as pd
from datetime import datetime

def materialize():
    data = [
        {
            "vendor_id": 1,
            "pickup_datetime": "2024-01-01 10:00:00",
            "dropoff_datetime": "2024-01-01 10:15:00",
            "passenger_count": 2,
            "trip_distance": 3.5,
            "fare_amount": 15.0,
            "payment_type": 1 
        },
        {
            "vendor_id": 2,
            "pickup_datetime": "2024-01-01 11:00:00",
            "dropoff_datetime": "2024-01-01 11:20:00",
            "passenger_count": 1,
            "trip_distance": 5.0,
            "fare_amount": 22.5,
            "payment_type": 2 # Cash
        }
    ]
    
    return pd.DataFrame(data)
