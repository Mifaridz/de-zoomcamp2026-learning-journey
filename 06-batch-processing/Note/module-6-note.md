# 🚀 Module 6 — Batch Processing

> **Topik:** Distributed Data Processing menggunakan Apache Spark

Pada modul kali ini, saya memasuki tahapan yang sangat krusial dalam perjalanan menjadi seorang _Data Engineer_, yaitu **Batch Processing**. Sejauh ini, saya sudah berurusan dengan skrip Python sederhana dan query SQL, tetapi sekarang saya akan belajar bagaimana menangani data dalam skala yang jauh lebih besar menggunakan **Apache Spark**.

Saya menyadari bahwa di dunia industri, volume data tidak selalu bisa ditangani oleh satu komputer saja. Itulah mengapa saya perlu memahami konsep pemrosesan terdistribusi. Di modul ini, saya akan mendalami bagaimana Spark bekerja, mengapa ia menjadi standar industri, dan bagaimana mengintegrasikannya ke dalam sebuah _data pipeline_ yang profesional, mulai dari pengerjaan lokal menggunakan Docker hingga _deployment_ di _cloud_ menggunakan layanan seperti Google Cloud Platform (GCP).

---

# 6.1 Introduction

## 6.1.1 Introduction to Batch Processing

Dalam bagian pembuka ini, saya mempelajari fondasi utama dari pemrosesan data. Hal pertama yang saya tangkap adalah bahwa tidak semua data harus diproses secara instan. Ada dua metode utama yang perlu saya bedakan: **Batch** dan **Streaming**.

### Apa Itu Batch Processing?

Saya memahami bahwa **Batch Processing** adalah metode di mana data dikumpulkan dalam satu kelompok besar (_batch_) selama periode tertentu sebelum akhirnya diproses sekaligus. Data ini bersifat _bounded_ atau memiliki batasan yang jelas, misalnya data transaksi selama satu hari penuh.

**Cara kerjanya:**

1. Data masuk dan dikumpulkan di sebuah penyimpanan (seperti database atau _data lake_).
2. Setelah interval waktu yang ditentukan selesai (misalnya jam 23:59), satu unit pekerjaan (_job_) akan dijalankan.
3. _Job_ tersebut mengambil seluruh data dari titik awal hingga titik akhir interval tersebut, memprosesnya, dan menghasilkan output dataset baru.

### Perbandingan: Batch vs Streaming

Saya mencatat poin penting mengenai perbedaan kedua metode ini untuk memudahkan pemahaman saya di masa depan:

| Fitur                  | Batch Processing                             | Streaming Processing                                      |
| ---------------------- | -------------------------------------------- | --------------------------------------------------------- |
| **Karakteristik Data** | _Bounded_ (Punya batas awal & akhir)         | _Unbounded_ (Terus mengalir tanpa henti)                  |
| **Contoh Riil**        | Data transaksi harian taksi pada 15 Januari. | Sinyal GPS taksi yang dikirim tiap detik saat perjalanan. |
| **Waktu Proses**       | Menit ke Jam (Interval: Harian, Jam-jaman).  | Milidetik ke Detik (_Real-time_).                         |
| **Unit Proses**        | Seluruh dataset dalam satu periode.          | Per kejadian (_event_) atau _micro-batch_.                |

### Frekuensi dan Teknologi

Saya belajar bahwa frekuensi pemrosesan batch yang paling umum di industri adalah **harian (daily)** dan **jam-jaman (hourly)**. Meskipun secara teori kita bisa melakukan batch setiap 5 menit, namun hal itu jarang dilakukan karena kompleksitasnya yang meningkat.

Beberapa teknologi yang saya kenali sebagai alat bantu batch processing antara lain:

- **Python Scripts:** Seperti yang saya lakukan di Minggu ke-1 untuk melakukan ingest CSV ke database.
- **SQL:** Sangat populer karena kemudahannya, terutama jika menggunakan tools seperti **dbt**.
- **Apache Spark:** Inilah bintang utama yang akan saya pelajari minggu ini karena kemampuannya menangani data masif dengan sangat cepat.

### Alur Kerja dan Orkestrasi

Saya memahami bahwa dalam pipeline yang kompleks, kita sering menggabungkan berbagai teknologi. Di sinilah saya membutuhkan **Orchestrator** seperti **Apache Airflow**.

**Contoh alur yang saya bayangkan:**

1. Data mentah (CSV) mendarat di **Data Lake (Google Cloud Storage)**.
2. Skrip Python melakukan pembersihan awal.
3. Job **Spark** melakukan pemrosesan berat (misal: agregasi data jutaan baris).
4. Hasil akhirnya disimpan di **Data Warehouse (BigQuery)** untuk dianalisis.

### Keuntungan dan Kekurangan Batch Processing

Hal menarik bagi saya adalah meskipun teknologi _streaming_ terdengar lebih canggih, faktanya **80-90%** pekerjaan di perusahaan tetap menggunakan _batch_. Mengapa?

**Kelebihan (Kenapa saya harus menyukai Batch):**

- **Mudah Dikelola:** Dengan alat seperti Airflow, saya bisa mendefinisikan langkah-langkah kerja dengan jelas.
- **Retryable (Aman dari Kegagalan):** Jika proses gagal, saya bisa menjalankan ulang (_retry_) dengan aman karena datanya statis.
- **Scalable:** Jika data bertambah besar, saya tinggal menambah jumlah mesin dalam **Cluster** Spark.

**Kekurangan (Risiko yang harus saya mitigasi):**

- **Latensi (Delay):** Data tidak tersedia secara instan. Saya mencatat contoh yang menarik: jika sebuah proses harian baru berjalan setelah hari berakhir dan butuh waktu 20 menit untuk selesai, maka data dari jam pertama kemarin baru bisa dilihat 25 jam kemudian. Ini adalah sesuatu yang harus saya komunikasikan dengan tim bisnis.

