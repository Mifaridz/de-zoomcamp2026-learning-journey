import duckdb
import requests
from pathlib import Path

BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"

def download_and_convert_files(taxi_type):
    data_dir = Path("data") / taxi_type
    data_dir.mkdir(exist_ok=True, parents=True)

    # Loop tahun 2019 dan 2020
    for year in [2019, 2020]:
        for month in range(1, 13):
            parquet_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
            parquet_filepath = data_dir / parquet_filename

            if parquet_filepath.exists():
                print(f"Skipping {parquet_filename} (already exists)")
                continue

            # Download CSV.gz file
            csv_gz_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.csv.gz"
            csv_gz_filepath = data_dir / csv_gz_filename

            print(f"Downloading {csv_gz_filename}...")
            response = requests.get(f"{BASE_URL}/{taxi_type}/{csv_gz_filename}", stream=True)
            try:
                response.raise_for_status()
                with open(csv_gz_filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            except Exception as e:
                print(f"Failed to download {csv_gz_filename}: {e}")
                continue

            print(f"Converting {csv_gz_filename} to Parquet...")
            
            # Gunakan in-memory connection hanya untuk konversi
            con = duckdb.connect()
            try:
                con.execute(f"""
                    COPY (SELECT * FROM read_csv_auto('{csv_gz_filepath}'))
                    TO '{parquet_filepath}' (FORMAT PARQUET, CODEC 'SNAPPY')
                """)
            except Exception as e:
                print(f"Error converting {csv_gz_filename}: {e}")
            finally:
                con.close()

            # Hapus file CSV.gz untuk hemat space
            csv_gz_filepath.unlink()
            print(f"Completed {parquet_filename}")

def update_gitignore():
    gitignore_path = Path(".gitignore")
    content = gitignore_path.read_text() if gitignore_path.exists() else ""
    if 'data/' not in content:
        with open(gitignore_path, 'a') as f:
            f.write('\n# Data directory\ndata/\n' if content else '# Data directory\ndata/\n')

if __name__ == "__main__":
    update_gitignore()
    
    # Proses download satu per satu
    for taxi_type in ["yellow", "green"]:
        download_and_convert_files(taxi_type)
        
    print("Ingestion selesai! Jalankan script load_prod sekarang.")