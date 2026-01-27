# 🎻 1-Intro to Workflow Orchestration

> **Topik:** _Managing Complex Data Pipelines with Kestra_

### Analogi: Dirigen dan Partitur Musik

Saya sangat suka analogi ini karena sangat masuk akal untuk pemula:

- **Musisi (Tools):** Script Python kita, Docker, atau SQL query. Mereka jago di bidang masing-masing.
- **Partitur (Workflow):** Urutan langkah yang harus dijalankan.
- **Dirigen (Orchestrator):** Alat seperti **Kestra**. Dia tidak "memainkan musik" sendiri, tapi dia yang memastikan pemain drum selesai dulu baru biola masuk.

> **📝 Note :** Inti dari Orchestration adalah **Control**. Kita nggak mau script Transform jalan kalau script Extract-nya ternyata gagal. Orchestrator-lah yang menjaga "harmoni" ini.

---

### DAG (Directed Acyclic Graph)

Dalam dunia DE, alur kerja kita sering digambarkan sebagai **DAG**. Ini adalah peta jalan pipeline kita.

- **Nodes (Kotak):** Tugas atau _Task_ yang harus dikerjakan.
- **Edges (Panah):** Urutan atau ketergantungan (_Dependency_).

**Tugas Utama Sang "Dirigen" (Orchestrator):**

1. **Scheduling:** Jalanin script tiap jam 3 pagi secara otomatis.
2. **Dependency Management:** Memastikan urutan (E → T → L) benar.
3. **Error Handling:** Kalau gagal, coba lagi (_Retry_) atau lapor ke Slack/Email.
4. **Logging:** Mencatat semua kejadian buat bahan _debugging_ kalau ada masalah.

---

### Kenapa Pakai Kestra?

Sebagai seseorang yang baru belajar Docker Compose, saya merasa beruntung pakai Kestra karena:

- **Declarative (YAML):** Cara konfigurasinya mirip banget sama `docker-compose.yaml`. Gak perlu belajar bahasa pemrograman baru yang ribet buat bikin _workflow_.
- **Modern & Event-Driven:** Dia bisa jalan bukan cuma karena jadwal, tapi juga karena ada "kejadian" (misal: ada file baru masuk ke folder).
- **Full ETL Support:** Sangat mendukung proses _Extract, Transform, dan Load_ yang sudah kita pelajari.

---

### 📌 Summary

Modul 2 ini adalah soal **Otomatisasi**. Saya belajar bahwa di dunia nyata, seorang Data Engineer tidak mungkin menjalankan script manual setiap hari. Kita butuh "Partitur" (Workflow) dan "Dirigen" (Kestra) untuk memastikan ribuan baris data mengalir dengan selamat dari sumber ke database tujuan tanpa campur tangan manusia secara terus-menerus.

---