---

## 🛠️ Daftar Istilah Penting yang Saya Pelajari

Untuk memastikan saya tidak tersesat dalam materi ini, saya merangkum beberapa istilah teknis yang sering disebutkan:

- **Apache Spark:** Mesin pengolah data terdistribusi yang sangat cepat. Spark memproses data di dalam memori (RAM), bukan di disk, sehingga jauh lebih cepat daripada pendahulunya (Hadoop MapReduce).
- **DataFrame:** Konsep di Spark yang mirip dengan tabel di SQL atau DataFrame di Pandas. Ini adalah struktur data yang memudahkan saya memproses data dalam baris dan kolom.
- **RDD (Resilient Distributed Dataset):** Konsep lama di Spark yang mendasari DataFrame. RDD adalah sekumpulan data yang tersebar di banyak komputer (distribusi) dan tahan banting (_resilient_) jika salah satu komputer mati.
- **Cluster:** Sekumpulan komputer yang bekerja sama untuk memproses tugas yang diberikan oleh Spark. Ada satu "Master" yang membagi tugas dan banyak "Workers" yang mengerjakan tugas tersebut.
- **Google Cloud Storage (GCS):** Penyimpanan awan dari Google. Dalam _data engineering_, GCS sering berperan sebagai **Data Lake**, tempat saya menyimpan file mentah sebelum diproses.
- **Dataproc:** Layanan dari Google Cloud yang memungkinkan saya menjalankan Cluster Spark dengan mudah tanpa harus mengatur server sendiri secara manual.
- **BigQuery:** _Data Warehouse_ milik Google yang sangat cepat untuk melakukan query SQL pada data berskala petabyte. Biasanya menjadi tujuan akhir data yang sudah diproses oleh Spark.

---

### 📌 Summary 6.1.1

Dari pendahuluan ini, saya menyimpulkan beberapa poin utama:

1. **Batch Processing** tetap menjadi tulang punggung dunia _Data Engineering_ karena kestabilan dan kemudahannya dalam penanganan kegagalan.
2. **Delay atau latensi** adalah konsekuensi utama dari batch yang harus diterima oleh bisnis jika ingin biaya yang lebih efisien.
3. **Apache Spark** adalah alat wajib bagi saya untuk menangani pemrosesan batch yang membutuhkan skalabilitas tinggi.
4. **Orkestrasi (seperti Airflow)** adalah "dirigen" yang mengatur kapan dan bagaimana semua teknologi pemrosesan ini bekerja sama secara harmonis.

---

# 🛠️ 6.1 Introduction

## 🐘 6.1.2 Introduction to Spark

Di bagian ini, saya mulai mendalami apa itu **Apache Spark**. Saya belajar bahwa Spark bukan sekadar alat biasa, melainkan sebuah **multi-language engine** yang dirancang khusus untuk mengeksekusi _large-scale data processing_. Baik itu untuk kebutuhan _data engineering_, _data science_, hingga _machine learning_, Spark mampu bekerja pada satu mesin tunggal (_single node_) maupun pada ribuan mesin sekaligus dalam sebuah **Cluster**.

### ⚙️ Spark sebagai sebuah "Engine"

Satu hal yang menarik bagi saya adalah istilah **"Engine"**. Saya memahami bahwa Spark tidak menyimpan data secara permanen. Cara kerjanya adalah:

1. **Pull:** Spark menarik data dari sumbernya (seperti Database atau **Data Lake** di **GCS**).
2. **Process:** Data tersebut dibawa ke mesin-mesin milik Spark (**Executors**) untuk diolah.
3. **Output:** Setelah selesai, hasilnya dikirim kembali ke **Data Lake** atau **Data Warehouse** (seperti **BigQuery**).

### 🏛️ Arsitektur Terdistribusi (Cluster Computing)

Saya belajar bahwa kekuatan utama Spark terletak pada kemampuannya bekerja secara terdistribusi. Dalam sebuah **Cluster**, Spark bisa mengoordinasikan puluhan hingga ribuan mesin untuk bekerja secara paralel.

- **Cluster:** Kumpulan komputer yang saling terhubung untuk menyelesaikan tugas komputasi besar.
- **Master Node:** Bertugas sebagai pengatur lalu lintas dan pembagi tugas.
- **Worker Nodes (Executors):** Mesin-mesin yang melakukan pekerjaan berat memproses data.

### 🐍 Dukungan Multi-Bahasa dan PySpark

Meskipun Spark ditulis menggunakan bahasa **Scala**, saya merasa lega karena Spark memiliki "wrapper" atau dukungan untuk bahasa lain.

- **Scala & Java:** Cara asli dan paling optimal untuk berkomunikasi dengan Spark.
- **Python (PySpark):** Versi yang paling populer di kalangan _Data Engineer_. Saya belajar bahwa PySpark memungkinkan saya menulis kode Python yang kemudian diterjemahkan menjadi instruksi yang dipahami oleh engine Spark.
- **R:** Juga tersedia, meski mungkin tidak sepopuler Python.

### 🔄 Batch vs Streaming di Spark

Meskipun minggu ini saya fokus pada **Batch Processing**, saya baru tahu bahwa Spark juga sangat mumpuni untuk **Streaming**. Konsepnya cukup elegan bagi saya: Spark melihat _stream_ data sebagai urutan _batch-batch_ kecil (_micro-batches_). Teknik pemrosesan yang saya pelajari untuk batch akan sangat berguna jika nanti saya belajar streaming.

### ❓ Kapan Saya Harus Menggunakan Spark?

Ini adalah pertanyaan besar yang terjawab di materi ini. Saya belajar bahwa **SQL** (seperti di **BigQuery** atau Athena) harus menjadi pilihan pertama jika transformasi data bisa dinyatakan dengan query sederhana. Namun, saya akan beralih ke **Spark** ketika:

