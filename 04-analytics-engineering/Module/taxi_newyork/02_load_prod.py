import duckdb

def load_to_prod():
    print("Connecting to database...")
    con = duckdb.connect("taxi_rides_ny.duckdb")
    
    # -------------------------------------------------------
    # OPSI HEMAT RAM: Batasi penggunaan memory jika ingin membuat TABLE fisik
    # Hilangkan tanda pagar di bawah jika komputermu punya RAM kecil (misal 4GB/8GB)
    con.execute("PRAGMA memory_limit='4GB'")
    # -------------------------------------------------------

    con.execute("CREATE SCHEMA IF NOT EXISTS prod")

    for taxi_type in ["yellow", "green"]:
        print(f"Processing {taxi_type} taxi data...")
        
        # --- CARA 1: Menggunakan VIEW (Sangat Direkomendasikan) ---
        # View tidak memakan RAM saat dibuat. Dia membaca langsung dari Parquet 
        # saat kamu melakukan query (SELECT). Ini mencegah duplikasi data.
        query = f"""
            CREATE OR REPLACE VIEW prod.{taxi_type}_tripdata AS
            SELECT * FROM read_parquet('data/{taxi_type}/*.parquet', union_by_name=true)
        """
        
        # --- CARA 2: Menggunakan TABLE (Berat di RAM) ---
        # Jika kamu benar-benar butuh tabel fisik, gunakan query ini:
        # query = f"""
        #     CREATE OR REPLACE TABLE prod.{taxi_type}_tripdata AS
        #     SELECT * FROM read_parquet('data/{taxi_type}/*.parquet', union_by_name=true)
        # """
        
        con.execute(query)
        print(f"Success: prod.{taxi_type}_tripdata created.")

    # Verifikasi
    print("\nVerifying data counts:")
    for taxi_type in ["yellow", "green"]:
        result = con.execute(f"SELECT COUNT(*) FROM prod.{taxi_type}_tripdata").fetchone()
        count = result[0] if result else 0
        print(f"{taxi_type}: {count:,} rows")

    con.close()

if __name__ == "__main__":
    load_to_prod()