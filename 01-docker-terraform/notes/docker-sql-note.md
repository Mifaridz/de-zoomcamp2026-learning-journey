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

### 📌 Summary (Rangkuman Akhir)

Docker bukan cuma soal instalasi software, tapi soal cara kita membungkus seluruh environment kerja supaya rapi. Poin pentingnya adalah penggunaan _Image_ untuk menghemat space dan selalu pakai flag _--rm_ pas lagi testing supaya sampah container nggak numpuk di laptop.

> **💡 Note:** _Docker memisahkan antara compute (container) dan storage (volume). Ini adalah prinsip dasar infrastruktur data yang modern._

---

# 🐍 02-Virtual Environments and Data Pipelines

> **Topik:** _Virtual Environments & Build My First Pipeline_

### Setting Up "Kandang" (Environment)

Masalah klasik pada saat menjalakan python dengan project yang berbeda adalah seringnya _library_ yang tabrakan. Jadi saat akan membuat sebuah project alahkah baiknya melakukan setting Environment terlebih dahulu dan list _library_ apa saja yang akan digunakan.

- **Wajib Pakai Virtual Env:** Jangan pernah install apapun di Python global. Titik.
- **Tool Pilihan: `uv**`: Ini *game changer*. Jauh lebih ngebut dibanding `pip`atau`conda`karena dibuat pake Rust. Gunakan `_curl -LsSf https://astral.sh/uv/install.sh | sh_`untuk install`uv`jika menggubakan`WSL` karena terhalang lincense.
- **Highlight Perintah Penting:**
- `uv init --python=3.13`: Bikin pondasi project baru.
- `uv add pandas pyarrow`: Masukin "bumbu" (library) yang kita butuhin.
- `uv run python script.py`: Cara "aman" jalanin script biar nggak nyari library ke mana-mana.

> **💡 Note:** `uv run` itu praktis banget karena dia otomatis nge-sync environment kita sebelum script jalan. Gak ada lagi drama "ModuleNotFoundError".

---

### Anatomy of a Pipeline

Saya belajar kalau pipeline itu nggak harus ribet. Esensinya cuma tiga: **Input → Proses → Output**.

- **Input:** Download data (CSV/JSON) dari internet.
- **Proses:** Di sini Pandas main peran. Kita transform data mentah jadi siap pakai.
- **Output:** Simpan ke database (Postgres) atau file yang lebih canggih (Parquet).
- **Dynamic Scripting:** Pake `sys.argv` supaya script kita nggak kaku. Jadi bisa input argumen (misal: tanggal data) lewat terminal tanpa harus edit file `.py`-nya terus-terusan.

> **💡 Note:** Jangan lupa pake `df.head()` buat _sanity check_ di tengah jalan, biar kita tau datanya beneran ada atau nggak sebelum diproses lebih jauh.

---

### Data Format: Parquet is King!

Dulu taunya cuma CSV, sekarang baru ngeh kenapa orang DE suka **Parquet**.

- **Highlight:** Parquet itu format _columnar_. Efeknya? Ukuran file jadi jauh lebih kecil (dikompresi) dan baca datanya jauh lebih kenceng daripada CSV yang baris demi baris.

> **💡 Note:** _Don't be a messy dev!_ Langsung tambahin `*.parquet` di `.gitignore` biar repository Git kita tetep bersih dari file data yang berat.

---

### 📌 Summary (Rangkuman Akhir)

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

| Langkah   | Perintah                                          | Catatan Saya                                                         |
| --------- | ------------------------------------------------- | -------------------------------------------------------------------- |
| **Build** | `docker build -t pipeline-data:v1 .`              | Jangan lupa **titik (.)** di akhir! Itu artinya folder saat ini.     |
| **Run**   | `docker run -it --rm pipeline-data:v1 2026-01-18` | `2026-01-18` akan ditangkap sebagai argumen oleh script Python saya. |

---

### 📌 Summary

Memasukkan pipeline ke dalam Docker merupakan **standarisasi** untuk setiap tugas "_Image_" atau project yang akan dijalankan. Dengan teknik _Layer Caching_, proses _development_ jadi jauh lebih cepat.

**Insight Penting:** Penggunaan `ENTRYPOINT` membuat container berperilaku seperti aplikasi _executable_. Kita tinggal panggil nama image-nya dan masukkan argumen yang kita mau di belakangnya.

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

### Jebakan Batman: Localhost vs Docker Network

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

### 📌 Summary (Rangkuman Akhir)

Inti dari materi ini adalah **Pemisahan antara Compute dan Storage**. Container boleh mati atau diganti kapan saja (`--rm`), asalkan datanya sudah kita ikat ke folder lokal lewat **Bind Mount**. Dengan menggunakan `uv --dev`, manajemen _tools_ pembantu (seperti `pgcli`) juga jadi jauh lebih bersih di mata seorang _developer_.

**Insight Pribadi:** Ternyata mengelola database bisa semudah menjalankan satu perintah Docker. Tidak perlu install macem-macem secara permanen di Windows/Mac.

---
