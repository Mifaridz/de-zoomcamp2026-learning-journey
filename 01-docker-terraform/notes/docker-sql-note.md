# 🐳 01-Introduction to Docker

> **Topik:** Containerization Fundamentals
> **Konteks:** Data Engineering Infrastructure

## Konsep Utama (Core Concepts)

Docker adalah software _containerization_ yang mengisolasi aplikasi dalam lingkungan yang ringan (_lean_), mirip dengan Virtual Machine tetapi jauh lebih efisien secara sumber daya.

- **Docker Image:** Snapshot atau "cetakan biru" yang berisi semua dependency untuk menjalankan software (termasuk kode data pipeline).
- **Docker Container:** Unit runtime yang berjalan berdasarkan Image.
- **Statelessness:** Secara default, container bersifat sementara. Perubahan di dalamnya akan hilang saat container dihapus (bersifat tidak permanen).

### Mengapa Data Engineer Butuh Docker?

- **Reproducibility:** Menjamin pipeline berjalan sama di laptop lokal, AWS, maupun GCP.
- **Portability:** Memungkinkan pemindahan workload ke berbagai cloud provider tanpa mengubah konfigurasi sistem.
- **Integration:** Digunakan secara luas untuk CI/CD, AWS Batch, Kubernetes, dan pengolahan data skala besar seperti Apache Spark.

### Mekanisme Persistence (Volumes)

Karena container bersifat _stateless_, kita menggunakan **Volumes** untuk menghubungkan folder di komputer host dengan folder di dalam container. Ini memungkinkan data tetap tersimpan atau kode di host bisa dieksekusi oleh environment di dalam container.

## Perintah Dasar (Basic Commands)

| Perintah             | Deskripsi                                                                 |
| -------------------- | ------------------------------------------------------------------------- |
| `docker --version`   | Mengecek versi Docker yang terinstall.                                    |
| `docker run <image>` | Mengunduh (jika belum ada) dan menjalankan container.                     |
| `docker run -it`     | Menjalankan container secara interaktif (masuk ke terminal container).    |
| `docker ps -a`       | Melihat semua container (yang sedang berjalan maupun berhenti).           |
| `docker rm <id>`     | Menghapus container yang sudah berhenti.                                  |
| `--rm`               | Flag untuk menghapus container secara otomatis setelah selesai digunakan. |

---

## Apa yang Berhasil Saya Pelajari

- **Isolasi Environment:** Saya belajar bahwa menginstall library (seperti Python) di dalam Docker tidak akan mengotori sistem operasi utama saya.
- **Override Entrypoint:** Saya memahami cara mengubah perilaku default sebuah image (misal: masuk ke `bash` alih-alih langsung menjalankan aplikasi) menggunakan flag `--entrypoint`.
- **Mounting Volume:** Saya berhasil memetakan folder lokal ke dalam container menggunakan sintaks `-v $(pwd)/host_folder:/container_folder`, sehingga file di host bisa dibaca oleh script di dalam Docker.

### Menjalankan Python di Container (Slim Version)

Gunakan versi `-slim` untuk menghemat ruang penyimpanan.
Biasakan menggunakan flag `--rm` setiap kali melakukan testing agar storage laptop tidak penuh dengan sisa-sisa container yang sudah tidak terpakai.

```bash
docker run -it \
    --rm \
    --entrypoint=bash \
    python:3.9.16-slim

```

### Menghubungkan Script Lokal ke Container

Contoh melakukan mount volume agar script Python di lokal bisa dijalankan oleh environment Docker:

```bash
docker run -it \
    --rm \
    -v $(pwd)/test:/app/test \
    --entrypoint=bash \
    python:3.9.16-slim

```

### 📌 Summary

Docker bukan cuma soal instalasi software, tapi soal cara kita membungkus seluruh environment kerja supaya rapi. Poin pentingnya adalah penggunaan _Image_ untuk menghemat space dan selalu pakai flag _--rm_ pas lagi testing supaya sampah container nggak numpuk di laptop.

> **Note:** _Docker memisahkan antara compute (container) dan storage (volume). Ini adalah prinsip dasar infrastruktur data yang modern._

---

# 🐍 02-Virtual Environments and Data Pipelines

