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

### 🛠️ Setting Up "Kandang" (Environment)

Masalah klasik pada saat menjalakan python dengan project yang berbeda adalah seringnya _library_ yang tabrakan. Jadi saat akan membuat sebuah project alahkah baiknya melakukan setting Environment terlebih dahulu dan list _library_ apa saja yang akan digunakan.

- **Wajib Pakai Virtual Env:** Jangan pernah install apapun di Python global. Titik.
- **Tool Pilihan: `uv**`: Ini *game changer*. Jauh lebih ngebut dibanding `pip`atau`conda`karena dibuat pake Rust. Gunakan `_curl -LsSf https://astral.sh/uv/install.sh | sh_`untuk install`uv`jika menggubakan`WSL` karena terhalang lincense.
- **Highlight Perintah Penting:**
- `uv init --python=3.13`: Bikin pondasi project baru.
- `uv add pandas pyarrow`: Masukin "bumbu" (library) yang kita butuhin.
- `uv run python script.py`: Cara "aman" jalanin script biar nggak nyari library ke mana-mana.

> **💡 Note:** `uv run` itu praktis banget karena dia otomatis nge-sync environment kita sebelum script jalan. Gak ada lagi drama "ModuleNotFoundError".

---

### 🚀 Anatomy of a Pipeline

Saya belajar kalau pipeline itu nggak harus ribet. Esensinya cuma tiga: **Input → Proses → Output**.

- **Input:** Download data (CSV/JSON) dari internet.
- **Proses:** Di sini Pandas main peran. Kita transform data mentah jadi siap pakai.
- **Output:** Simpan ke database (Postgres) atau file yang lebih canggih (Parquet).
- **Dynamic Scripting:** Pake `sys.argv` supaya script kita nggak kaku. Jadi bisa input argumen (misal: tanggal data) lewat terminal tanpa harus edit file `.py`-nya terus-terusan.

> **💡 Note:** Jangan lupa pake `df.head()` buat _sanity check_ di tengah jalan, biar kita tau datanya beneran ada atau nggak sebelum diproses lebih jauh.

---

### 📄 Data Format: Parquet is King!

Dulu taunya cuma CSV, sekarang baru ngeh kenapa orang DE suka **Parquet**.

- **Highlight:** Parquet itu format _columnar_. Efeknya? Ukuran file jadi jauh lebih kecil (dikompresi) dan baca datanya jauh lebih kenceng daripada CSV yang baris demi baris.

> **💡 Note:** _Don't be a messy dev!_ Langsung tambahin `*.parquet` di `.gitignore` biar repository Git kita tetep bersih dari file data yang berat.

---

### 📌 Summary (Rangkuman Akhir)

Hari ini saya berhasil bikin pipeline Python sederhana yang bisa nerima argumen terminal. Inti dari materi ini bukan cuma soal nulis kode, tapi soal **standardisasi**. Pake `uv` buat ngatur dependensi, pake `sys.argv` buat bikin script fleksibel, dan milih format `Parquet` buat efisiensi.

---
