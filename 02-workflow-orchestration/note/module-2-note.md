# 🎻 2-Introduction to Workflow Orchestration

> **Topik:** Fondasi Orkestrasi Workflow & Pengenalan Kestra

Dalam data engineering modern, workflow orchestration adalah bagian penting untuk memastikan pipeline berjalan **teratur**, **otomatis**, dan **dapat dipantau**.
Kalau di Module-01 kita belajar membungkus environment dengan Docker, di module ini saya belajar **mengorkestrasi** tugas-tugas yang menggunakan environment tersebut.

Saya suka melihat konsep ini seperti **orkestra musik**:

- Instrumen = berbagai tools (database, script Python, API, storage, dsb)
- Konduktor = orchestrator
- Lagu = workflow

Tanpa konduktor, semua instrumen bisa jalan sendiri-sendiri tanpa koordinasi. Sama seperti pipeline data yang bisa kacau kalau dijalankan manual satu per satu.

## **2.1.1 - What is Workflow Orchestration?**

Workflow orchestration adalah proses mengatur serangkaian tugas agar berjalan dalam urutan yang benar, dengan dependensi yang tepat, serta dapat dipantau dan dijalankan otomatis.

Beberapa hal yang bisa dilakukan orchestrator:

- Menjalankan workflow yang terdiri dari beberapa langkah (tasks)
- Memantau dan mencatat log, termasuk error handling
- Menjalankan workflow otomatis berdasarkan **schedule (cron)** atau **event**
- Mengatur pergerakan data dari satu sistem ke sistem lain
- Memberikan observability (run history, retry mechanism, alert, dsb)

### Mengapa Orchestration Penting di Data Engineering?

- **Automasi:** Menghilangkan proses manual yang rawan error
- **Reliabilitas:** Pipeline tetap jalan walaupun kita tidak mengawasi secara langsung
- **Visibility:** Kita bisa melihat step mana yang gagal dan kenapa
- **Reproducibility:** Setiap run bersifat konsisten dan bisa ditelusuri

Seringkali pipeline ETL terdiri dari banyak komponen: pengambilan data, transformasi, validasi, hingga load ke data warehouse. Mengatur semua itu secara manual akan sangat melelahkan. Di sinilah workflow orchestration menjadi solusi.

---

## **2.1.2 - What is Kestra?**

Kestra adalah **platform workflow orchestration open-source** yang bersifat **infinitely scalable**, memungkinkan kita menjalankan workflow dalam skala kecil hingga enterprise.

Kestra sangat fleksibel karena:

- Bisa dibangun dengan **Flow as Code (YAML)**
- Bisa digunakan secara **no-code** melalui UI
- Bisa dibantu dengan **AI Copilot** untuk menulis task
- Mendukung **semua bahasa pemrograman** (Python, Bash, SQL, dsb)
- Memiliki lebih dari **1000 plugin** untuk integrasi dengan tool modern
- Bisa berjalan dengan **schedule** atau **event-trigger**

Dari pengalaman saya mempelajari berbagai orchestrator (Airflow, Prefect, Dagster), Kestra memiliki learning curve yang paling bersahabat karena konsepnya sederhana: **flow → task → trigger**.

Hal yang paling membantu adalah:

- UI sangat intuitif
- YAML flow mudah dibaca
- Observability kuat (log, graph, execution timeline)
- Mudah di-deploy (lokal maupun cloud)

### Kapan Kita Memakai Kestra?

- Ingin menjalankan pipeline ETL otomatis
- Perlu memonitor setiap langkah pipeline
- Butuh retry, timeout, error handling, dan notifikasi
- Ingin pipeline berjalan saat ada event tertentu (misal: file baru masuk ke bucket)
- Menghubungkan banyak sistem secara terkoordinasi

Module ini akan membuat saya lebih memahami cara membangun workflow ETL nyata menggunakan Kestra sebagai pusat kendalinya.

---

## 📚 Apa yang Berhasil Saya Pelajari

- **Konsep orkestrasi sangat mirip orkestra musik**, sehingga mudah dipahami: setiap tools perlu “dipimpin” agar sinkron.
- **Data pipeline butuh orchestrator** supaya tiap langkah berjalan dalam urutan yang tepat dan mudah dimonitor.
- **Kestra sangat fleksibel**—bisa menggunakan YAML, UI, atau AI Copilot.
- **Flow Kestra mudah dipahami** karena struktur YAML-nya jelas dan terstandarisasi.
- **Integrasi plugin yang banyak** membantu menghubungkan pipeline ke database, cloud storage, API, dan tools lainnya tanpa membuat script dari nol.
- **Kestra mendukung event-based trigger**, fitur penting yang sering muncul dalam real-world pipeline (misalnya saat data baru masuk ke S3/GCS).