1. **Fleksibilitas:** Saya butuh logika yang terlalu kompleks untuk ditulis dalam SQL.
2. **Modularity:** Saya ingin membagi kode menjadi modul-modul, menggunakan _unit testing_, dan menerapkan praktik _software engineering_ yang baik.
3. **Machine Learning (ML):** Ini adalah _use case_ favorit saya. Proses _training_ model ML dan penerapannya (_scoring_) pada dataset raksasa seringkali tidak mungkin dilakukan hanya dengan SQL.

---

## 📚 Penjelasan Istilah Teknis (Technical Terms)

Untuk memperdalam pemahaman saya, saya merangkum istilah-istilah teknis yang muncul:

- **Apache Spark:** Framework komputasi terdistribusi yang memproses data di dalam memori (RAM). Ini jauh lebih cepat dibanding **Hadoop MapReduce** yang harus menulis data ke disk di setiap tahapannya.
- **DataFrame:** Abstraksi tingkat tinggi di Spark yang merepresentasikan data dalam bentuk tabel (baris dan kolom). Ini memudahkan saya karena sintaksnya mirip dengan library Pandas di Python atau tabel SQL.
- **RDD (Resilient Distributed Dataset):** Abstraksi dasar Spark sebelum adanya DataFrame. RDD bersifat _low-level_ dan tahan banting (_fault-tolerant_). Jika satu mesin mati, Spark tahu cara membangun kembali bagian data yang hilang di mesin tersebut.
- **Dataproc:** Layanan terkelola dari Google Cloud untuk menjalankan cluster Spark. Saya tidak perlu pusing mengatur server satu per satu; Dataproc melakukannya untuk saya.
- **BigQuery:** _Data Warehouse_ Google tempat saya menyimpan data yang sudah bersih dan siap dianalisis.
- **Google Cloud Storage (GCS):** Tempat penyimpanan file mentah (Data Lake) yang sering menjadi sumber data (_source_) bagi Spark.

---

### 📌 Summary 6.1.2

Berdasarkan apa yang saya pelajari, berikut adalah poin-poin intinya:

1. **Spark adalah Engine:** Ia bertugas menarik, mengolah, dan membuang kembali data ke penyimpanan.
2. **Pemrosesan Terdistribusi:** Kemampuan Spark untuk menjalankan tugas di banyak mesin (**Cluster**) adalah kunci menangani _Big Data_.
3. **PySpark adalah Sahabat DE:** Sebagai pembelajar Python, PySpark adalah jembatan saya untuk menguasai Spark tanpa harus belajar Scala dari nol.
4. **Gunakan Alat yang Tepat:** Gunakan SQL untuk transformasi sederhana di Data Warehouse, dan gunakan Spark untuk logika yang kompleks, modular, atau kebutuhan Machine Learning.
5. **Peningkatan dari Hadoop:** Spark jauh lebih efisien dibanding sistem lama karena memproses data di memori, bukan di disk.

---

# 🐧 6.2 (Optional) Installing Spark (Linux)

Pada bagian ini, saya akan mendalami langkah-langkah teknis untuk melakukan instalasi **Apache Spark** di sistem operasi Linux. Panduan ini sangat fleksibel karena bisa saya terapkan di _Virtual Machine_ (VM) Google Cloud, server Ubuntu lokal, maupun **WSL (Windows Subsystem for Linux)** yang saya gunakan di Windows.

Saya menyadari bahwa Spark memiliki banyak ketergantungan (_dependencies_), jadi urutan instalasi ini sangat krusial agar tidak terjadi error saat menjalankan aplikasi nantinya.

---

### ☕ Langkah 1: Instalasi Java (JDK 11)

Hal pertama yang saya pelajari adalah Spark berjalan di atas **JVM (Java Virtual Machine)**. Namun, saya harus berhati-hati dengan versinya. Meskipun saat ini sudah ada Java 17 atau yang lebih baru, Spark versi 3.0.3 (yang stabil untuk belajar) membutuhkan **JDK 8 atau 11**.

**Mengapa harus JDK 11?**
Versi terbaru Java seringkali belum sepenuhnya kompatibel dengan library internal Spark. Oleh karena itu, saya memilih **OpenJDK 11** karena stabil dan didukung luas di lingkungan Linux.

**Proses yang saya lakukan:**

1. **Download:** Saya mengambil paket OpenJDK dari sumber terpercaya (seperti tautan yang disediakan di dokumentasi kursus).
2. **Ekstrak:** Menggunakan perintah `tar -xvf`, saya mengekstrak file tersebut ke folder khusus, misalnya di `~/spark`.
3. **Konfigurasi `JAVA_HOME`:** Ini adalah langkah paling penting. Saya harus memberitahu sistem di mana letak Java berada.

```bash
export JAVA_HOME="${HOME}/spark/jdk-11.0.1"
export PATH="${JAVA_HOME}/bin:${PATH}"

```

---

### 🔥 Langkah 2: Instalasi Apache Spark

Setelah Java siap, saya melanjutkan ke instalasi Spark itu sendiri. Saya memilih **Spark 3.0.3** dengan paket yang sudah di-_build_ untuk **Hadoop 3.2**.

**Mengapa Hadoop 3.2?**
Meskipun saya mungkin tidak menginstal cluster Hadoop secara penuh, Spark menggunakan library Hadoop untuk berinteraksi dengan sistem penyimpanan seperti **GCS (Google Cloud Storage)** atau S3. Memilih versi yang sesuai memastikan komunikasi data berjalan lancar.

**Proses yang saya lakukan:**

