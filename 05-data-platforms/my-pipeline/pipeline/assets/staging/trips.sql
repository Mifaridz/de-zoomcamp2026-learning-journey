/* @bruin

name: staging.trips
type: duckdb.sql

materialization:
  type: table
  strategy: create+replace

depends:
  - ingestion.trips
  - ingestion.payment_lookup

columns:
  - name: vendor_id
    type: BIGINT
    description: ID of the taxi vendor
  - name: pickup_datetime
    type: VARCHAR
    primary_key: true
    checks:
      - name: not_null
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
  - name: payment_type_name
    type: VARCHAR

@bruin */

SELECT 
    t.*,
    p.payment_type_name
FROM ingestion.trips t
LEFT JOIN ingestion.payment_lookup p 
    ON t.payment_type = p.payment_type_id