> **Topik:** _Virtual Environments & Build My First Pipeline_

### Setting Up "Kandang" (Environment)

Masalah klasik pada saat menjalakan python dengan project yang berbeda adalah seringnya _library_ yang tabrakan. Jadi saat akan membuat sebuah project alahkah baiknya melakukan setting Environment terlebih dahulu dan list _library_ apa saja yang akan digunakan.

- **Wajib Pakai Virtual Env:** Jangan pernah install apapun di Python global. Titik.
- **Tool Pilihan: `uv`**: Ini _game changer_. Jauh lebih ngebut dibanding `pip`atau`conda`karena dibuat pake Rust. Gunakan `_curl -LsSf https://astral.sh/uv/install.sh | sh_`untuk install`uv`jika menggubakan`WSL` karena terhalang lincense.
- **Highlight Perintah Penting:**
- `uv init --python=3.13`: Bikin pondasi project baru.
- `uv add pandas pyarrow`: Masukin "bumbu" (library) yang kita butuhin.
- `uv run python script.py`: Cara "aman" jalanin script biar nggak nyari library ke mana-mana.

> **📝Note:** `uv run` itu praktis banget karena dia otomatis nge-sync environment kita sebelum script jalan. Gak ada lagi drama "ModuleNotFoundError".

---

### Anatomy of a Pipeline

Saya belajar kalau pipeline itu nggak harus ribet. Esensinya cuma tiga: **Input → Proses → Output**.

- **Input:** Download data (CSV/JSON) dari internet.
- **Proses:** Di sini Pandas main peran. Kita transform data mentah jadi siap pakai.
- **Output:** Simpan ke database (Postgres) atau file yang lebih canggih (Parquet).
- **Dynamic Scripting:** Pake `sys.argv` supaya script kita nggak kaku. Jadi bisa input argumen (misal: tanggal data) lewat terminal tanpa harus edit file `.py`-nya terus-terusan.

> **📝Note:** Jangan lupa pake `df.head()` buat _sanity check_ di tengah jalan, biar kita tau datanya beneran ada atau nggak sebelum diproses lebih jauh.

---

### Data Format: Parquet is King!

Dulu taunya cuma CSV, sekarang baru ngeh kenapa orang DE suka **Parquet**.

- **Highlight:** Parquet itu format _columnar_. Efeknya? Ukuran file jadi jauh lebih kecil (dikompresi) dan baca datanya jauh lebih kenceng daripada CSV yang baris demi baris.

> **📝Note:** _Don't be a messy dev!_ Langsung tambahin `*.parquet` di `.gitignore` biar repository Git kita tetep bersih dari file data yang berat.

---

### 📌 Summary

Hari ini saya berhasil bikin pipeline Python sederhana yang bisa nerima argumen terminal. Inti dari materi ini bukan cuma soal nulis kode, tapi soal **standardisasi**. Pake `uv` buat ngatur dependensi, pake `sys.argv` buat bikin script fleksibel, dan milih format `Parquet` buat efisiensi.

---

# 🐳03-Dockerizing the Data Pipeline

> **Topik:** _Bridging Python Environment & Infrastructure_

### Analogi Sederhana

Saya menyimpulkan proses ini dalam dua tahap besar:

- **`docker build` (Proses Kompilasi):** Mengubah _source code_ + _environment_ (`uv`) menjadi satu paket Image siap pakai.
- **`docker run` (Proses Eksekusi):** Menjalankan "paket" tersebut di mesin mana saja.

---

### Anatomi Dockerfile (Si "Resep Masakan")

Dockerfile adalah urutan instruksi yang dibaca Docker dari atas ke bawah. Berikut komponen kuncinya:

- **`FROM`**: Bahan dasar (OS + Python).
- **`WORKDIR`**: Menentukan folder kerja di dalam container (seperti `cd`).
- **`COPY`**: Memasukkan file dari laptop ke dalam container.
- **`RUN`**: Perintah eksekusi saat pembuatan image (misal: install library).
- **`ENV`**: Setting variabel lingkungan (seperti PATH).
- **`ENTRYPOINT`**: Perintah otomatis yang jalan saat container dinyalakan.

---

### Optimasi "Pro"

