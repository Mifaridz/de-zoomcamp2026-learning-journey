import dlt
import requests
import logging
from typing import Iterator, Dict, Any

logger = logging.getLogger(__name__)

BASE_URL = (
    "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"
)

@dlt.resource(
    name="taxi_trips",
    write_disposition="append",
)
def taxi_api_resource() -> Iterator[Dict[str, Any]]:
    """
    Streaming data from Taxi REST API, page by page.
    The API returns up to 1000 rows per page.
    """
    page = 1
    session = requests.Session()

    while True:
        try:
            resp = session.get(BASE_URL, params={"page": page}, timeout=10)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed on page {page}: {e}")
            break

        data = resp.json()

        if not data:
            logger.info(f"No more data. Finished at page {page}.")
            break

        for rec in data:
            yield rec

        page += 1


@dlt.source
def taxi_pipeline_rest_api_source():
    return [taxi_api_resource()]


pipeline = dlt.pipeline(
    pipeline_name="taxi-pipeline",
    destination="duckdb",
    dataset_name="taxi_dataset",
    progress="log",
)

if __name__ == "__main__":
    info = pipeline.run(taxi_pipeline_rest_api_source())
    print(info)