1. **Download:** Menggunakan perintah `wget` untuk mengambil file `.tgz` langsung ke server.
2. **Ekstrak:** Kembali menggunakan `tar` untuk mengeluarkan isi folder Spark.
3. **Konfigurasi `SPARK_HOME`:** Sama seperti Java, saya harus mendaftarkan path Spark ke sistem agar perintah `spark-shell` atau `pyspark` bisa dikenali dari direktori mana pun.

```bash
export SPARK_HOME="${HOME}/spark/spark-3.0.3-bin-hadoop3.2"
export PATH="${SPARK_HOME}/bin:${PATH}"

```

---

### 📝 Langkah 3: Mengatur Environment Variables di `.bashrc`

Saya tidak ingin mengetik perintah `export` di atas setiap kali saya masuk ke terminal. Oleh karena itu, saya menyimpannya secara permanen di file **`.bashrc`**.

**Apa itu `.bashrc`?**
Ini adalah skrip yang dijalankan setiap kali saya membuka sesi terminal baru. Dengan memasukkan variabel path ke sini, sistem saya akan selalu "ingat" di mana letak Java dan Spark.

**Yang saya tambahkan di akhir file `.bashrc`:**

```bash
export JAVA_HOME="${HOME}/spark/jdk-11.0.1"
export PATH="${JAVA_HOME}/bin:${PATH}"

export SPARK_HOME="${HOME}/spark/spark-3.0.3-bin-hadoop3.2"
export PATH="${SPARK_HOME}/bin:${PATH}"

```

Setelah itu, saya menjalankan `source ~/.bashrc` untuk memuat ulang konfigurasinya tanpa harus _restart_ mesin.

---

### 🐍 Langkah 4: Konfigurasi PySpark untuk Jupyter Notebook

Karena saya lebih nyaman menggunakan Python daripada Scala, saya perlu menghubungkan Spark dengan **Jupyter Notebook**. Di sini saya belajar tentang variabel **`PYTHONPATH`**.

**Fungsi `PYTHONPATH`:**
Variabel ini memberitahu Python untuk mencari library di luar folder standar. Saya harus mengarahkan Python ke folder `python` di dalam `SPARK_HOME` agar saya bisa melakukan `import pyspark`.

**Tambahan di `.bashrc` untuk PySpark:**

```bash
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9-src.zip:${SPARK_HOME}/python:${PYTHONPATH}"

```

_Catatan: `py4j` adalah jembatan yang memungkinkan Python memanggil objek Java di dalam Spark._

---

### 📊 Langkah 5: Menjalankan Spark Session dan Memverifikasi Spark UI

Setelah semua terinstal, saya melakukan pengujian sederhana di Jupyter Notebook. Saya membuat sebuah **SparkSession**.

**Apa itu SparkSession?**
Ini adalah "pintu masuk" utama untuk berinteraksi dengan Spark. Di sini saya mendefinisikan konfigurasi aplikasi, seperti:

- **`.master("local[*]")`**: Memberitahu Spark untuk berjalan di mesin lokal menggunakan semua inti CPU (_cores_) yang tersedia.
- **`.appName("test")`**: Memberikan nama pada aplikasi saya agar mudah dipantau.

Satu hal keren yang saya temukan adalah **Spark UI**. Saat Spark sedang berjalan, ia membuka sebuah _web interface_ di **Port 4040**.

- **Fungsi Spark UI:** Saya bisa melihat daftar _jobs_, _stages_, dan _tasks_ yang sedang berjalan. Jika ada proses yang lambat, saya bisa melihat bagian mana dari kode saya yang memakan waktu paling lama di sini.

Jika saya bekerja di VM Cloud, saya harus memastikan melakukan **Port Forwarding** untuk port 8888 (Jupyter) dan 4040 (Spark UI) agar bisa diakses dari browser komputer lokal saya.

---

## 📚 Penjelasan Istilah Teknis (Technical Terms)

Dalam proses instalasi ini, saya menemui beberapa istilah penting:

- **Spark:** Framework untuk pemrosesan data besar secara paralel.
- **DataFrame:** Abstraksi data yang saya gunakan dalam Python (PySpark) yang sangat mirip dengan tabel SQL.
- **RDD (Resilient Distributed Dataset):** Unit data dasar Spark yang bersifat _fault-tolerant_. Saat saya menjalankan `spark-shell`, saya sebenarnya memanipulasi RDD di balik layar.
- **Cluster:** Jika saya nantinya beralih dari `local[*]` ke mode produksi, saya akan menggunakan banyak mesin yang bekerja bersama sebagai satu kesatuan.
- **Google Cloud Storage (GCS):** Saya bisa mengarahkan Spark untuk membaca file langsung dari GCS dengan menambahkan konfigurasi konektor yang tepat.
- **BigQuery:** Hasil akhir dari pemrosesan Spark di Linux ini nantinya bisa saya simpan ke BigQuery untuk kebutuhan pelaporan (_reporting_).

---

### 📌 Summary 6.2

Langkah-langkah yang saya pahami dalam menginstal Spark di Linux meliputi:

1. **Instalasi JDK 11** sebagai prasyarat utama karena Spark berjalan di atas JVM.
2. **Download Spark 3.0.3** yang kompatibel dengan Hadoop 3.2 untuk memastikan konektivitas data yang luas.
3. **Mengatur Environment Variables** di `.bashrc` agar perintah Spark dapat diakses secara global di sistem.
4. **Menghubungkan PySpark ke Jupyter** dengan mengatur `PYTHONPATH` dan menggunakan `SparkSession`.
5. **Memantau eksekusi melalui Spark UI** di port 4040 untuk melihat performa dan detail pekerjaan yang dilakukan oleh cluster lokal saya.

---

# 🛠️ 6.3 Spark SQL and DataFrames

## 🚗 6.3.1 First Look at Spark / PySpark