Saya juga makin paham bahwa orchestrator bukan sekadar penjadwal task, tetapi tempat di mana pipeline bisa diaudit, diulang, dan dilacak secara historis — elemen penting dalam dunia data engineering modern.

---

## 📌 Summary

Workflow orchestration adalah inti dari data pipeline modern karena memberikan **struktur, otomasi, dan observability**.
Kestra menjadi pilihan yang tepat karena fleksibel, powerful, dan mudah dikembangkan baik untuk pemula maupun engineer berpengalaman.

> **📝 Note:** _Di dunia modern data platform, pipeline tidak hanya perlu berjalan — tetapi harus bisa di-monitor, diulang, diperbaiki, dan ditrigger secara otomatis. Orchestrator seperti Kestra adalah kuncinya._

---

# 🚀 2.2-Getting Started with Kestra

> **Topik:** Instalasi Kestra, Konsep Utama Kestra, dan Menjalankan Python Script di dalam Workflow

---

## **2.2.1 – Installing Kestra**

Untuk menjalankan Kestra secara lokal, saya menggunakan **Docker Compose**, sama seperti kita menggunakan Postgres + pgAdmin di Module 01. Bedanya, sekarang kita menambahkan dua service baru:

1. **Kestra Server**
2. **Kestra Database (Postgres)**

### Kenapa Kestra Butuh Postgres?

Kestra menyimpan:

- definisi flow,
- hasil execution,
- logs,
- metadata lainnya

semuanya di database relational.
Karena di Module 01 kita sudah punya Postgres, kita hanya perlu menyesuaikan konfigurasi agar tidak bentrok port.

### Langkah Instalasi

Masuk ke folder module:

```bash
cd 02-workflow-orchestration
docker compose up -d
```

Setelah kontainer berjalan, saya bisa membuka UI Kestra di:

```
http://localhost:8080
```

Untuk mematikan:

```bash
docker compose down
```

> **Catatan:** Pastikan pgAdmin tidak memakai port yang sama dengan Kestra. Jika bentrok, cek FAQ di README.

---

### **Pengaturan Username & Password**

Saat menambahkan Postgres buat Kestra, jangan lupa mengatur:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`

Ini memastikan Kestra dapat membuat connection pool dengan benar.

Contoh snippet:

```yaml
environment:
  POSTGRES_USER: kestra
  POSTGRES_PASSWORD: kestra123
  POSTGRES_DB: kestra
