# 🚀 de-zoomcamp2026-learning-journey

**Penyelenggara:** [DataTalks.Club](https://github.com/DataTalksClub/data-engineering-zoomcamp)

![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/images/bg-de_zoomcamp.png?raw=true)

Repositori ini adalah dokumentasi perjalanan belajar saya dalam menguasai infrastruktur data modern melalui program **Data Engineering Zoomcamp**. Sebagai seseorang yang sedang memulai karir sebagai **Data Engineer**, proyek ini mencakup implementasi pipeline data dari hulu ke hilir.

---

## 🛠️ Tech Stack

Daftar alat dan teknologi yang dipelajari dan diimplementasikan:

- **Cloud:** Google Cloud Platform (GCP) - GCS, BigQuery
- **Infrastructure as Code:** Terraform
- **Containerization:** Docker & Docker Compose
- **Workflow Orchestration:** Kestra / Mage / Airflow
- **Data Warehouse:** BigQuery
- **Analytics Engineering:** dbt (data build tool)
- **Batch Processing:** Apache Spark (PySpark)
- **Stream Processing:** Kafka
- **Programming:** Python & SQL

---

## 📚 Daftar Modul & Materi

### 🔹 Modul 1: Containerization & Infrastructure as Code

Fokus pada persiapan lingkungan kerja dan otomatisasi infrastruktur.

- Setup Google Cloud Platform (GCP) & Cloud SDK.
- Automasi resource cloud (Bucket & Dataset) menggunakan **Terraform**.
- Menjalankan PostgreSQL dan pgAdmin di dalam **Docker**.
- Ingesting dataset (NY Taxi Data) ke Postgres menggunakan Python.

### 🔹 Modul 2: Workflow Orchestration

Mengelola alur kerja data secara otomatis dan teratur.

- Pengenalan konsep orchestration.
- Membuat pipeline ETL (Extract, Transform, Load).
- Mengatur penjadwalan (scheduling) dan backfilling data.
- Menghubungkan orchestrator dengan Google Cloud Storage.

### 🔹 Modul 3: Data Warehouse (BigQuery)

Mempelajari penyimpanan data skala besar dan optimasi query.

- Arsitektur BigQuery dan cara kerjanya.
- Implementasi **Partitioning** dan **Clustering** untuk efisiensi biaya/performa.
- Best practices dalam pengelolaan Data Warehouse.

### 🔹 Modul 4: Analytics Engineering

Mengubah data mentah menjadi data siap pakai untuk analisis.

- Dasar-dasar **dbt (data build tool)**.
- Data modeling (Staging, Core, Models).
- Menjalankan pengujian data (Testing) dan dokumentasi otomatis.
- Visualisasi data

### 🔹 Modul 5: Data Platforms (Bruin)

Fokus pada pembangunan dan pengelolaan platform data modern yang mendukung pemrosesan dalam skala besar.

- Konsep dan arsitektur platform data modern.
- Pengenalan **Bruin** sebagai platform data terpusat untuk orkestrasi, penyimpanan, dan pemrosesan data.
- Cara mengelola dataset, pipeline, serta job dalam Bruin.
- Integrasi Bruin dengan layanan penyimpanan dan komputasi di cloud.
- Praktik terbaik dalam manajemen data, versioning, dan monitoring pipeline.

### 🔹 Modul 6: Batch Processing

Mengelola pemrosesan data dalam volume besar secara berkala.

- Pengenalan Apache Spark (Framework komputasi terdistribusi).
- Operasi DataFrames dan SQL untuk manipulasi data.
- Mekanisme internal GroupBy dan Joins (Shuffle, Partisi).

### 🔹 Modul 7: Stream Processing

Mengelola aliran data secara real-time.

- Arsitektur **Kafka** (Producer, Consumer, Topics).
- Operasi Kafka Streams dan KSQL untuk pemrosesan data.
- Manajemen Schema dengan Avro (Serialisasi dan evolusi data).

### 🔹 Capstone Project

Membangun proyek akhir yang mengintegrasikan semua materi dari Modul 1 sampai 6 untuk menyelesaikan masalah data di dunia nyata.

## 📅 Kurikulum & Progres

| Minggu  | Topik                                          | Status |             Folder/Link              |
| :------ | :--------------------------------------------- | :----: | :----------------------------------: |
| Week 1  | Intro & Prerequisites (Docker, Terraform, GCP) |   ✅   |    [Lihat](/01-docker-terraform/)    |
| Week 2  | Workflow Orchestration                         |   ✅   | [Lihat](/02-workflow-orchestration/) |
| Week 3  | Data Warehouse (BigQuery)                      |   ✅   |     [Lihat](/03-data-warehouse/)     |
| Week 4  | Analytics Engineering (dbt)                    |   ✅   | [Lihat](/04-analytics-engineering/)  |
| Week 5  | Data Platforms (Bruin)                         |   ✅   |     [Lihat](/05-data-platforms/)     |
| Week 6  | Batch Processing (Spark)                       |   ✅   |    [Lihat](/06-batch-processing/)    |
| Week 7  | Stream Processing (Kafka)                      |   ✅   |       [Lihat](/07-streaming/)        |
| Project | Capstone Project 1                             |   📅   |                  -                   |

> _Ket: ✅ Selesai | 🚧 Sedang Dikerjakan | 📅 Rencana_

---