Ini poin paling teknis yang saya pelajari. Di Dockerfile, saya melakukan **COPY dua kali**. Kenapa?
![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/01-docker-terraform/notes/note-image/copy2times.png?raw=true)

1. **Layer Caching (Efisiensi Waktu):**

- Saya copy `pyproject.toml` dan `uv.lock` duluan, lalu jalankan `uv sync`.
- Baru setelah itu copy `pipeline.py`.
- **Hasilnya:** Kalau saya cuma ubah kode di `pipeline.py`, Docker nggak perlu download ulang library Pandas/Pyarrow (pakai _cache_). Build ulang jadi cuma hitungan detik!

2. **Multi-stage Copy:**

- Menggunakan `COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/`.
- Tujuannya "meminjam" file binary `uv` dari image resminya tanpa harus install manual yang ribet. Image jadi lebih kecil dan bersih.

---

### Workflow Eksekusi

Setelah Dockerfile siap, ini langkah yang saya lakukan di terminal:

| Langkah   | Perintah                                          | Note                                                                 |
| --------- | ------------------------------------------------- | -------------------------------------------------------------------- |
| **Build** | `docker build -t pipeline-data:v1 .`              | Jangan lupa **titik (.)** di akhir! Itu artinya folder saat ini.     |
| **Run**   | `docker run -it --rm pipeline-data:v1 2026-01-18` | `2026-01-18` akan ditangkap sebagai argumen oleh script Python saya. |

---

### 📌 Summary

Memasukkan pipeline ke dalam Docker merupakan **standarisasi** untuk setiap tugas "_Image_" atau project yang akan dijalankan. Dengan teknik _Layer Caching_, proses _development_ jadi jauh lebih cepat.

> **📝Note:** Penggunaan `ENTRYPOINT` membuat container berperilaku seperti aplikasi _executable_. Kita tinggal panggil nama image-nya dan masukkan argumen yang kita mau di belakangnya.

---

# 🐘 04-PostgreSQL in Docker

> **Topik:** _Database Infrastructure & Data Persistence_

### Konsep: Persistence & Environment

Di sini saya belajar tentang cara yang baik untuk mengelola database di container.

- **Environment Variables (`-e`)**: Cara menyuntikkan konfigurasi (user, pass, nama DB) tanpa bongkar pasang Image.
- **Port Mapping (`-p`)**: Jembatan antara dunia luar (laptop saya) dan dunia dalam container.
- _Highlight:_ `5432:5432` artinya "Ketuk pintu 5432 di laptop, otomatis masuk ke 5432 di container".

- **Persistence (Bind Mount)**: Ini kuncinya! Saya menggunakan `-v` untuk memetakan folder di laptop ke folder data di container.
- _Poin Penting:_ **Kiri (Laptop/Host) : Kanan (Container)**. Apa yang disimpan di Kanan, fisiknya ada di Kiri. Jadi kalau container dihapus, data di folder laptop tetap aman.

---

### Workflow: Menghidupkan Database

Langkah praktis yang saya jalankan untuk membangun "rumah" bagi data nanti:

1. **Siapkan Folder Fisik:** `mkdir ny_taxi_postgres_data`
2. **Jalankan Container (Postgres 16-alpine):**

```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v "$(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data" \
  -p 5432:5432 \
  postgres:16-alpine

```

3. **Install Tool Klien (pgcli):**
   Saya menggunakan `uv add --dev pgcli`.

- **Kenapa pakai `--dev`?** Agar library ini cuma ada di laptop saya untuk kebutuhan _testing_, tapi tidak akan ikut terinstal saat nanti dideploy ke server produksi. Sangat efisien!

---

### Jebakan "Batman": Localhost vs Docker Network

Ada satu _insight_ penting yang saya catat:

- Saat ini saya mengakses database pakai `localhost` karena `pgcli` jalan langsung di laptop.
- **Tapi nanti**, kalau script Python saya juga sudah masuk ke dalam Docker, `localhost` tidak akan berfungsi lagi. Bagi container, `localhost` adalah dirinya sendiri, bukan database-nya.
- _Solusi ke depan:_ Harus pakai **Docker Network** supaya antar container bisa saling mengobrol pakai nama service-nya.

---

### Tabel Perintah & SQL Check