```

---

### **Menambahkan Flow ke Kestra**

Ada dua cara:

#### 1. Copy-Paste YAML ke Editor UI

Cara cepat untuk belajar dan bereksperimen.

#### 2. Programmatic Upload via API

Cocok untuk CI/CD atau automasi deployment workflow.

Kestra menyediakan API endpoint seperti:

```
PUT /api/v1/flows/{namespace}/{id}
```

yang bisa dipanggil dengan curl / python.

---

## **2.2.2 – Kestra Concepts**

Agar bisa membangun workflow, saya harus mengenal komponen inti dalam Kestra. Berikut konsep yang menurut saya paling fundamental:

| Konsep              | Penjelasan                                                              |
| ------------------- | ----------------------------------------------------------------------- |
| **Flow**            | Wadah utama berisi tasks, trigger, dan logic orkestrasi.                |
| **Tasks**           | Langkah-langkah individual di dalam flow (log, python, http, sql, dsb). |
| **Inputs**          | Nilai dinamis yang bisa diberikan saat flow dijalankan.                 |
| **Outputs**         | Nilai yang dihasilkan oleh task atau flow untuk dipakai task lain.      |
| **Triggers**        | Mekanisme otomatis untuk menjalankan flow (schedule & event-based).     |
| **Execution**       | Satu kali proses run dari flow. Punya status: success, failed, killed.  |
| **Variables**       | Key-value yang bisa dipakai ulang di banyak task.                       |
| **Plugin Defaults** | Default configuration untuk plugin tertentu dalam satu namespace.       |
| **Concurrency**     | Batas maksimal flow yang boleh berjalan sekaligus.                      |

### Contoh “Hello World” Flow (01_hello_world.yaml)

Flow ini menunjukkan hampir seluruh konsep Kestra:

- Ada **5 tasks** → 3 log, 1 sleep, 1 return
- Menggunakan **input `name`**
- Membuat **variable** untuk merangkai pesan sambutan
- Menghasilkan **output** dari task `return`
- Ada **trigger harian** jam 10 pagi
- **Plugin defaults** mengubah level log menjadi ERROR
- Menentukan **concurrency limit = 2** (lebih dari itu akan gagal)

Flow sederhana seperti ini sangat bagus untuk memahami bagaimana Kestra memproses urutan task, menangani input/output, dan menjalankan trigger.

---

## **2.2.3 – Orchestrate Python Code**

Setelah memahami flow dasar, langkah berikutnya adalah menjalankan **Python script** di dalam Kestra. Ini penting karena **Python adalah bahasa utama dalam data engineering**.

### Cara Menjalankan Python di Kestra

Kestra menyediakan dua cara:

1. **Menulis Python langsung di YAML** (inline)
2. **Menjalankan file `.py` dari docker volume**

Ini membuat Kestra fleksibel—saya bisa:

- menulis script kecil langsung di flow, atau
- menjalankan modul Python yang lebih kompleks

Kestra tidak membatasi tools; kita bisa memadukan Python, SQL, Bash, dan plugin lainnya dalam satu pipeline.

---

### **Contoh Python Workflow (02_python.yaml)**

Flow ini mengeksekusi kode Python yang:

- melakukan request ke DockerHub
- mengambil jumlah Docker image pulls
- mengembalikan hasilnya sebagai **output** Kestra
- output tersebut bisa dipakai task berikutnya

Ini menunjukkan bahwa Kestra bukan hanya menjalankan langkah-langkah statis, tetapi juga bisa memproses logika dan operasi dinamis di dalam task.

---

## 📚 Apa yang Berhasil Saya Pelajari

- Instalasi Kestra dengan Docker Compose cukup sederhana asalkan port tidak bentrok.
- Kestra punya konsep yang mirip orchestrator lain (seperti Airflow), tetapi jauh lebih mudah dipahami.
- Flow YAML Kestra itu **clean**, mudah dibaca, dan cepat dibuat ulang.
- Menjalankan Python di dalam flow memberikan fleksibilitas penuh dalam membangun pipeline ETL.
- Output Python bisa dipakai oleh task lainnya—inti dari membangun workflow yang modular.
- Trigger dan concurrency membuat workflow lebih aman, terkontrol, dan otomatis.

---

## 📌 Summary

Bagian ini memberi fondasi untuk bekerja dengan Kestra:

- Instalasi lokal dengan Docker Compose
- Memahami konsep fundamental workflow
- Belajar menambahkan flow secara manual dan via API
- Menjalankan Python script sebagai bagian dari orchestrated workflow

> **📝 Note:** _Kestra bukan hanya alat penjadwalan, tetapi sebuah platform orkestrasi lengkap yang menggabungkan fleksibilitas bahasa pemrograman, plugin, dan kontrol eksekusi—membuat pipeline data lebih rapi, otomatis, dan dapat diaudit._

---

# 🛠️ 2.3-Hands-On Coding Project: Build Data Pipelines with Kestra

> **Topik:** Membangun Pipeline ETL (Yellow & Green Taxi) ke Postgres Lokal

Setelah paham konsep dasar orkestrasi, saatnya saya mempraktikkannya secara langsung. Di bagian ini, fokusnya adalah membangun pipeline ETL untuk data **NYC Taxi (Yellow & Green)**.
Jika di Module-01 saya belajar mengelola database-nya, sekarang saya menggunakan Kestra untuk mengatur aliran datanya secara otomatis.

Rencana besarnya adalah:

- **Extract:** Mengambil data dari file CSV (GitHub).
- **Load:** Memasukkannya ke Postgres lokal (Docker).
- **Automate:** Mencoba scheduling dan backfilling.

---

## **2.3.1 - Getting Started Pipeline**

Sebagai pemanasan, saya mencoba pipeline sederhana untuk memahami bagaimana Kestra bekerja dengan berbagai teknologi dalam satu flow.

Alur kerjanya cukup menarik:

1. **Extract:** Mengambil data melalui HTTP REST API.
2. **Transform:** Mengolah data tersebut menggunakan script Python.
3. **Query:** Melakukan pengecekan data menggunakan DuckDB.

Di tahap ini, saya belajar melihat **Gantt Chart** dan **Logs** di UI Kestra untuk memahami urutan eksekusi dan memantau jika ada error di tiap langkahnya.

---

## **2.3.2 - Local DB: Load Taxi Data to Postgres**

Sebelum melompat ke Cloud (GCP), saya mematangkan pemahaman dengan menggunakan database Postgres lokal yang berjalan di Docker (menggunakan file _Docker Compose_ yang sama dari Module-01).

**Alur Pipeline Taxi Data:**

- **Partitioning:** Data diambil berdasarkan tahun dan bulan.
- **Table Management:** Kestra akan membuat tabel secara otomatis jika belum ada.
- **Loading:** Data dari CSV dimuat ke tabel bulanan, lalu di-_merge_ ke tabel utama (destination table).

> **💡 Catatan Penting tentang Data:**
> Meskipun TLC menyediakan format Parquet, di materi ini saya menggunakan **CSV**. Kenapa? Karena CSV jauh lebih mudah diintip isinya (pake teks editor atau Excel) bagi saya yang baru mulai belajar, sehingga proses _debugging_ jadi lebih simpel.

---

## **2.3.3 - Learn Scheduling and Backfills**

Nah, di sinilah kekuatan asli orchestrator terlihat. Saya mencoba menjalankan pipeline secara otomatis dan menangani data masa lalu.

- **Scheduling:** Saya mengatur agar pipeline jalan otomatis setiap hari jam **09:00 AM UTC**. Tidak perlu lagi menjalankan script manual tiap pagi!
- **Backfilling:** Ini fitur yang sangat keren. Jika saya punya data tahun 2019 yang belum masuk, saya bisa melakukan "backfill". Kestra akan menjalankan ulang task untuk periode waktu tersebut secara otomatis.

_Contoh kasus:_ Saya mencoba melakukan backfill khusus untuk dataset **Green Taxi tahun 2019**.

---

## 📚 Apa yang Berhasil Saya Pelajari

- **Visibility adalah kunci:** Dengan melihat _Gantt Chart_, saya bisa tahu persis langkah mana yang memakan waktu paling lama.
- **Transisi dari Docker ke Orchestration:** Saya merasa Docker Compose dari Module-01 sangat berguna karena sekarang saya tinggal "menumpangkan" Kestra di atas infrastruktur yang sudah ada.
- **Memahami pentingnya format data:** Saya belajar bahwa dalam belajar, fungsionalitas lebih penting daripada kecanggihan format (memilih CSV daripada Parquet agar lebih mudah dipahami).
- **Kekuatan Backfill:** Saya baru sadar betapa repotnya kalau harus memasukkan data histori secara manual. Fitur backfill di Kestra sangat memudahkan pekerjaan Data Engineer saat ada data lama yang perlu diproses ulang.
- **Workflow terintegrasi:** Kestra bisa menggabungkan HTTP request, Python, dan SQL dalam satu file YAML yang rapi.

---

## 📌 Summary

Hands-on kali ini memberikan gambaran nyata bagaimana seorang Data Engineer bekerja sehari-hari: tidak hanya menulis script, tapi mengatur bagaimana script itu berinteraksi dengan API, Database, dan Jadwal rutin.

> **📝 Note:** _Automation bukan cuma soal menjalankan script secara berkala, tapi soal membangun sistem yang bisa mengelola data masa lalu (backfill) dan masa depan (scheduling) dengan konsisten._

---

# ☁️ 2.4-ELT Pipelines in Kestra: Google Cloud Platform

> **Topik:** Migrasi Pipeline ke Cloud (GCS & BigQuery) serta Strategi ELT

Setelah berhasil menjalankan pipeline di environment lokal, sekarang saya melangkah ke level profesional: **Cloud**. Di bagian ini, saya belajar memindahkan data NYC Taxi ke **Google Cloud Platform (GCP)** menggunakan kombinasi maut antara Data Lake (GCS) dan Data Warehouse (BigQuery).

---

## **2.4.1 - ETL vs ELT**

Satu hal besar yang saya pelajari di sini adalah pergeseran paradigma dari ETL ke **ELT**.

- **ETL (Extract, Transform, Load):** Seperti yang saya lakukan di Postgres lokal (materi 2.3). Data diolah dulu (misal pakai Python) baru dimasukkan ke DB.
- **ELT (Extract, Load, Transform):** Pendekatan Cloud-Native. Data mentah di-_load_ dulu ke Storage (GCS), baru proses transformasinya dilakukan langsung di dalam Data Warehouse (BigQuery).

**Kenapa ELT lebih oke di Cloud?**
Karena Cloud punya _infinite scalability_. Daripada komputer lokal saya ngos-ngosan mengolah jutaan baris Yellow Taxi data pakai Python, lebih baik saya lempar datanya ke BigQuery dan biarkan kekuatan komputasi Google yang melakukan transformasi dalam hitungan detik.

---

## **2.4.2 - Setup Google Cloud Platform (GCP)**

Sebelum pipeline bisa jalan, saya perlu melakukan konfigurasi "jembatan" antara Kestra dan GCP.

1. **KV Store (Key-Value):** Saya belajar menggunakan fitur KV Store di Kestra (`06_gcp_kv.yaml`) untuk menyimpan variabel penting seperti `GCP_PROJECT_ID` dan `GCP_BUCKET_NAME`. Ini jauh lebih rapi daripada menuliskannya secara manual di setiap flow.
2. **Resource Provisioning:** Saya menggunakan flow `07_gcp_setup.yaml` untuk membuat bucket GCS dan dataset BigQuery secara otomatis. Ini sangat praktis karena infrastruktur bisa dibuat lewat kode (Infrastructure as Code sederhana).

---

## **2.4.3 - GCP Workflow: Load Taxi Data to BigQuery**

Setelah infrastruktur siap, saya menjalankan proses ELT yang sesungguhnya melalui flow `08_gcp_taxi.yaml`.

Data mengalir dari **GitHub (CSV)** → **GCS (Data Lake)** → **BigQuery (Data Warehouse)**. Di sinilah saya melihat kemudahan plugin Kestra dalam menangani autentikasi dan transfer data antar layanan Google tanpa harus pusing memikirkan koneksi manual yang ribet.

---

## **2.4.4 - Schedule and Backfill Full Dataset**

Di Cloud, batasan _resource_ laptop saya sudah hilang. Saya bisa lebih berani:

- **Complex Scheduling:** Mengatur jadwal berbeda untuk dataset berbeda (Green Taxi jam 09:00, Yellow Taxi jam 10:00).
- **Full Backfill:** Berbeda dengan lokal yang hanya berani _backfill_ sedikit data, di GCP saya bisa melakukan _backfill_ untuk **seluruh dataset histori** tanpa takut storage penuh atau laptop hang. BigQuery dan GCS menangani skalabilitasnya untuk saya.

---

## 📚 Apa yang Berhasil Saya Pelajari

- **Power of ELT:** Saya paham sekarang bahwa kalau datanya besar, biarkan database (warehouse) yang bekerja keras melakukan transformasi, jangan memaksakan script Python lokal.
- **Kestra KV Store:** Fitur ini sangat membantu untuk menjaga kode tetap _clean_. Kalau project ID atau nama bucket berubah, saya cukup ganti di satu tempat (KV Store).
- **Skalabilitas Cloud:** Ada rasa "aman" saat menjalankan pipeline di Cloud. Saya tidak perlu khawatir soal memori laptop atau sisa disk space saat memproses jutaan baris data.
- **Separation of Concerns:** GCS sebagai tempat singgah data mentah (Data Lake) dan BigQuery sebagai tempat data siap pakai (Data Warehouse) adalah arsitektur standar industri yang kini saya kuasai cara orkestrasinya.

---

## 📌 Summary

Migrasi dari lokal ke GCP bukan cuma soal pindah tempat simpan data, tapi soal mengubah strategi dari **ETL ke ELT** untuk memanfaatkan kekuatan Cloud. Dengan Kestra, transisi ini terasa mulus karena kita tetap menggunakan logika YAML yang sama, hanya mengganti plugin targetnya saja.

> **📝 Note:** _Cloud mengubah cara kita berpikir tentang data. Jangan takut memproses data besar, cukup pastikan orkestrasinya efisien dan biarkan infrastruktur cloud menangani bebannya._

---

# 🤖 2.5-Using AI for Data Engineering in Kestra

> **Topik:** AI Copilot, Context Engineering, dan RAG dalam Data Pipeline

Di bagian ini, saya belajar bahwa menjadi Data Engineer di era sekarang bukan berarti harus hafal semua sintaks YAML. Kuncinya adalah bagaimana kita berkolaborasi dengan AI secara cerdas melalui **Context Engineering**. Jika di modul sebelumnya saya fokus pada "cara kerja" pipeline, di sini saya fokus pada "cara mempercepat" pembuatannya.

---

## **2.5.1 - Why AI for Workflows?**

AI bukan untuk menggantikan kita, tapi untuk menghilangkan tugas-tujuan repetitif seperti:

- Menulis _boilerplate_ code (kerangka dasar YAML).
- Mencari dokumentasi plugin yang ribet.
- Mengurangi _human error_ pada penulisan properti.

Namun, saya belajar satu prinsip penting: **AI hanya sebagus konteks yang kita berikan.**

---

## **2.5.2 - Context Engineering: ChatGPT vs Kestra Copilot**

Saya melakukan eksperimen menarik untuk membuktikan pentingnya konteks.

### Eksperimen: ChatGPT Tanpa Konteks

Saat saya meminta ChatGPT membuatkan flow Kestra untuk load data ke BigQuery tanpa data pendukung, hasilnya seringkali:

- **Outdated:** Menggunakan plugin versi lama yang sudah di-rename.
- **Hallucinated:** Mengarang properti yang sebenarnya tidak ada.
- **Error:** Kode tidak bisa langsung dijalankan (perlu banyak perbaikan manual).

**Kenapa?** Karena LLM umum punya _knowledge cutoff_. Mereka tidak tahu update terbaru dari Kestra.

---

## **2.3.3 - AI Copilot di Kestra**

Kestra punya solusi keren bernama **AI Copilot**. Ini adalah asisten yang sudah "dibekali" dokumentasi terbaru Kestra secara _real-time_.

### Cara Setup:

Saya belajar bahwa kita tidak boleh menaruh API Key sembarangan di Git. Cara terbaik adalah lewat environment variabel atau KV Store.

```yaml
services:
  kestra:
    environment:
      KESTRA_CONFIGURATION: |
        kestra:
          ai:
            type: gemini
            gemini:
              api-key: ${GEMINI_API_KEY}
