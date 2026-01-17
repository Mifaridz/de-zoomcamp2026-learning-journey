# 🐳 01-Introduction to Docker

> **Topik:** Containerization Fundamentals
> **Konteks:** Data Engineering Infrastructure
> **Status:** Completed ✅

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