| Perintah                        | Deskripsi                                     |
| ------------------------------- | --------------------------------------------- |
| `uv run pgcli -h localhost ...` | Masuk ke terminal database secara interaktif. |
| `\dt`                           | Cek tabel yang ada (Data Definition).         |
| `CREATE TABLE...`               | Membuat skema awal untuk menampung data.      |

---

### 📌 Summary

Inti dari materi ini adalah **Pemisahan antara Compute dan Storage**. Container boleh mati atau diganti kapan saja (`--rm`), asalkan datanya sudah kita ikat ke folder lokal lewat **Bind Mount**. Dengan menggunakan `uv --dev`, manajemen _tools_ pembantu (seperti `pgcli`) juga jadi jauh lebih bersih di mata seorang _developer_.

---

# 🚜05-Data Ingestion (The Chunking Method)

> **Topik:** _Handling Large Datasets & Memory Optimization_

### Konsep Utama: "Kenapa Harus Chunking?"

Masalah utama di Data Engineering adalah **Memory Error**. Jika kita punya file 10GB sementara RAM laptop cuma 8GB, membukanya secara langsung akan membuat sistem _crash_.

- **Solusinya:** Membaca data dalam potongan kecil (misal per 100.000 baris).
- **Iterator:** Objek Python yang bertindak sebagai "penunjuk". Dia tidak memuat semua data, tapi hanya mengambil satu potong data saat kita memanggilnya.

---

### Tooling & Setup

Untuk proses penyerapan (_ingestion_) ini, memerlukan beberapa alat tambahan di _environment_ `uv`:

- **SQLAlchemy:** Translator yang mengubah perintah Python menjadi bahasa SQL.
- **psycopg2-binary:** Driver atau jembatan komunikasi antara Python dan PostgreSQL.
- **Jupyter:** Tempat eksperimen kode sebelum dijadikan script `.py` permanen.

> **📝Note:** Gunakan perintah `uv add --dev jupyter` agar alat bantu eksperimen ini tidak memberatkan sistem saat nanti kita melakukan _deployment_ ke server produksi.

---

### Alur Kerja Ingestion

#### 1. Koneksi Database (The Engine)

Menggunakan `create_engine` sebagai pusat komunikasi ke Postgres Docker yang sudah kita nyalakan sebelumnya.

- Format: `postgresql://user:pass@host:port/db_name`

#### 2. Skema Otomatis (DDL)

Salah satu kemudahan di Pandas adalah fungsi `pd.io.sql.get_schema`. Dia otomatis menebak tipe data kolom (Integer, Float, atau Timestamp) dari file CSV untuk dibuatkan tabelnya di SQL.

> **📝Note:** Selalu cek tipe data kolom tanggal. Jika tipenya masih _Object_, paksa jadi _Datetime_ dengan parameter `parse_dates` agar kita bisa melakukan analisis waktu di database nanti.

#### 3. Logika Ingestion Berulang

Ini adalah inti dari kodenya. Prosesnya adalah:

1. **Buat Tabel Kosong:** Pakai `head(0).to_sql(..., if_exists='replace')`.
2. **Looping Data:** Menggunakan `while True` dan `next(df_iter)`.
3. **Append Data:** Masukkan potongan data baru ke bawah data yang sudah ada dengan `if_exists='append'`.

---

### Strategi `if_exists`: Replace vs Append

Saya harus sangat teliti di bagian ini:

- **`replace`**: Digunakan hanya sekali di awal untuk menghapus tabel lama dan membuat struktur baru yang bersih.
- **`append`**: Digunakan di dalam _looping_ untuk terus menumpuk data. Jika salah pakai `replace` di dalam _loop_, data sebelumnya akan terhapus dan yang tersisa cuma potongan terakhir!

---

### 📌 Summary

Proses _Data Ingestion_ bukan sekadar `copy-paste`. Kita harus memperhatikan **Data Integrity** (tipe data yang benar) dan **Resource Management** (penggunaan RAM). Dengan teknik _Chunking_ dan penanganan _error_ `StopIteration`, kita bisa memproses data sebesar apa pun tanpa takut laptop meledak.

---

# 🐍 06-Refactoring to Production Scripts

> **Topik:** _From Notebooks to Automated CLI Tools_

### Mindset: Analyst vs. Engineer

