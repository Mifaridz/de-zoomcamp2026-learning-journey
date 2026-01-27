# 🎻 1-Intro to Workflow Orchestration

> **Topik:** _Managing Complex Data Pipelines with Kestra_

### Analogy: Conductor and Music Score

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

# 🕹️ 2-Membangun Pusat Kendali (Kestra Setup)

> **Topik:** _Orchestration Architecture & Programmatic Workflows_

### Arsitektur Kestra: Kenapa Butuh Postgres?

Saya mencatat satu hal penting: Kestra adalah aplikasi **Stateless**, sedangkan Postgres adalah **Stateful**-nya.

- **Kestra Server:** Menjalankan logika, memantau jadwal, dan mengirim perintah.
- **Postgres Database:** Tempat Kestra menyimpan "ingatan". Semua _Flow_ yang kamu buat, _Log_ setiap percobaan, dan status _Task_ (berhasil/gagal) disimpan di sini.
- **Networking:** Karena keduanya ada di satu file Docker Compose, Kestra bisa memanggil Postgres hanya dengan nama servisnya.

---

### Anatomi Sebuah Flow

Saya belajar bahwa menulis _Flow_ di Kestra itu seperti menyusun instruksi untuk robot:

1. **Flow:** Dokumen master (Satu file YAML).
2. **Task:** Unit kerja terkecil. Di sinilah kita memberi tahu Kestra: "Download file ini", "Jalankan SQL itu".
3. **Triggers:** Bagian yang membuat sistem ini otomatis. Tanpa _Trigger_, _Flow_ hanyalah sekumpulan instruksi yang menunggu tombol klik manual.

---

### Python di Kestra: Isolasi adalah Kunci

Ini adalah fitur favorit saya sebagai _Data Engineer_. kemarin, kita harus pusing memikirkan _library_ Python yang bentrok di server.

- **Plugin `io.kestra.plugin.scripts.python.Script`:** Kestra bisa membuat kontainer Python temporer untuk menjalankan script kita.
- **Dependency Management:** Kita bisa menambahkan `pip install pandas` di dalam YAML-nya langsung. Jadi, lingkungan Python kita selalu bersih dan terisolasi untuk setiap _Task_.

---

### "The Engineer Way": Automasi dengan curl

Kenapa harus pakai terminal kalau ada UI? Materi ini mengajarkan saya cara berpikir seorang _Engineer_ sejati:

- **Manual (UI):** Bagus untuk belajar, coba-coba, dan melihat visualisasi DAG.
- **Programmatic (API/curl):** Wajib dikuasai untuk skala besar. Bayangkan harus memindahkan 100 _Flow_ ke server baru; mengetik perintah `curl` jauh lebih cepat dan minim kesalahan daripada klik-klik manual.

---

### 📌 Summary

Sekarang saya tidak lagi menjalankan script Python secara terisolasi. Saya menjalankannya di dalam sebuah **Ecosystem**. Kestra memberikan saya visibilitas penuh: jika script Python saya gagal, saya bisa lihat log-nya langsung di dashboard, tahu jam berapa gagalnya, dan bisa klik _Retry_ dengan satu tombol.

> **📝 Note :** Ternyata, orkestrasi itu soal **Visibilitas** dan **Kontrol**. Semakin kita tahu apa yang terjadi di dalam "pipa" data kita, semakin mudah kita memperbaikinya.

---