```

**Hasilnya?** Saat saya memasukkan prompt yang sama persis dengan ChatGPT, AI Copilot memberikan YAML yang **siap eksekusi**, menggunakan plugin yang benar, dan mengikuti _best practices_.
**Kesimpulan:** _Context matters!_

---

## **2.5.4 - Bonus: Retrieval Augmented Generation (RAG)**

Ini adalah konsep paling canggih di modul ini. **RAG** adalah teknik untuk memberikan "ingatan jangka pendek" pada AI berdasarkan data yang kita miliki.

### Bagaimana RAG Bekerja di Kestra?

1. **Ingest:** Mengambil dokumen (misal: rilis terbaru Kestra).
2. **Embeddings:** Mengubah teks jadi angka (vektor) agar dipahami mesin.
3. **Store:** Disimpan di KV Store atau Vector DB.
4. **Query:** Saat kita bertanya, AI mencari data yang paling relevan dari penyimpanan tadi sebelum menjawab.

### Perbandingan Hasil:

- **Tanpa RAG:** AI menjawab secara umum, ngawur, atau bilang "saya tidak tahu" tentang fitur terbaru.
- **Dengan RAG:** AI menjawab sangat detail karena dia "membaca" dokumen yang saya berikan sebelum menjawab.

---

## 📚 Apa yang Berhasil Saya Pelajari

- **AI as a Partner:** Saya tidak harus menulis setiap baris YAML dari nol. AI Copilot bisa menangani bagian yang membosankan, sementara saya fokus pada logika flow-nya.
- **Pentingnya Grounding:** Saya belajar bahwa RAG adalah solusi terbaik untuk mengatasi halusinasi AI. Dengan memberikan dokumen asli sebagai referensi, jawaban AI jadi jauh lebih bisa dipercaya.
- **Keamanan API Key:** Jangan pernah melakukan _hardcode_ API Key. Menggunakan `${GEMINI_API_KEY}` di Docker Compose adalah praktik yang lebih aman.
- **Vector Embeddings:** Konsep mengubah teks menjadi vektor untuk pencarian adalah hal baru bagi saya yang sangat berguna untuk pengembangan aplikasi AI ke depannya.

---

## 📌 Summary

Menggunakan AI dalam Data Engineering bukan soal malas, tapi soal **efisiensi**. Dengan **Kestra AI Copilot** dan teknik **RAG**, saya bisa membangun pipeline yang kompleks lebih cepat dan lebih akurat daripada mengandalkan AI umum saja.

> **📝 Note:** _Di masa depan, tugas Data Engineer bukan lagi sekadar menulis kode, tapi mengelola konteks dan data agar AI bisa membantu kita membangun sistem yang lebih besar._

---