- **Analyst (Jupyter):** Fokus pada eksplorasi, visual, dan interaktif. Tapi, sulit dijadwalkan secara otomatis.
- **Engineer (Script `.py`):** Fokus pada otomatisasi, skalabilitas, dan parameter dinamis. Inilah yang digunakan di sistem nyata (seperti Airflow).

---

### Tooling Baru: Library `click`

Dulu di modul awal saya belajar `sys.argv`, tapi sekarang saya diperkenalkan dengan **`click`**.

- **Kenapa `click`?** Jauh lebih rapi dan profesional untuk membuat **CLI (Command Line Interface)**.
- **Decorator Magic (`@click`):** Saya belajar bahwa tanda `@` di atas fungsi itu gunanya untuk "membungkus" fungsi tersebut agar punya kekuatan tambahan (menangkap input dari terminal).

> **📝Note:** Menggunakan `click` membuat script saya tidak lagi kaku. Saya bisa memasukkan user, password, dan URL database langsung dari terminal tanpa perlu menyentuh kode programnya lagi.

---

### Prinsip "Hardcoding is Evil"

Satu pelajaran penting yang saya catat: **Jangan pernah menulis nilai tetap (Hardcoded)** seperti password atau URL file di dalam kode.

- **Solusinya:** Gunakan **Arguments/Flags**.
- **Manfaatnya (Reusability):** Bulan depan kalau ada data baru, saya tidak perlu buka file `.py`-nya. Cukup ganti link URL-nya di terminal. Script yang sama bisa dipakai berkali-kali!

---

### Struktur Script `ingest_data.py`

Saya merangkum struktur script produksi yang baik:

1. **Definisi Argumen:** Menentukan apa saja yang harus diinput (user, password, host, port, db, table, url).
2. **Koneksi Engine:** Membuat jalur ke database berdasarkan argumen tersebut.
3. **Logika Ingestion:** Menggabungkan teknik _Chunking_ dan _DateTime conversion_ agar data masuk dengan format yang benar.

---

### Cara Eksekusi Script

Menjalankan script sekarang terasa lebih keren karena menggunakan terminal:

```bash
uv run python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url="https://link-data-taksi.csv.gz"

```

---

### 📌 Summary

Mengubah Notebook menjadi Script adalah proses **Standardisasi**. Dengan library `click`, script saya sekarang bersifat dinamis dan siap dijalankan oleh sistem otomatis mana pun.

> **📝Note:** Saya melihat sudut pandang baru ini seperti memisahkan antara "mesin" (logika kode) dan "bahan bakar" (parameter input). Mesinnya tetap sama, bahan bakarnya bisa kita ganti-ganti sesuai kebutuhan.

---

# 🖥️ 07-Docker Networking & pgAdmin GUI

> **Topik:** _Inter-container Communication & Database Management_

### Konsep Utama: Kenapa Butuh Docker Network?

Saya memahami ini sebagai konsep dasar _Distributed Systems_.

- **Isolated Environment:** Secara default, setiap container itu seperti laptop yang terpisah.
- **Masalah Localhost:** Bagi Container A, `localhost` adalah dirinya sendiri. Dia tidak bisa melihat Container B melalui `localhost`.
- **Docker Network:** Berfungsi sebagai "Switch LAN" virtual yang menghubungkan antar container agar bisa saling berkomunikasi.
- **Service Discovery (DNS):** Docker punya fitur cerdas di mana **Nama Container** otomatis menjadi **Hostname**. Kita tidak perlu menghafal IP Address container, cukup panggil namanya saja.

---

### Mengapa Baru Sekarang Kita Mengatur Network?

Saya mencatat perbedaan mendasar antara latihan sebelumnya dan sekarang:

1. **Kemarin:** Script Python jalan di laptop (Host) -> Mengakses Docker via `localhost` (Jembatan Port). Ini berhasil.
2. **Sekarang:** pgAdmin jalan di dalam Docker -> Ingin mengakses Postgres yang juga di Docker. pgAdmin tidak bisa pakai `localhost` karena database-nya berada di "laptop" (container) yang berbeda.

---

### Workflow: Menghubungkan Dua Container

Langkah-langkah yang saya jalankan untuk membuat ekosistem database yang terhubung:

