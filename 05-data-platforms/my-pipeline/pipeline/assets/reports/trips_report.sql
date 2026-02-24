/* @bruin

name: reports.trips_report
type: duckdb.sql

materialization:
  type: table
  strategy: create+replace

depends:
  - staging.trips

columns:
  - name: vendor_id
    type: BIGINT
    description: ID of the taxi vendor
  - name: total_trips
    type: BIGINT
    description: Total number of trips per vendor
  - name: total_revenue
    type: DOUBLE
    description: Total fare amount collected per vendor

@bruin */

SELECT 
    vendor_id,
    count(*) as total_trips,
    sum(fare_amount) as total_revenue
FROM staging.trips
GROUP BY 1