Pada bagian ini, saya akhirnya mulai "mengotori tangan" dengan menggunakan **PySpark** secara langsung. Saya mempelajari bagaimana memproses dataset yang cukup signifikan, yaitu data _High Volume For-Hire Vehicle_ (HVFHV) dari New York City Taxi. Walaupun ukurannya sekitar 700 MB (bukan _Big Data_ yang sesungguhnya), jumlah barisnya yang mencapai **12 juta baris** sudah cukup untuk melihat kekuatan Spark dibanding alat pemrosesan data biasa.

Berikut adalah pemahaman mendalam yang saya rangkum:

---

### 🐍 Apa itu PySpark?

Saya memahami bahwa **PySpark** adalah Python API untuk **Apache Spark**. Mengingat Spark sendiri dibangun menggunakan bahasa Scala, PySpark bertindak sebagai "jembatan" yang memungkinkan saya menulis kode Python untuk menjalankan tugas pemrosesan data terdistribusi yang sangat berat.

**Hal yang saya pelajari tentang PySpark:**

- **Efisiensi:** Saya bisa tetap menggunakan sintaks Python yang intuitif, sementara di balik layar, Spark mengeksekusi logika tersebut di atas **JVM (Java Virtual Machine)** secara paralel.
- **Skalabilitas:** Kode yang saya tulis di laptop saya hari ini bisa dijalankan di sebuah **Cluster** berisi ribuan mesin tanpa perubahan besar pada logika kodenya.

---

### 🏗️ SparkSession: Pintu Masuk Utama

Langkah pertama yang selalu saya lakukan saat bekerja dengan PySpark adalah membuat sebuah **SparkSession**. Saya mengibaratkan SparkSession sebagai "Panglima" atau "Entry Point" untuk semua fungsionalitas Spark.

**Cara saya membuatnya di notebook:**

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("test") \
    .getOrCreate()

```

**Penjelasan dari perspektif saya:**

- **`.master("local[*]")`**: Saya memberitahu Spark untuk menjalankan tugas secara lokal di komputer saya. Tanda bintang `[*]` sangat penting—ini artinya Spark akan menggunakan **semua core CPU** yang tersedia di mesin saya untuk bekerja secara paralel.
- **`.getOrCreate()`**: Jika sudah ada sesi yang berjalan, Spark akan memberikannya kepada saya. Jika belum, ia akan membuatkan yang baru.

---

### 📂 Membaca Data dengan Spark

Saya mencoba membaca file CSV berukuran besar menggunakan Spark. Di sini saya menemukan perbedaan mencolok antara Spark dan Pandas.

**Temuan saya saat membaca data:**

1. **Infer Schema:** Secara default, Spark tidak secerdas Pandas dalam menebak tipe data. Jika saya hanya melakukan `spark.read.csv()`, semua kolom akan dianggap sebagai **String**.
2. **Schema Manual:** Untuk efisiensi memori, saya belajar bahwa sangat penting bagi seorang Data Engineer untuk mendefinisikan **Schema** secara eksplisit menggunakan `types.StructType`.

**Contoh pendefinisian schema yang saya pelajari:**
Saya harus mengubah tipe data yang tidak efisien (seperti _Long_ yang memakan 8 byte) menjadi _Integer_ (4 byte) jika datanya memang hanya angka bulat kecil.

```python
from pyspark.sql import types

schema = types.StructType([
    types.StructField('hvfhs_license_num', types.StringType(), True),
    types.StructField('dispatching_base_num', types.StringType(), True),
    types.StructField('pickup_datetime', types.TimestampType(), True),
    types.StructField('dropoff_datetime', types.TimestampType(), True),
    types.StructField('PULocationID', types.IntegerType(), True),
    types.StructField('DOLocationID', types.IntegerType(), True),
    types.StructField('SR_Flag', types.StringType(), True)
])

```

---

### 🧩 Konsep Partisi (The Power of Parallelism)

Salah satu pelajaran paling berharga di bagian ini adalah tentang **Partitions**. Saya memahami bahwa Spark membagi data besar menjadi bagian-bagian kecil yang disebut partisi.

**Analogi yang saya gunakan:**
Bayangkan saya punya satu file raksasa dan 8 pekerja (**Executors**). Jika saya tidak membagi file tersebut, hanya 1 pekerja yang sibuk sementara 7 lainnya menganggur (idle).

- **Masalah:** File CSV tunggal seringkali dianggap sebagai satu partisi besar.
- **Solusi:** Saya menggunakan perintah `.repartition(24)`. Ini akan memecah data saya menjadi 24 bagian kecil. Dengan begitu, semua core CPU saya (misal 8 core) bisa bekerja secara bergantian memproses 24 file tersebut secara paralel.

---

### 💾 Menyimpan Data ke Parquet

Setelah data dibaca dan dipartisi, saya belajar untuk menyimpannya ke format **Parquet**.

```python
df.repartition(24).write.parquet('fhvhv/2021/01/')