1. **Buat Jaringan Virtual:**
   `docker network create pg-network`
2. **Jalankan Postgres dengan Nama Spesifik:**

```bash
docker run -d \
  --network=pg-network \
  --name pgdatabase \
  -e POSTGRES_USER="root" ... (parameter lainnya)

```

> **Highlight:** Parameter `--name pgdatabase` sangat penting karena ini akan menjadi alamat (Hostname) yang dipanggil oleh pgAdmin.

3. **Jalankan pgAdmin di Jaringan yang Sama:**

```bash
docker run -d \
  --network=pg-network \
  --name pgadmin \
  -p 8085:80 \
  dpage/pgadmin4

```

---

### Konfigurasi Koneksi pgAdmin

Saat mendaftarkan server baru di GUI pgAdmin, bagian paling krusial adalah **Hostname**.

- **SALAH:** Mengisi `localhost`.
- **BENAR:** Mengisi `pgdatabase` (sesuai nama container yang dibuat).

> **📝Notel:** Port yang dipetakan ke laptop (`8085`) hanya digunakan untuk mengakses web-nya saja. Namun, di dalam jaringan Docker, komunikasi antar container tetap menggunakan port asli aplikasi (Postgres tetap `5432`).

---

### 📌 Summary

Inti dari materi ini adalah memahami bahwa container tidak hidup sendirian. Agar bisa saling mengobrol, mereka harus berada di dalam **Docker Network** yang sama. Penggunaan **Nama Container sebagai Hostname** adalah standar industri yang memudahkan kita dalam mengelola infrastruktur tanpa harus pusing dengan perubahan IP dinamis.

> **Insight Pribadi:** Ternyata membangun infrastruktur data itu seperti menyusun jaringan kabel LAN, tapi semuanya dilakukan lewat baris perintah (virtual). Dengan pgAdmin, saya sekarang bisa melihat data taksi yang kita _ingest_ kemarin dengan jauh lebih nyaman.

---

# 🐳 08-Containerizing the Pipeline

> **Topik:** _Turning Scripts into Portable Data Products_

### Konsep Utama: Perubahan Koneksi

Saya mencatat satu perubahan logika yang sangat krusial saat memindahkan script ke dalam Docker:

- **Kemarin (Local):** Script di laptop mengakses database via `localhost`.
- **Sekarang (Inside Docker):** Karena script berjalan di dalam container `taxi_ingest`, dia tidak lagi mengenal `localhost` milik laptop.
- **Solusinya:** Menggunakan **Nama Container** (`pgdatabase`) sebagai Hostname. Docker Network otomatis menerjemahkan nama ini menjadi alamat IP yang tepat.

---

### Optimasi Dockerfile: Layer Caching

Saya belajar teknik "cerdas" dalam menyusun Dockerfile agar proses _build_ tidak memakan waktu lama:

1. **Tahap 1:** Copy `pyproject.toml` dan jalankan `uv sync`.
2. **Tahap 2:** Copy script utama `ingest_data.py`.

- **Kenapa dipisah?** Karena proses instalasi library itu berat dan lama. Dengan memisahkan perintahnya, jika saya hanya mengubah logika kodingan, Docker akan memakai _cache_ untuk library-nya. Build ulang jadi super cepat!

---

### Workflow Eksekusi Final

Inilah langkah-langkah standar industri yang saya jalankan:

| Langkah   | Perintah                                               | Tujuan                                                                  |
| --------- | ------------------------------------------------------ | ----------------------------------------------------------------------- |
| **Build** | `docker build -t taxi_ingest:v001 .`                   | Membuat "Master Image" aplikasi.                                        |
| **Run**   | `docker run --network=pg-network taxi_ingest:v001 ...` | Menjalankan proses ingestion di dalam ekosistem Docker yang terisolasi. |

> **📝 Note:** Jangan lupa sertakan flag `--network=pg-network`. Tanpa ini, script kita akan "buta" dan tidak bisa menemukan database meskipun namanya sudah benar.

---

### Standar Industri: Alur Kerja Data Engineer

Saya merangkum jalur karir seorang DE dalam empat langkah dari materi ini:

1. **Explore:** Eksperimen data di Jupyter Notebook (`.ipynb`).
2. **Refactor:** Ubah jadi script Python bersih (`.py`) dengan parameter dinamis.
3. **Containerize:** Bungkus semuanya ke dalam Dockerfile.
4. **Deploy:** Jalankan di server/cloud menggunakan Docker.

---

### 📌 Summary

Proses _Containerizing_ ini memberikan jaminan **Reproducibility**. Tidak ada lagi drama "di laptop saya jalan, di server kok error?". Dengan Docker, lingkungan kerja kita sudah terkunci rapat dan aman.

> **Insight Pribadi:** Ternyata, inti dari Data Engineering bukan cuma soal kodingan, tapi soal membangun "pipa" infrastruktur yang rapi, otomatis, dan tahan banting.

---

Gak nyangka, akhirnya sampai juga di penghujung **Modul 1: Introduction to Docker**. Kalau sebelumnya saya merasa seperti "tukang" yang harus narik kabel dan nyalain mesin satu-satu, di materi **Docker Compose** ini saya merasa naik level jadi seorang **Architect**.

Berikut adalah catatan penutup saya untuk Modul 1, fokus pada efisiensi dan otomasi infrastruktur.

---

# 🎼 09- Docker Compose

> **Topik:** _Infrastructure as Code (IaC) for Local Development_

### Konsep Utama: Kenapa Harus Compose?

Saya sangat menghargai prinsip **Infrastructure as Code (IaC)**. Daripada ngetik perintah `docker run` yang panjangnya kayak kereta api setiap kali mau mulai kerja, saya cukup menulis "resep master" di satu file.

> **Analogi:** Saya bikin _blueprint_ (file YAML), lalu robot (Docker Compose) yang bakal beliin servernya, masang kabel LAN-nya, dan nyalain semuanya buat saya.

---

### Bedah File `docker-compose.yaml`

Menulis YAML itu gampang-gampang susah. Satu aturan maut yang saya catat: **Spasi adalah segalanya!**

- **Indentasi:** Jangan pernah pakai `Tab`, harus pakai `Double Space`. Kalau spasi salah, Docker bakal bingung dan error.
- **Services:** Di sini tempat saya daftar aplikasi apa saja yang mau dijalankan (Postgres, pgAdmin, dll).
- **Automatic Networking:** Ini fitur paling "magic". Semua kontainer yang ada di file yang sama otomatis bisa saling mengobrol pakai nama servisnya tanpa perlu saya buat network manual lagi.

> **📝 Note:** Di dalam Compose, `pgdatabase` bukan cuma nama, tapi juga alamat (Hostname). Ini yang bikin hidup Data Engineer jauh lebih mudah.

---

### Cheat Sheet: Lifecycle Management

Ini adalah perintah harian yang wajib saya hafal di luar kepala:

| Perintah                 | Apa yang Terjadi?                                                                     |
| ------------------------ | ------------------------------------------------------------------------------------- |
| `docker-compose up`      | Nyalain semua sistem (saya bisa lihat log-nya langsung).                              |
| `docker-compose up -d`   | **Detached mode**. Nyalain semua di background, terminal tetap bisa dipakai.          |
| `docker-compose down`    | Matiin dan hapus kontainer. Bersih total!                                             |
| `docker-compose down -v` | Matiin sistem **DAN** hapus data (Volume). Gunakan hanya kalau mau reset DB dari nol. |

---

### Menghubungkan Script Ingestion ke Compose

Satu hal teknis yang saya pelajari: Docker Compose otomatis bikin nama network sendiri. Biasanya formatnya `[NAMA_FOLDER]_default`.

- Jadi, kalau saya mau jalankan script `ingest_data.py` dari luar Compose tapi mau nyambung ke Postgres yang di dalam Compose, saya harus pakai nama network tersebut.

> **📝 Note:** Selalu cek nama network pakai `docker network ls` sebelum menjalankan kontainer ingestion agar tidak terjadi "Connection Error".

### 📌 Summary

Modul 1 ini mengajarkan saya bahwa Data Engineering bukan cuma soal _coding_, tapi soal membangun **Infrastruktur yang Reproducible**. Dengan Docker Compose, saya punya "pabrik" data yang bisa saya bawa kemana saja, jalankan di OS apa saja, dan hasilnya akan selalu sama.

---