```

**Mengapa saya harus memilih Parquet?**

- **Kompresi:** Ukuran filenya jauh lebih kecil dibanding CSV karena menggunakan algoritma seperti Snappy.
- **Columnar Storage:** Sangat cepat untuk dibaca oleh alat analitik seperti **BigQuery** karena kita hanya perlu membaca kolom yang dibutuhkan.

---

### 📊 Memantau Lewat Spark UI

Selama proses ini, saya selalu memantau **Spark UI** di port **4040**. Ini membantu saya memahami apa yang terjadi "di bawah kap mesin":

- Saya bisa melihat **Jobs** (tugas besar).
- Saya bisa melihat **Stages** (tahapan kerja, seperti saat melakukan repartition).
- Saya bisa melihat **Tasks** (satuan kerja terkecil yang dijalankan oleh core CPU).

---

## 📚 Penjelasan Istilah Teknis (Technical Terms)

- **PySpark:** Antarmuka Python untuk berinteraksi dengan engine Spark.
- **SparkSession:** Objek utama untuk mengontrol aplikasi Spark.
- **DataFrame:** Struktur data tabular di Spark, mirip dengan tabel SQL.
- **RDD (Resilient Distributed Dataset):** Lapisan data lebih rendah yang ada di bawah DataFrame. DataFrame lebih mudah digunakan dan lebih teroptimasi.
- **Partition:** Bagian dari dataset yang dikerjakan oleh satu inti CPU.
- **Executor:** Mesin atau proses yang melakukan perhitungan data.
- **Cluster:** Gabungan dari banyak komputer (nodes) yang menjalankan Spark.
- **Parquet:** Format file penyimpanan kolom yang dioptimalkan untuk Big Data.

---

### 📌 Summary 6.3.1

Dalam sesi "First Look" ini, saya menyimpulkan:

1. **SparkSession** adalah langkah awal wajib untuk memulai setiap aplikasi PySpark.
2. Mendefinisikan **Schema secara manual** adalah praktik terbaik untuk menjaga akurasi data dan efisiensi memori (misalnya menggunakan `IntegerType` alih-alih `Long`).
3. **Partisi** adalah kunci dari kecepatan Spark. Tanpa partisi yang tepat, resource komputer saya akan terbuang sia-sia.
4. Menyimpan hasil ke format **Parquet** sangat direkomendasikan untuk integrasi dengan **Data Warehouse** di tahap pipeline berikutnya.

---

## 📊 6.3.2 Spark DataFrames

Setelah sebelumnya saya hanya melakukan "pemanasan" dengan instalasi dan pembacaan data sederhana, di bagian ini saya menyelam lebih dalam ke jantung pemrosesan data di Spark, yaitu **DataFrame**. Saya menyadari bahwa memahami cara kerja DataFrame bukan hanya soal menghafal sintaks, tapi memahami filosofi di balik pemrosesan data terdistribusi.

---

### 🗂️ Konsep DataFrame di Spark

Saya belajar bahwa **Spark DataFrame** adalah abstraksi data tingkat tinggi yang merepresentasikan data dalam bentuk tabel (baris dan kolom). Namun, yang membedakannya dari tabel biasa adalah sifatnya yang **terdistribusi**.

Satu hal yang sangat memudahkan saya adalah saat membaca file **Parquet**. Karena Parquet menyimpan metadata tentang skema, Spark secara otomatis mengetahui tipe data setiap kolom (apakah itu _String_, _Timestamp_, atau _Integer_) tanpa saya harus mendefinisikannya secara manual seperti pada file CSV.

---

### ⚖️ Spark DataFrame vs. Pandas DataFrame

Sebagai seseorang yang sering menggunakan Python, saya tergoda untuk menyamakan Spark DataFrame dengan **Pandas**. Namun, saya menemukan perbedaan fundamental yang sangat penting:

| Fitur               | Pandas DataFrame                          | Spark DataFrame                                              |
| ------------------- | ----------------------------------------- | ------------------------------------------------------------ |
| **Eksekusi**        | Eager (langsung dieksekusi).              | Lazy (tertunda/malas).                                       |
| **Skalabilitas**    | Terbatas pada memori satu mesin saja.     | Terdistribusi di banyak mesin (Cluster).                     |
| **Penyimpanan**     | Disimpan seluruhnya di RAM mesin lokal.   | Dibagi menjadi partisi-partisi di seluruh cluster.           |
| **Fault Tolerance** | Jika proses gagal, data di memori hilang. | Resilien; bisa membangun kembali data yang hilang (Lineage). |

Saya memahami bahwa jika dataset saya muat di memori laptop, Pandas sangat luar biasa. Namun, jika saya harus mengolah miliaran baris data taksi New York, Spark adalah satu-satunya pilihan yang masuk akal.

---

### 🐢 Evaluasi Tertunda: Transformasi vs. Aksi

Ini adalah konsep yang paling "mengubah cara berpikir" saya. Spark tidak langsung menjalankan perintah saya. Ia membagi operasinya menjadi dua kategori:

1. **Transformasi (Transformations):** Operasi yang menghasilkan DataFrame baru dari yang lama (misal: `select`, `filter`, `groupBy`). Operasi ini bersifat **Lazy**. Spark hanya mencatat apa yang harus dilakukan dalam sebuah rencana kerja (**DAG - Directed Acyclic Graph**).
2. **Aksi (Actions):** Operasi yang memicu Spark untuk benar-benar melakukan perhitungan dan mengembalikan hasil (misal: `show()`, `take()`, `count()`, `write()`).

**Hal yang menarik bagi saya:** Ketika saya mengetik `.filter()`, Spark UI tidak menunjukkan adanya _job_ baru. Baru saat saya mengetik `.show()`, Spark "terbangun" dan menjalankan seluruh rangkaian perintah dari awal hingga akhir secara efisien.

---

### 🛠️ Operasi Dasar DataFrame

Saya mempraktikkan beberapa operasi dasar yang sangat mirip dengan SQL namun ditulis dalam gaya pemrograman:

- **Select & Filter:**
  Saya bisa memilih kolom tertentu dan menyaring baris berdasarkan kondisi.

```python
df.select('pickup_datetime', 'dropoff_datetime', 'PULocationID') \
  .filter(df.hvfhs_license_num == 'HV0003')

```

- **Adding Columns (`withColumn`):**
  Saya belajar menggunakan fungsi bawaan dari `pyspark.sql.functions` (biasa diimpor sebagai `F`) untuk memanipulasi kolom. Contohnya, mengubah _timestamp_ menjadi _date_.

```python
from pyspark.sql import functions as F
df = df.withColumn('pickup_date', F.to_date(df.pickup_datetime))

```

---

### 🧙‍♂️ User-Defined Functions (UDF)

Salah satu kekuatan Spark yang membuat saya terkesan adalah **UDF**. Kadang-kadang, logika bisnis terlalu rumit untuk dinyatakan dengan fungsi standar SQL atau Spark. Di sinilah saya bisa menulis fungsi Python murni dan "mengangkatnya" menjadi fungsi Spark.

**Mengapa ini penting bagi saya?**
Sebagai pengembang, saya bisa menulis logika yang sangat spesifik (misalnya algoritma pembagian ID yang aneh), menutupinya dengan _unit test_ di Python, lalu menerapkannya pada jutaan baris data di Spark.

**Contoh yang saya pelajari:**
Saya mendefinisikan fungsi Python biasa, lalu membungkusnya dengan `F.udf()`. Meskipun fleksibel, saya harus ingat bahwa UDF Python sedikit lebih lambat karena Spark harus memindahkan data antara JVM dan Python interpreter. Jadi, jika ada fungsi bawaan Spark, saya akan memprioritaskannya.

---

### 📚 Penjelasan Istilah Teknis (Technical Terms)

- **Lazy Evaluation:** Strategi optimasi di mana Spark menunda eksekusi hingga hasil benar-benar dibutuhkan oleh sebuah Aksi.
- **DAG (Directed Acyclic Graph):** Grafik rencana kerja yang disusun Spark untuk mengeksekusi transformasi dengan cara yang paling optimal.
- **F (Functions):** Koleksi fungsi bawaan Spark yang sangat dioptimalkan untuk pemrosesan data terdistribusi.
- **UDF (User-Defined Function):** Fungsi kustom yang dibuat pengguna untuk menangani logika yang tidak tersedia di fungsi standar.
- **Schema on Read:** Kemampuan Spark (terutama pada format Parquet) untuk mengetahui struktur data saat data tersebut dibaca.

---

### 📌 Summary 6.3.2

Ringkasan penting yang saya pelajari tentang Spark DataFrames:

1. **DataFrame adalah tabel terdistribusi** yang memungkinkan pemrosesan data skala besar secara paralel.
2. **Perbedaan utama dengan Pandas** terletak pada skalabilitas dan sifat eksekusinya yang _Lazy_.
3. **Memahami perbedaan antara Transformasi dan Aksi** adalah kunci untuk men-debug performa aplikasi Spark melalui Spark UI.
4. **Gunakan fungsi bawaan Spark (`F`) semaksimal mungkin** sebelum beralih ke UDF demi efisiensi performa.
5. **Data Engineering adalah tentang fleksibilitas:** Spark memberikan saya kemudahan SQL dengan kekuatan bahasa pemrograman seperti Python.

---

## 🚕 6.3.3 Preparing Dataset NYC Taxi (Yellow & Green) 🗽

Dataset **New York City Taxi & Limousine Commission (TLC)** adalah dataset klasik dalam dunia _Data Engineering_. Dataset ini mencatat jutaan perjalanan taksi di NYC, termasuk lokasi jemput/antar, waktu, tarif, dan jumlah penumpang.

Dalam Zoomcamp kali ini, kita fokus pada dua jenis taksi:

1. **🟨 Yellow Taxi:** Taksi yang biasanya beroperasi di area Manhattan.
2. **🟩 Green Taxi:** Taksi yang diperkenalkan untuk melayani area di luar Manhattan (Boro Taxis).

**Mengapa dataset ini digunakan dalam Zoomcamp? 🤔**

- **📊 Volume yang Signifikan:** Ukurannya cukup besar untuk merasakan manfaat sistem terdistribusi (Spark), namun masih bisa ditangani di mesin lokal atau VM tunggal.
- **⚙️ Masalah Skema Nyata:** Data dari tahun ke tahun seringkali memiliki perubahan tipe data atau nama kolom yang tidak konsisten. Ini memberikan tantangan nyata bagi seorang _Data Engineer_.
- **🔗 Relasi Antar Data:** Kita bisa melakukan operasi _Join_ antara data taksi dengan data referensi zona (_taxi zone lookup_).

---

### 🛠️ Proses Persiapan Data (Data Preparation) 📋

Proses ini sangat penting untuk meminimalisir error "Schema Mismatch" di tahap berikutnya. Berikut adalah langkah-langkah yang dilakukan:

#### 1️⃣ Automasi Download dengan Bash Script 📥

Alih-alih mengunduh satu per satu secara manual, kita menggunakan _Bash Script_ untuk mengunduh data bulanan dari tahun 2020 dan 2021. Script ini menggunakan `wget` dan melakukan format bulan (misalnya `1` menjadi `01`) menggunakan perintah `printf`.

#### 2️⃣ Kompresi On-the-Fly 🗜️

Data diunduh dalam format CSV dan langsung dikompresi menggunakan `gzip`. Spark dan Pandas dapat membaca file `.csv.gz` secara langsung tanpa perlu diekstrak terlebih dahulu, yang sangat menghemat ruang penyimpanan di _Data Lake_.

#### 3️⃣ Pendefinisian Skema yang Ketat (Strict Schema) 🔐

Spark seringkali menebak semua kolom sebagai _String_ saat membaca CSV. Untuk menghindarinya, kita mendefinisikan skema secara manual menggunakan `StructType`.

- **💾 Efisiensi Memori:** Kita mengubah tipe data `Long` (8 byte) menjadi `Integer` (4 byte) untuk kolom ID atau jumlah penumpang.
- **✅ Konsistensi:** Memastikan kolom waktu dibaca sebagai `TimestampType` agar fungsi manipulasi tanggal bisa bekerja.

#### 4️⃣ Konversi ke Parquet dengan Repartitioning 🔄

Setelah CSV dibaca dengan skema yang benar, data disimpan ke dalam format **Parquet**.

- **❓ Mengapa Parquet?** Format ini menyimpan skema di dalamnya (self-describing) dan jauh lebih cepat untuk operasi analitik.
- **⚡ Repartitioning:** Karena file CSV asli mungkin hanya terdiri dari satu file besar, kita menggunakan `.repartition(4)` (sesuaikan dengan jumlah core CPU) agar saat disimpan, data terbagi menjadi beberapa file kecil. Ini memungkinkan semua _executor_ Spark bekerja secara paralel di tahap selanjutnya.

---

### 📚 Penjelasan Istilah Teknis (Technical Terms) 🔍

- **Bash Script:** 📜 File teks berisi serangkaian perintah Linux/Unix yang dijalankan secara otomatis.
- **Gzip (.gz):** 🗜️ Algoritma kompresi file yang umum digunakan untuk mengecilkan ukuran file teks seperti CSV.
- **Schema Mismatch:** ⚠️ Kondisi di mana struktur data (nama atau tipe kolom) tidak sesuai dengan yang diharapkan oleh program.
- **StructType & StructField:** 🏗️ Komponen dalam PySpark yang digunakan untuk mendefinisikan struktur tabel secara programmatik.
- **Self-Describing Format:** 📝 Format file (seperti Parquet) yang menyimpan informasi tentang kolom dan tipe datanya di dalam file itu sendiri.

---

### 📌 Summary 6.3.3 ✨

Proses persiapan ini memastikan bahwa:

1. **✅ Data terkumpul secara sistematis** untuk tahun 2020 dan 2021 (Yellow & Green).
2. **🔒 Skema data terkunci** dan konsisten, sehingga tidak ada error saat kita menggabungkan data antar bulan atau tahun.
3. **⚡ Data optimal untuk Spark** karena sudah dalam format Parquet dan terbagi dalam partisi yang merata.

---

## 📊 6.3.4 SQL with Spark

Setelah berhasil menyiapkan data dalam format Parquet, langkah selanjutnya adalah melakukan analisis. Salah satu fitur terkuat Spark adalah kemampuannya untuk menjalankan query SQL murni di atas DataFrame. Ini sangat berguna bagi siapa saja yang sudah terbiasa dengan sintaks SQL namun ingin memanfaatkan kekuatan pemrosesan terdistribusi Spark.

---

### 💻 Menjalankan SQL di Spark

Agar Spark bisa mengenali sebuah DataFrame sebagai tabel SQL, kita perlu mendaftarkannya terlebih dahulu sebagai **Temporary View**.

1. **Registrasi Tabel:** Gunakan perintah `df.createOrReplaceTempView("nama_tabel")`. Ini tidak memindahkan data, melainkan hanya memberikan alias agar Spark SQL engine bisa menemukannya.
2. **Eksekusi Query:** Jalankan perintah SQL melalui `spark.sql("SELECT ...")`. Hasilnya akan selalu berupa DataFrame baru.

**Contoh Alur Kerja:**

- Menggabungkan data taksi Kuning dan Hijau (Union).
- Menyeragamkan nama kolom (misal: `lpep_pickup_datetime` menjadi `pickup_datetime`).
- Menambahkan kolom literal seperti `service_type` untuk membedakan sumber data.
- Mendaftarkan hasilnya sebagai `trips_data` dan menjalankan query agregasi pendapatan per bulan/zona.

---

### 🧠 Spark SQL Engine & Eksekusi

Saat kita menjalankan perintah `spark.sql()`, Spark tidak langsung mengeksekusi baris perintah tersebut. Di balik layar, Spark SQL menggunakan **Catalyst Optimizer** untuk menyusun rencana eksekusi yang paling efisien.

Melalui **Spark Master UI**, kita bisa melihat bagaimana query tersebut dipecah menjadi beberapa **Stages** dan **Tasks**:

- **Exchange (Shuffle):** Terjadi saat kita melakukan `GROUP BY`. Spark harus memindahkan data antar _executor_ agar data dengan kunci yang sama berada di tempat yang sama untuk dihitung.
- **Parallel Processing:** Jika kita memiliki 4 core CPU, Spark bisa menjalankan 4 tugas secara bersamaan, mempercepat proses agregasi jutaan baris data.

---

### ⚡ Optimasi Query: Coalesce vs Repartition

Salah satu masalah yang sering muncul saat menulis hasil query adalah terciptanya terlalu banyak file kecil (misal: 200 file berukuran hanya beberapa KB). Ini tidak efisien untuk penyimpanan maupun pembacaan di masa depan.

| Teknik               | Fungsi                                    | Penggunaan                                                                               |
| -------------------- | ----------------------------------------- | ---------------------------------------------------------------------------------------- |
| **`repartition(n)`** | Mengatur ulang data ke dalam `n` partisi. | Bisa menambah atau mengurangi partisi; melibatkan _full shuffle_.                        |
| **`coalesce(n)`**    | Mengurangi jumlah partisi ke `n`.         | Lebih efisien untuk **mengurangi** file karena meminimalkan perpindahan data antar core. |

> **Catatan Penting:** Gunakan `.coalesce(1)` sebelum melakukan `.write()` jika hasil akhir Anda cukup kecil dan Anda ingin menyimpannya sebagai satu file tunggal di Data Lake.

---

### 📌 Summary 6.3.4

- **SQL Bridge:** Spark memungkinkan penggunaan SQL di atas data taksi yang terdistribusi, memberikan fleksibilitas tanpa harus berpindah ke Data Warehouse.
- **Logical vs Physical Plan:** Spark merencanakan eksekusi query secara cerdas sebelum benar-benar menyentuh data.
- **Data Lake Reporting:** Hasil pengolahan Spark bisa langsung disimpan kembali ke Data Lake (sebagai Parquet) untuk kemudian dikonsumsi oleh alat BI atau proses ETL lainnya.
- **Manajemen Partisi:** Mengelola jumlah file output (menggunakan `coalesce`) sangat krusial untuk menjaga kesehatan performa Data Lake.

---
