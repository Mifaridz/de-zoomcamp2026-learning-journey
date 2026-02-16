# 🌉 04-Analytics Engineering Basics

> **Topik:** Fondasi Analytics Engineering & Dimensional Modeling (Kimball)

Setelah belajar cara menyimpan data di BigQuery pada Module-03, sekarang saya masuk ke tahap di mana data mentah tersebut "dimasak" agar siap dikonsumsi. Memahami mengapa peran ini ada dan teori apa yang mendasarinya sebelum kita terjun ke _tooling_ (dbt).

---

## **4.1.1 - Kenapa Analytics Engineering Ada?**

Dunia data berubah drastis dalam beberapa tahun terakhir, dan perubahan ini menciptakan celah baru:

- **Cloud Data Warehouse (BigQuery/Snowflake):** Penyimpanan dan komputasi jadi murah. Kita tidak perlu lagi pelit soal data apa yang harus di-load.
- **EL Tools (Fivetran/Stitch):** Memasukkan data ke warehouse jadi sangat mudah (otomatis).
- **Self-service BI:** Orang bisnis sekarang bisa bikin laporan sendiri, tapi mereka butuh data yang bersih dan terstruktur.

### **Menjembatani Celah (The Gap)**

Dulu, tim data hanya terbagi dua:

1. **Data Engineer:** Ahli infrastruktur, tapi kurang paham konteks bisnis.
2. **Data Analyst:** Ahli bisnis, tapi kurang paham _best practice_ software engineering (seperti version control atau testing).

**Analytics Engineer** muncul untuk mengisi celah itu. Mereka membawa ilmu _software engineering_ ke dunia analisis. Mereka memastikan data tidak hanya "ada", tapi juga bersih, teruji, dan terdokumentasi.

---

## **4.1.2 - ETL vs ELT**

Penyegaran kembali tentang perbedaan strategi transformasi data:

- **ETL (Extract, Transform, Load):** Transformasi di luar warehouse. Bersih sejak hari pertama, tapi kaku dan lambat diatur.
- **ELT (Extract, Load, Transform):** Pendekatan modern yang kita gunakan. Data mentah masuk dulu ke warehouse, baru diolah di dalam (menggunakan **dbt**). Ini jauh lebih fleksibel karena kita punya akses ke data mentah kapan saja.

---

## **4.1.3 - Dimensional Modeling (Kimball)**

Ini adalah _mental model_ utama dalam menyusun data agar cepat di-query dan mudah dipahami manusia. Berbeda dengan normalisasi (3NF) yang saya pelajari di database aplikasi, di sini kita sengaja membiarkan ada redudansi data demi performa.

### **Fact Tables vs Dimension Tables**

- **Fact Tables (Fakta):** Berisi metrik, angka, atau kejadian bisnis. Pikirkan sebagai **KATA KERJA**.
- _Contoh:_ "Terjadi pesanan", "Seseorang naik taksi".

- **Dimension Tables (Dimensi):** Berisi konteks atau atribut dari fakta tersebut. Pikirkan sebagai **KATA BENDA**.
- _Contoh:_ "Siapa pelanggannya?", "Di mana lokasinya?", "Apa warna taksinya?".

Keduanya membentuk **Star Schema**, di mana tabel fakta ada di tengah dikelilingi oleh tabel-tabel dimensi.

---

## **4.1.4 - Analogi Dapur**

Ini analogi favorit saya untuk memahami aliran data di warehouse:

> - **Staging Area (Pantry):** Tempat penyimpanan bahan mentah (raw data). Berantakan dan tidak untuk dilihat tamu (bisnis user).
> - **Processing Area (Kitchen):** Tempat koki (Analytics Engineer) bekerja memotong, memasak, dan membumbui data. Di sini efisiensi dan standar rasa dijaga.
> - **Presentation Area (Dining Hall):** Meja makan tempat hidangan (data model) disajikan. Bersih, tertata, dan siap dinikmati oleh orang bisnis lewat dashboard.

---

## 📚 Apa yang Saya Pelajari

- **Definisi Peran:** Saya sekarang paham bahwa Analytics Engineer bukan cuma "tukang bikin tabel", tapi orang yang menerapkan disiplin _Software Engineering_ (seperti Testing dan CI/CD) ke dalam workflow data.
- **Mindset User-Centric:** Tujuan akhir saya bukan cuma mengisi database, tapi menyediakan "hidangan" data yang mudah dimengerti oleh orang yang tidak tahu teknis.
- **Pentingnya Teori Kimball:** Saya belajar bahwa struktur data yang bagus (Star Schema) akan sangat membantu mempercepat query di BigQuery, karena BigQuery sangat suka dengan tabel yang sudah terdenormalisasi dengan baik.
- **Fokus dbt:** Saya mulai melihat posisi dbt ada di bagian "Kitchen". dbt adalah alat yang akan saya gunakan untuk memasak data mentah di pantry menjadi hidangan lezat di meja makan.

---

## 📌 Summary

Analytics Engineering bukan hanya soal alat, tapi soal **perubahan cara kerja**. Dengan memindahkan transformasi ke dalam warehouse (ELT) dan menerapkan pemodelan dimensi, kita bisa membangun sistem data yang lebih kuat, teruji, dan benar-benar berguna bagi bisnis.

> **📝 Note:** _Data Engineering membangun jalannya, Analytics Engineering membangun kendaraannya agar user bisa sampai ke tujuan (insight) dengan nyaman._

---

# 🧱 4.1.2-What is dbt?

> **Topik:** Mengenal dbt sebagai Standar Baru Transformasi Data

Setelah paham konsep _Analytics Engineering_, sekarang saya belajar tentang alat yang memungkinkan semua itu terjadi. **dbt** adalah alat yang duduk di atas _data warehouse_ kita (seperti BigQuery) dan bertugas mengubah data mentah menjadi data yang siap pakai.

Saya suka membayangkan dbt sebagai **compiler untuk SQL**. Kita menulis logika bisnisnya, dbt yang mengurus teknis pembuatan tabel dan pengaturannya di database.

---

## **Apa itu dbt Sebenarnya?**

dbt adalah _transformation workflow tool_. Posisinya ada di huruf **"T"** dalam strategi **ELT**.

- **Input:** Data mentah (_raw data_) yang sudah di-load ke warehouse.
- **Proses:** Kita menulis SQL (atau Python) untuk mendefinisikan transformasi.
- **Output:** dbt mengelola dependensi dan merubah SQL tersebut menjadi tabel atau view permanen di warehouse.

---

## **Masalah yang Diselesaikan dbt**

Sebelum ada dbt, proses transformasi data seringkali berantakan (query raksasa ribuan baris, tidak ada testing, dokumentasi di Excel). dbt membawa **Software Engineering Best Practices** ke dunia data:

- **Version Control:** Semua kode transformasi disimpan di Git. Ada riwayat perubahan dan bisa kolaborasi tim.
- **Modularity:** Saya tidak perlu menulis query "spageti" yang panjang. Saya bisa memecah logika menjadi potongan-potongan kecil yang bisa dipakai ulang.
- **Testing:** Ada fitur otomatis untuk mengecek kualitas data (misal: memastikan ID tidak ada yang null atau duplikat).
- **Documentation:** Dokumentasi dibuat otomatis dari kode. Tidak ada lagi dokumentasi yang ketinggalan zaman.
- **Environments:** Saya punya "bak pasir" (_sandbox_) sendiri untuk _coding_ tanpa takut merusak data yang dipakai orang kantor (pemisahan Dev dan Prod).

---

## **Cara Kerja dbt (The Mechanics)**

Hal yang paling ajaib bagi saya adalah: **Saya tidak perlu lagi menulis `CREATE TABLE` atau `DROP VIEW`.**

1. Saya cukup menulis pernyataan `SELECT`.
2. Saya menggunakan fungsi `ref()` atau `source()` untuk menghubungkan satu tabel dengan tabel lainnya.
3. Saat saya menjalankan perintah `dbt run`, dbt akan:

- Menyusun (compile) SQL saya.
- Menangani urutan eksekusi (tabel mana yang harus dibuat duluan).
- Membungkus query saya dengan DDL/DML yang sesuai secara otomatis.

---

## **dbt Core vs dbt Cloud**

Ada dua jalur untuk menggunakan dbt, dan ini perbandingannya:

| Fitur             | **dbt Core** (Open Source)           | **dbt Cloud** (SaaS)                          |
| ----------------- | ------------------------------------ | --------------------------------------------- |
| **Biaya**         | Gratis selamanya.                    | Ada _Free Plan_ untuk individu.               |
| **Interface**     | Terminal / CLI.                      | IDE berbasis Web yang intuitif.               |
| **Instalasi**     | Manual di laptop (Python/Pip).       | Tidak butuh instalasi lokal.                  |
| **Orchestration** | Harus diatur sendiri (Airflow/Cron). | Sudah ada penjadwal (_scheduler_) bawaan.     |
| **Cocok untuk**   | Engineer yang suka kontrol penuh.    | Tim yang ingin cepat _set up_ dan kolaborasi. |

---

## **Alur Proyek di Zoomcamp Ini**

Di module ini, kita akan menempuh alur kerja profesional:

1. **Raw Data:** Data taksi NYC yang sudah ada di BigQuery.
2. **Transformasi:** Menggunakan dbt untuk mengubahnya menjadi model data _Star Schema_ (Fakta & Dimensi).
3. **Visualisasi:** Hasil akhir dbt akan dikonsumsi oleh dashboard (Looker Studio) untuk dilihat orang bisnis.

---

## 📚 Apa yang Saya Pelajari

- **Mindset Baru:** Saya belajar bahwa menulis SQL bukan lagi sekadar menulis query, tapi **membangun software**. dbt memaksa saya untuk peduli pada testing dan dokumentasi.
- **Otomatisasi DDL:** Saya sangat senang karena tidak perlu pusing lagi dengan urutan pembuatan tabel. dbt tahu tabel mana yang bergantung pada tabel lainnya lewat fitur _Lineage_.
- **Efisiensi Kolaborasi:** Dengan adanya pemisahan _Environment_, saya merasa lebih aman untuk bereksperimen di tahap _Development_ tanpa risiko merusak laporan dashboard utama.
- **Pilihan Jalur:** Saya mengerti perbedaan Core dan Cloud. Untuk pemula seperti saya, dbt Cloud sangat membantu karena saya bisa fokus belajar transformasinya tanpa pusing dengan instalasi environment Python lokal yang rumit.

---

## 📌 Summary

dbt adalah standar industri saat ini untuk _Analytics Engineering_. dbt mengubah SQL yang tadinya hanya "bahasa kueri" menjadi kode yang bisa diuji, dikelola versinya, dan dijalankan secara otomatis dengan _best practice_ rekayasa perangkat lunak.

> **📝 Note:** _dbt tidak memindahkan data (E/L). dbt hanya bekerja di dalam database untuk mengubah data yang sudah ada (T). Jangan lupakan perbedaan ini saat merancang pipeline!_

---

# ⚖️ 4.2.1-dbt Core vs dbt Cloud

> **Topik:** Evolusi dbt, Masa Depan dengan Fusion, dan Strategi Belajar

Setelah tahu apa itu dbt, sekarang saya harus memilih "senjata" mana yang akan digunakan. Ada dua dbt yang populer, dan ada satu teknologi baru bernama **Fusion** yang bakal jadi standar masa depan.

---

## **4.2.1.1 - Perbandingan Dua Saudara: Core & Cloud**

### **dbt Core (Si Open Source)**

Lahir tahun 2016, dbt Core adalah mesin asli yang membuat dbt populer.

- **Gratis 100%:** Jalan di terminal laptop kita sendiri.
- **Transparan:** Kode sumbernya ada di GitHub, bisa kita bedah atau modifikasi.
- **Manual:** Kita sendiri yang mengatur instalasi, jadwal (_scheduling_), dan dokumentasi.

### **dbt Cloud (Si SaaS Platform)**

Lahir dua tahun kemudian untuk menjawab kebutuhan perusahaan besar.

- **Berbayar (SaaS):** Tidak perlu pusing urusan infrastruktur.
- **Fitur Lengkap:** Sudah termasuk _hosting_ dokumentasi, _orchestration_ (penjadwalan), dan sistem keamanan untuk tim.
- **User-Friendly:** Punya IDE berbasis web, jadi tidak harus jago pakai terminal.

---

## **4.2.1.2 - dbt Fusion: Masa Depan dbt (Update 2025/2026)**

Ini adalah informasi terbaru yang sangat menarik! Pada Mei 2025, dbt Labs mengumumkan perombakan total kode dbt yang disebut **Fusion**.

**Kenapa Fusion Penting?**

- **Sangat Cepat:** Kompilasi kode bisa 30x lebih cepat dibanding versi lama.
- **Smarter:** Bisa mendeteksi error _sebelum_ kita menjalankan query, jadi hemat waktu dan biaya di BigQuery/Snowflake.
- **Unified License:** Visinya adalah satu lisensi untuk semua. Kamu bisa kerja di web IDE atau di VS Code pake _official extension_, tapi mesinnya tetap sama (Fusion).

**Batasan Fusion saat ini (Awal 2026):**

- Belum mendukung semua database. Saat ini baru mendukung "pemain besar" seperti **BigQuery, Snowflake, Databricks, Postgres, dan Redshift**.
- **Belum mendukung DuckDB** atau adapter komunitas lainnya. Jadi kalau pakai database "niche", kita mungkin masih harus pakai dbt Core versi lama.

---

## **4.2.1.3 - Kenapa Zoomcamp Pakai dbt Core + DuckDB?**

Mungkin awalnya saya bingung, "Kenapa tidak pakai yang Cloud saja biar gampang?" Ternyata ada alasan kuat di baliknya:

1. **Under the Hood:** Pakai dbt Core memaksa saya paham apa yang sebenarnya terjadi di balik layar (bagaimana folder disusun, bagaimana perintah dijalankan).
2. **Transferable Skills:** Kalau sudah paham Core, pindah ke Cloud itu gampang banget. Tapi kalau cuma tahu klik-klik di Cloud, saya bakal bingung kalau harus kerja di terminal.
3. **DuckDB Power:** Menggunakan DuckDB lokal membantu saya belajar tanpa harus takut kena tagihan cloud yang mahal saat masih tahap eksperimen.

---

## 📚 Apa yang Saya Pelajari

- **Fokus pada Fundamental:** Saya belajar bahwa dbt Core atau Cloud hanyalah "bungkus". Logika transformasinya tetap sama. Sebagai konsultan atau engineer nanti, saya harus fleksibel bisa pakai keduanya.
- **Antisipasi Teknologi Baru:** Dengan adanya **Fusion**, saya tahu bahwa efisiensi kompilasi adalah tren masa depan. Saya harus mulai membiasakan diri dengan _official extension_ di VS Code.
- **Kompatibilitas Hybrid:** Dulu orang teknis pakai Core dan orang analis pakai Cloud di project yang sama. Sekarang arahnya menuju satu ekosistem yang lebih menyatu (_Unified_).
- **Pentingnya Memilih Adapter:** Saya harus cek [dokumentasi resmi](https://docs.getdbt.com/docs/fusion/supported-features) sebelum memulai project baru untuk memastikan database yang saya pakai didukung oleh engine Fusion.

---

## 📌 Summary

Tidak masalah mana yang dipelajari duluan. dbt Core memberikan pemahaman mendalam, sementara dbt Cloud memberikan kenyamanan skala perusahaan. Di tahun 2026 ini, **dbt Fusion** adalah arah baru yang akan menyatukan keduanya dengan kecepatan yang jauh lebih tinggi.

> **📝 Note:** _Pahami mesinnya (Core), maka kamu akan menguasai kemudinya (Cloud). Jangan kaget kalau performa dbt kamu tiba-tiba melesat kalau sudah pakai engine Fusion!_

---

# 📂 4.3.1-dbt Project Structure

> **Topik:** Anatomi Proyek dbt & Arsitektur Folder `models`

Mempelajari struktur dbt adalah tentang memahami di mana setiap potongan _puzzle_ harus diletakkan. dbt punya aturan main yang sangat terstandarisasi, jadi siapa pun yang membuka proyek saya nanti (termasuk saya sendiri 6 bulan lagi) tidak akan kebingungan mencari file.

---

## **File & Folder Utama di Top-Level**

### **1. `dbt_project.yml` (Otak Proyek)** 🧠

Ini adalah file paling penting. Tanpa file ini, dbt tidak akan jalan.

- Berisi nama proyek, konfigurasi profil (koneksi ke DB), variabel, dan pengaturan _materialization_ default (apakah mau jadi tabel atau view).

### **2. Folder `models/` (Jantung Proyek)** ❤️

Di sinilah semua logika transformasi SQL saya berada. dbt menyarankan struktur 3 lapis (Staging, Intermediate, Marts) yang akan kita bedah di bawah.

### **3. `macros/` (Fungsi Reusable)** 🛠️

Jika saya sering menulis SQL yang sama berulang kali (misal: konversi mata uang atau format tanggal), saya akan membungkusnya jadi **Macro**. Ini seperti fungsi di Python, tulis sekali, pakai di mana saja.

### **4. `seeds/` (Ingest CSV Cepat)** 🌱

Tempat menaruh file CSV kecil (seperti tabel _lookup_ atau daftar kode wilayah). dbt akan mengubah CSV ini menjadi tabel di database.

> _Catatan:_ Ini cara "cepat dan kotor", lebih baik load data lewat pipeline utama jika datanya besar.

### **5. `snapshots/` (Perekam Histori)** 📸

Berguna jika tabel sumber saya sering berubah (kolomnya tertimpa data baru), tapi saya butuh menyimpan riwayat perubahannya (_Slowly Changing Dimensions_). dbt akan mengambil "foto" data tersebut secara berkala.

### **6. `tests/` (Quality Control)** ✅

Tempat menaruh query SQL untuk memastikan data saya benar. Aturannya sederhana: **Jika query menghasilkan baris (>0), maka test gagal.** \* _Contoh:_ Test untuk memastikan tidak ada total jam kerja yang lebih dari 24 jam dalam sehari.

### **7. `analysis/` & `README.md`**

- **Analysis:** Tempat coretan SQL _ad-hoc_ yang tidak ingin saya jadikan tabel permanen.
- **README:** Manual panduan proyek agar kawan setim tahu cara menjalankan proyek ini.

---

## **Arsitektur Folder `models/`: Aliran dari Pantry ke Meja Makan**

dbt menyarankan struktur folder yang mengikuti **Analogi Dapur** yang kita bahas sebelumnya:

1. **`staging/` (Bahan Mentah):**

- Berisi definisi sumber (_Source_) dan model awal.
- Aturan emas: **1:1 dengan sumber**. Jangan lakukan transformasi berat di sini.
- Hanya pembersihan ringan: ganti nama kolom agar konsisten, ganti tipe data, atau hapus baris kosong.

2. **`intermediate/` (Proses Memasak):**

- Tempat semua "kegaduhan" terjadi: _join_ antar tabel yang kompleks, pembersihan berat, dan kalkulasi rumit.
- Data di sini belum siap disajikan ke orang bisnis.

3. **`marts/` (Hidangan Siap Saji):**

- Inilah hasil akhirnya. Tabel di sini sudah bersih, teruji, dan siap dikonsumsi oleh BI Tool (Looker/Tableau).
- Biasanya berbentuk _Star Schema_ (Fakta & Dimensi).

---

## 📚 Apa yang Saya Pelajari

- **Disiplin Folder:** Saya belajar bahwa kerapian folder bukan cuma soal estetika, tapi soal skalabilitas. Dengan memisahkan `staging` dan `marts`, saya tahu persis di mana harus mencari jika ada data yang salah tipe atau salah hitung.
- **Kekuatan Macros:** Saya baru sadar betapa membosankannya menulis logika pajak atau kalender fiskal berulang-ulang. Macro adalah penyelamat waktu yang luar biasa.
- **Testing sebagai First-Class Citizen:** Di dbt, testing bukan pilihan tapi bagian dari workflow. Saya merasa lebih aman karena dbt akan "berteriak" (error) jika data saya melanggar aturan bisnis yang saya buat di folder `tests`.
- **Fleksibilitas Konvensi:** Meskipun dbt menyarankan `staging/marts`, saya tahu beberapa tim memakai istilah lain (Bronze/Silver/Gold). Yang terpenting adalah konsistensi di dalam tim.

---

## 📌 Summary

Struktur proyek dbt dirancang untuk membawa keteraturan dalam kekacauan data. Dengan membagi proses menjadi **Staging (Persiapan)**, **Intermediate (Pemrosesan)**, dan **Marts (Penyajian)**, kita menciptakan pipeline yang mudah diaudit dan tahan lama.

> **📝 Note:** _Jangan pernah melakukan join kompleks di folder staging. Biarkan staging tetap bersih sebagai cerminan dari data sumber awal._

---

# 🔌 4.3.2-dbt Sources

> **Topik:** Mendefinisikan Sumber Data & Membuat Model Staging (`stg_`)

Di tahap ini, saya belajar bahwa kita tidak boleh langsung melakukan "hard-code" nama tabel (seperti `FROM project.dataset.table`) di dalam query SQL kita. Mengapa? Karena itu kaku. dbt punya cara yang lebih elegan bernama **Sources**.

---

## **4.3.2.1 - Mendefinisikan Sources dengan `sources.yml`**

Langkah pertama adalah membuat file YAML di dalam folder `models/staging/`. File ini adalah "peta" yang memberi tahu dbt di mana data mentah kita berada.

**Contoh Struktur `sources.yml`:**

```yaml
sources:
  - name: staging # Nama label bebas
    database: taxi_rides_ny # Nama Project GCP atau Nama DB DuckDB
    schema: trips_data_all # Nama Dataset BigQuery atau Schema DuckDB

    tables:
      - name: green_tripdata
      - name: yellow_tripdata
```

> **Penting:** Nama `database` dan `schema` harus persis sesuai dengan yang ada di warehouse kamu (BigQuery atau DuckDB).

---

## **4.3.2.2 - Menggunakan Fungsi `source()`**

Setelah didefinisikan di YAML, saya memanggil tabel tersebut di file SQL menggunakan Jinja macro:
`{{ source('nama_source', 'nama_tabel') }}`

**Kenapa pakai ini?**

1. **Fleksibilitas:** Jika besok dataset saya pindah dari `prod` ke `staging_db`, saya hanya perlu ubah satu file YAML, bukan ratusan file SQL.
2. **Lineage:** dbt otomatis tahu bahwa model saya bergantung pada data mentah tersebut.

---

## **4.3.2.3 - Membangun Model Staging yang Baik (`stg_`)**

Model staging adalah tempat kita melakukan "pembersihan awal". dbt menyarankan beberapa aturan emas:

1. **Prefix `stg_`:** Selalu awali nama file dengan `stg_` (contoh: `stg_green_tripdata.sql`).
2. **Explicit Casting:** Jangan percaya tipe data dari sumber. Gunakan `CAST(kolom AS type)` untuk memastikan semuanya benar (ID jadi integer, biaya jadi numeric, waktu jadi timestamp).
3. **Renaming:** Berikan nama kolom yang lebih manusiawi dan konsisten.
4. **Logical Ordering:** Susun kolom dengan urutan yang rapi:

- **Identifiers:** ID vendor, ID lokasi.
- **Timestamps:** Waktu jemput, waktu sampai.
- **Trip Info:** Jarak, jumlah penumpang.
- **Payment Info:** Tarif, pajak, tip, total bayar.

**Contoh Potongan SQL Staging:**

```sql
with tripdata as (
  select * from {{ source('staging','green_tripdata') }}
  where vendorid is not null -- Filter tipis untuk kualitas data
)
select
    -- identifiers
    cast(vendorid as integer) as vendorid,
    cast(pulocationid as integer) as pickup_locationid,
    -- timestamps
    cast(lpep_pickup_datetime as timestamp) as pickup_datetime,
    -- payment info
    cast(fare_amount as numeric) as fare_amount
from tripdata

```

---

## **4.3.2.4 - Catatan tentang Filter (The 1:1 Rule)**

Secara teori, staging harus **1:1** dengan sumber (jumlah baris dan kolom sama). Namun, di proyek Taxi NYC ini, ada banyak data sampah di mana `vendorid` bernilai NULL.

**Keputusan Praktis:** Kita melakukan filter `where vendorid is not null` langsung di staging agar model-model selanjutnya (Intermediate/Marts) sudah menerima data yang minimal punya identitas.

---

## 📚 Apa yang Saya Pelajari

- **Kekuatan Abstraksi:** Saya baru sadar betapa bahayanya _hard-coding_ nama tabel. Dengan `sources.yml`, manajemen lingkungan (Dev vs Prod) jadi jauh lebih mudah.
- **Disiplin Tipe Data:** Melakukan `CAST` di awal mencegah error "Type Mismatch" yang menyebalkan saat kita melakukan JOIN atau agregasi di layer Marts nanti.
- **Struktur sebagai Dokumentasi:** Dengan mengurutkan kolom (ID -> Time -> Info), file SQL saya jadi jauh lebih mudah dibaca oleh orang lain.
- **Pragmatisme vs Teori:** Meskipun teorinya staging harus 1:1, terkadang melakukan pembersihan dasar (seperti membuang baris NULL) di awal sangat membantu performa dan kejelasan data ke depannya.

---

## 📌 Summary

Sources adalah fondasi. Tanpa definisi sumber yang benar, dbt tidak tahu apa yang harus dimasak. Dengan membuat model staging (`stg_`) yang bersih, eksplisit, dan terstruktur, kita sudah menyelesaikan 50% pekerjaan berat dalam _Data Modeling_.

> **📝 Note:** _Jangan malas menulis `CAST`. Apa yang terlihat seperti integer di sumber, belum tentu terbaca integer oleh database tujuan. Eksplisit itu lebih baik daripada implisit!_

---

# 🏗️ 4.4.1-dbt Models & Business Context

> **Topik:** Transformasi Lanjutan, Perbedaan `ref()` vs `source()`, dan Penyatuan Data (Union)

Di tahap ini, seorang Data Engineer berubah peran menjadi **Analytics Engineer**. Kita tidak lagi cuma memikirkan tipe data, tapi bagaimana data ini bisa menjawab pertanyaan bisnis. Caranya? Dengan melakukan eksplorasi data secara mendalam sebelum menulis kode.

---

## **4.4.1.1 - Apa yang Sedang Kita Bangun?**

Ada dua produk utama yang biasanya dihasilkan di layer ini:

1. **Laporan & Dashboard:** Tabel yang khusus dibuat untuk visualisasi tertentu (misal: Pendapatan Bulanan per Lokasi).
2. **Model Dimensional (Star Schema):**

- **Fact Tables (`fct_`):** Berisi kejadian bisnis (KATA KERJA). Satu baris = satu kejadian. Contoh: `fct_trips` (satu baris per perjalanan).
- **Dimension Tables (`dim_`):** Berisi atribut dari entitas (KATA BENDA). Contoh: `dim_zones` (informasi lokasi).

---

## **4.4.1.2 - Sihir dbt: `source()` vs `ref()`**

Ini adalah perbedaan krusial yang harus diingat:

- **`{{ source('nama', 'tabel') }}`:** Digunakan **HANYA** untuk mengambil data mentah dari luar dbt (tabel yang didefinisikan di YAML).
- **`{{ ref('nama_model') }}`:** Digunakan untuk mengambil data dari **model dbt lain** yang sudah kita buat.

**Kenapa `ref()` sangat sakti?**
Karena dbt otomatis membangun **Lineage Graph (DAG)**. dbt tahu tabel mana yang harus diproses duluan berdasarkan siapa yang me-`ref` siapa. Saya tidak perlu pusing mengatur urutan _run_.

---

## **4.4.1.3 - Layer Intermediate (`int_`)**

Kadang kita butuh langkah "tengah" sebelum data siap disajikan di Marts. Misalnya, kita ingin menggabungkan data Taksi Kuning dan Hijau.

- **Konvensi:** Gunakan prefix `int_` (contoh: `int_trips_unioned.sql`).
- **Tujuan:** Menjaga agar layer Marts tetap bersih. Semua proses "kotor" seperti penyatuan (_union_) dilakukan di sini.

---

## **4.4.1.4 - Masalah Skema: Kuning vs Hijau**

Saat mencoba menggabungkan (_Union_) data `stg_green` dan `stg_yellow`, saya menemukan error: **jumlah kolom tidak sama.**
Ternyata, data Taksi Hijau punya dua kolom yang tidak ada di Taksi Kuning:

1. **`trip_type`:** Taksi Kuning selalu "street hail" (tipe 1), jadi kita bisa _hard-code_ nilainya.
2. **`ehail_fee`:** Taksi Kuning tidak punya fitur e-hail, jadi kita beri nilai 0.

**Penting:** Perbedaan ini bukan cuma masalah teknis, tapi masalah **Bisnis**. Taksi Kuning beroperasi di Manhattan (hail di jalan), sementara Taksi Hijau diciptakan untuk area luar Manhattan (bisa dipesan lewat aplikasi). Memahami ini membantu saya menentukan nilai _hard-code_ yang benar.

---

## 📚 Apa yang Saya Pelajari

- **Konteks adalah Kunci:** Saya belajar bahwa menjadi Data Engineer bukan cuma soal jago SQL. Saya harus tahu _kenapa_ datanya berbeda (sejarah Taksi NYC) agar bisa memberikan solusi data yang akurat.
- **Otomatisasi Dependensi:** Fungsi `ref()` benar-benar memudahkan hidup. Saya tidak perlu lagi mengelola skrip urutan eksekusi secara manual.
- **Layering itu Penting:** Dengan adanya layer `intermediate`, saya bisa melakukan transformasi yang "berantakan" tanpa mengotori tabel final yang akan dilihat oleh pengguna bisnis.
- **Standardisasi Skema:** Saya belajar cara menyelaraskan dua sumber data yang berbeda agar bisa disatukan dalam satu tabel fakta tunggal (`fct_trips`).

---

## 📌 Summary

Membangun model dbt adalah proses menerjemahkan aturan bisnis ke dalam kode SQL yang terstruktur. Dengan memanfaatkan **Star Schema** dan fungsi **`ref()`**, kita menciptakan sistem data yang tidak hanya cepat di-query, tapi juga mudah dipahami alur perubahannya.

> **📝 Note:** _Gunakan `source()` untuk data mentah, dan gunakan `ref()` untuk sesama model dbt. Ini adalah aturan dasar untuk membangun Lineage yang benar!_

---

# 🌱 4.4.2-dbt Seeds and Macros

> **Topik:** Ingest Data CSV (Seeds) dan Membuat Fungsi SQL Reusable (Macros)

Tujuan utama kita di sini adalah mengubah angka-angka kode yang membosankan menjadi informasi yang punya arti bagi manusia (seperti nama Vendor atau nama Wilayah).

---

## **4.4.2.1 - dbt Seeds: Memasukkan Data Manual ke Warehouse**

Kadang kita punya data referensi kecil dalam bentuk CSV (seperti tabel lookup lokasi) yang tidak ada di database utama. **Seeds** adalah solusinya.

- **Cara Pakai:**

1. Masukkan file `.csv` ke folder `seeds/`.
2. Jalankan perintah `dbt seed`.
3. dbt akan membuat tabel permanen di database kamu berdasarkan CSV tersebut.

- **Cara Panggil:** Gunakan `{{ ref('nama_file_csv') }}` sama seperti memanggil model SQL lainnya.

### **Aturan Main Seeds:**

- **Cocok untuk:** Data statis dan kecil (tabel referensi, daftar kode negara, dsb).
- **Haram untuk:** Data sensitif/rahasia (karena file CSV ini akan masuk ke Git/GitHub).
- **Jangan Berlebihan:** Jika datanya besar (jutaan baris), lebih baik di-load lewat pipeline data biasa (Python/Airflow/GCS), bukan lewat Seeds.

**Contoh Kasus:** Kita membuat `dim_zones` hanya dengan melakukan `SELECT` dari seed `taxi_zone_lookup`.

---

## **4.4.2.2 - dbt Macros: "Sihir" SQL yang Bisa Dipakai Ulang**

Pernahkah kamu menulis `CASE WHEN` yang sama di sepuluh file SQL yang berbeda? Itu sangat melelahkan dan rawan salah. **Macros** adalah cara dbt untuk membuat fungsi di dalam SQL.

- **Masalah:** Kode `CASE WHEN vendorid = 1 THEN 'Creative...'` jika ditulis berulang kali akan jadi "spaghetti code".
- **Solusi:** Bungkus logika tersebut di dalam file `.sql` di folder `macros/` menggunakan bahasa **Jinja**.

**Contoh Struktur Macro:**

```sql
{% macro get_payment_type_description(payment_type) %}
    case {{ payment_type }}
        when 1 then 'Credit card'
        when 2 then 'Cash'
        when 3 then 'No charge'
        ...
    end
{% endmacro %}

```

**Cara Panggil di Model:**
`{{ get_payment_type_description('payment_type') }} as payment_type_description`

---

## **4.4.2.3 - Kenapa Pakai Macro Lebih Baik?**

1. **DRY (Don't Repeat Yourself):** Tulis sekali, pakai di mana saja.
2. **Single Source of Truth:** Jika nama Vendor berubah, saya cukup ganti di satu file Macro, dan semua tabel yang menggunakannya akan otomatis terupdate.
3. **Clean Code:** File model SQL saya jadi lebih pendek dan fokus pada logika transformasi utama, bukan detail-detail kecil pemetaan kode.

---

## **4.4.2.4 - Persiapan "Boss Level": `fct_trips`**

Di akhir materi ini, ada tugas besar (PR) untuk membuat model `fct_trips`. Ini adalah tabel fakta utama yang menggabungkan segalanya. Hal yang harus diperhatikan:

- **Primary Key:** Harus buat `trip_id` yang unik.
- **Handling Duplicates:** Data taksi NYC terkenal banyak data ganda. Kita harus belajar cara membersihkannya sebelum masuk ke tabel fakta.
- **Enrichment:** Gabungkan data dari `dim_zones` untuk tahu lokasi jemput/antar, dan gunakan Macro/Seeds untuk memperjelas jenis pembayaran.

---

## 📚 Apa yang Saya Pelajari

- **Kekuatan Seeds:** Saya merasa sangat terbantu karena bisa memasukkan tabel referensi kecil tanpa perlu minta bantuan admin database untuk membuat tabel baru.
- **Pemrograman di dalam SQL:** Jinja dan Macros membuka pikiran saya bahwa SQL bisa sefleksibel Python. Kita bisa menggunakan _looping_ (`for`) dan _conditional_ (`if`) di dalam query kita.
- **Efisiensi Kerja:** Saya belajar bahwa dengan Macro, saya bisa membangun "perpustakaan logika bisnis" sendiri yang bisa saya bawa ke proyek-proyek masa depan.
- **Integritas Data:** Menciptakan `trip_id` yang unik dan menangani duplikat adalah ujian sesungguhnya bagi seorang Analytics Engineer untuk memastikan laporan akhirnya akurat.

---

## 📌 Summary

Seeds memudahkan kita memasukkan data pendukung kecil, sementara Macros membuat kode SQL kita menjadi modular dan mudah dikelola. Keduanya adalah alat wajib bagi seorang Analytics Engineer untuk mengubah data mentah menjadi informasi yang bersih, berstandar, dan punya konteks bisnis.

> **📝 Note:** _Gunakan Seeds untuk data yang jarang berubah, gunakan Macros untuk logika yang sering diulang. Dan ingat: jangan pernah menaruh password di folder seeds!_

---

# 📖 4.5.1-Documentation

> **Topik:** Menulis Dokumentasi di YAML, Meta Tags, dan Lineage Graph

Bayangkan jika kamu cuti, lalu rekan timmu harus memperbaiki model `fct_trips` yang kamu buat. Tanpa dokumentasi, mereka akan tersesat. dbt memudahkan kita membuat dokumentasi teknis yang sangat rapi langsung dari kode kita.

---

## **4.5.1.1 - Di Mana Dokumentasi Ditulis? (YAML)**

Di dbt, dokumentasi tidak ditaruh di dalam file `.sql`, melainkan di dalam file `.yml`.

- **Konvensi:** Biasanya kita membuat file bernama `schema.yml` di setiap folder (Staging, Core, dsb).
- **Fleksibilitas:** Kamu bisa punya satu YAML raksasa, atau satu YAML per satu model. Yang penting konsisten.

---

## **4.5.1.2 - Apa Saja yang Bisa Didokumentasikan?**

Hampir semua objek di dbt bisa diberi keterangan:

1. **Sources:** Jelaskan asal data mentah tersebut (misal: "Data dari API eksternal Vendor X").
2. **Models:** Jelaskan tujuan tabel tersebut (misal: "Tabel fakta untuk analisis bulanan").
3. **Columns:** Jelaskan arti dari setiap kolom, tipe datanya, dan aturan bisnisnya.
4. **Macros & Seeds:** Kamu juga bisa menjelaskan fungsi macro yang kamu buat.

**Tips Menulis Deskripsi Panjang:**
Gunakan operator `>` (untuk teks mengalir) atau `|` (untuk menjaga baris baru) agar file YAML tetap enak dibaca.

---

## **4.5.1.3 - Meta Tags: Metadata Kustom**

Fitur `meta` memungkinkan kita menambahkan label tambahan yang kita tentukan sendiri. Ini sangat berguna untuk **Data Governance**:

- **PII (Personally Identifiable Information):** Tandai kolom sensitif (seperti email atau nomor telepon).
- **Owner:** Siapa yang bertanggung jawab atas model ini?
- **Priority:** Seberapa krusial tabel ini untuk bisnis?

Contoh:

```yaml
columns:
  - name: customer_email
    meta:
      contains_pii: true
      owner: "@tim_marketing"
```

---

## **4.5.1.4 - Menghasilkan & Melihat Dokumentasi**

Setelah semua YAML terisi, ada dua langkah ajaib (terutama untuk pengguna **dbt Core**):

1. **`dbt docs generate`**: dbt akan mengumpulkan semua file SQL, YAML, dan metadata dari database (seperti ukuran tabel) ke dalam satu file JSON.
2. **`dbt docs serve`**: dbt akan menyalakan server lokal sehingga kamu bisa membuka dokumentasi tersebut di browser.

**Apa yang akan kamu lihat di sana?**

- **Compiled SQL:** Kamu bisa melihat SQL asli yang dijalankan dbt setelah semua Macro dan Jinja diterjemahkan.
- **Lineage Graph (DAG):** Ini adalah fitur favorit saya! Kamu bisa melihat peta visual aliran data dari hijau (Source) ke model akhir secara grafis. Kamu tahu persis jika tabel A berubah, tabel mana saja yang akan terkena dampaknya.

---

## 📚 Apa yang Saya Pelajari

- **Dokumentasi sebagai Kode:** Saya belajar bahwa dokumentasi bukan beban terpisah, tapi bagian dari workflow pengembangan. Menulisnya di YAML terasa lebih terstruktur daripada menulis di Wiki manual.
- **Kekuatan Visualisasi (Lineage):** Lineage Graph sangat membantu saya menjelaskan ke orang lain bagaimana data taksi kuning dan hijau akhirnya bersatu. Ini jauh lebih mudah dipahami daripada membaca ribuan baris kode.
- **Transparansi Tim:** Dengan `meta` tags, tim saya bisa tahu siapa yang harus dihubungi jika sebuah tabel error, dan kolom mana yang harus dijaga kerahasiaannya.
- **Efisiensi Debugging:** Fitur melihat _Compiled SQL_ di dbt docs sangat membantu saat saya ingin memastikan apakah Macro yang saya buat sudah mengeluarkan perintah SQL yang benar atau belum.

---

## 📌 Summary

Dokumentasi dbt adalah "peta" bagi siapa saja yang bekerja di dalam data warehouse. Dengan menggabungkan deskripsi kolom, metadata kustom, dan grafik silsilah data (_Lineage_), kita memastikan bahwa gudang data kita tetap teratur, transparan, dan mudah dikelola seiring berkembangnya proyek.

> **📝 Note:** _Jangan tunggu project selesai baru menulis dokumentasi. Tulis dokumentasi saat kamu membuat modelnya. Dokumentasi yang telat biasanya berakhir jadi dokumentasi yang tidak pernah dibuat._

---

# 🛡️ 4.5.2-dbt Tests

> **Topik:** Menjamin Kualitas Data Secara Proaktif

Dunia data itu berantakan. Terkadang datanya yang aneh, terkadang SQL kita yang salah. **Testing** adalah cara kita memastikan bahwa apa yang sampai ke dashboard adalah data yang valid dan bisa dipercaya oleh bisnis.

---

## **1. Singular Tests (Kustom SQL)**

Jenis tes paling dasar. Menulis query SQL yang mencari "data sampah".

- **Aturan:** Jika query menghasilkan baris (>0), maka test **GAGAL**.
- **Lokasi:** Disimpan di folder `tests/`.
- **Cocok untuk:** Aturan bisnis yang sangat spesifik.
- _Contoh:_ "Total biaya perjalanan tidak boleh negatif."

```sql
-- tests/assert_fare_positif.sql
select * from {{ ref('fct_trips') }} where fare_amount < 0

```

---

## **2. Source Freshness (Cek Kesegaran Data)**

Jangan sampai bos melihat data kemarin padahal seharusnya data hari ini.

- **Fungsi:** Memeriksa kapan terakhir kali data masuk ke database.
- **Cara kerja:** Kita tentukan kolom penanda waktu (misal: `pickup_datetime`) dan beri batas waktu (misal: beri peringatan jika data lebih dari 6 jam, error jika lebih dari 12 jam).
- **Lokasi:** Dikonfigurasi di file `sources.yml`.

---

## **3. Generic Tests (Tes Reusable di YAML)**

Ini adalah jenis tes yang paling sering digunakan karena sangat efisien. Cukup tulis di file YAML, dbt yang akan menjalankan SQL-nya.

### **The "Big Four" (Bawaan dbt):**

1. **`unique`**: Pastikan tidak ada duplikat (cocok untuk Primary Key).
2. **`not_null`**: Kolom wajib diisi, tidak boleh kosong.
3. **`accepted_values`**: Isi kolom harus sesuai daftar (misal: status harus 'Cash' atau 'Credit').
4. **`relationships`**: Pastikan ID di tabel A ada di tabel referensi B (Integritas Referensial).

**Tips Pro:** Jangan buat tes sendiri dari nol jika tidak perlu. Gunakan package komunitas seperti **dbt-utils** atau **dbt-expectations** yang punya ratusan jenis tes siap pakai.

---

## **4. Unit Tests (Tes Logika Terisolasi)**

Fitur baru (sejak dbt v1.8) untuk mengetes apakah rumus SQL kita benar tanpa menyentuh data asli.

- **Konsep:** Kita buat data "palsu" (mock data) dan kita tentukan hasil yang diharapkan.
- **Kegunaan:** Sangat bagus untuk mengetes logika yang rumit (seperti perhitungan pajak atau regex) di dalam pipeline CI/CD sebelum kode masuk ke produksi.

---

## **5. Model Contracts (Kontrak Skema)**

Jika tes lain menangkap error _setelah_ data diproses, **Contracts** mencegah model dijalankan jika bentuknya salah.

- **Fungsi:** Memaksa model untuk mengikuti aturan skema yang ketat (nama kolom harus pas, tipe data harus cocok).
- **Kegunaan:** Ini adalah "perjanjian" antara kita dan pengguna data. Jika kita tidak sengaja mengubah nama kolom yang dipakai dashboard, dbt akan langsung error dan berhenti sebelum merusak laporan.

---

## 📚 Apa yang Saya Pelajari

- **Mindset Defensif:** Saya belajar bahwa tugas saya bukan cuma mengalirkan data, tapi memastikan data tersebut **benar**. Testing membuat saya lebih percaya diri saat merilis kode baru.
- **Efisiensi YAML:** Saya sangat suka bagaimana dbt menyatukan dokumentasi dan testing di satu tempat (`schema.yml`). Ini membuat kode saya rapi dan teruji sekaligus.
- **Deteksi Dini:** Dengan _Source Freshness_, saya bisa tahu kalau pipeline upstream (E/L) macet sebelum orang bisnis komplain dashboard-nya tidak update.
- **Kolaborasi Terjaga:** _Model Contracts_ adalah penyelamat saat bekerja dalam tim besar. Ini mencegah perubahan yang tidak sengaja merusak sistem hilir (_downstream_).

---

## 📌 Summary

Testing di dbt bukan sekadar opsi, tapi kebutuhan. Gunakan **Generic Tests** untuk pengecekan rutin, **Singular Tests** untuk logika bisnis unik, dan **Model Contracts** untuk menjaga stabilitas arsitektur data.

> **📝 Note:** _Menjalankan `dbt run` tanpa `dbt test` itu seperti memasak tanpa mencicipi. kita tidak akan pernah tahu kalau masakanmu terlalu asin sampai tamu (pengguna data) yang mengatakannya!_

---

# 📦 4.5.3-dbt Packages

> **Topik:** Menggunakan "Library" dbt untuk Mempercepat Workflow

Jika di Python kita punya `pip install`, di dbt kita punya **Packages**. Paket-paket ini adalah kumpulan model, macro, dan test yang sudah dibuat oleh orang lain (atau dbt Labs) dan bisa kita gunakan secara gratis di proyek kita.

---

## **4.5.3.1 - Paket yang "Wajib" Ada di Proyek**

Ada beberapa paket yang sudah menjadi standar industri:

1. **`dbt-utils` (Si Pisau Lipat):**

- Wajib di-install! Berisi fungsi-fungsi SQL umum yang sering bikin pusing kalau ditulis manual.
- **Fitur andalan:** `generate_surrogate_key`. Ini cara termudah untuk membuat _Primary Key_ unik dari gabungan beberapa kolom secara otomatis dan aman di berbagai database (BigQuery, Snowflake, dll).

2. **`dbt-codegen` (Si Pengetik Otomatis):**

- Sangat membantu untuk malas mengetik! Paket ini bisa membuatkan file `schema.yml` atau skrip model staging secara otomatis hanya dengan membaca tabel di database.

3. **`dbt-expectations` (Si Polisi Data):**

- Menambahkan puluhan jenis test baru yang tidak ada di bawaan dbt. Misalnya: cek apakah format email benar, cek apakah nilai kolom ada di rentang tertentu, dll.

4. **`dbt-audit-helper` (Si Teman Refactoring):**

- Sangat berguna kalau sedang merombak SQL lama ke SQL baru. Paket ini akan membandingkan hasil kedua query tersebut dan memberi tahu jika ada baris atau nilai yang berbeda.

---

## **4.5.3.2 - Cara Instalasi & Penggunaan**

Prosesnya sangat sederhana:

1. **Buat file `packages.yml`:** Letakkan di folder utama proyek (sejajar dengan `dbt_project.yml`).
2. **Tulis paket yang diinginkan:** Ambil kode versinya dari [hub.getdbt.com](https://hub.getdbt.com).
3. **Jalankan `dbt deps`:** Perintah ini akan mengunduh paket tersebut ke folder `dbt_packages/`.

**Contoh Penggunaan Macro dari Paket:**
Misalnya kita ingin membuat `trip_id` yang unik menggunakan `dbt-utils`:

```sql
select
    {{ dbt_utils.generate_surrogate_key(['vendorid', 'lpep_pickup_datetime']) }} as trip_id,
    vendorid,
    lpep_pickup_datetime
from ...

```

---

## **4.5.3.3 - Kenapa Harus Pakai Packages?**

- **Jangan Re-invent the Wheel:** Masalah yang dihadapi (misal: buat surrogate key) pasti sudah pernah dihadapi ribuan orang lain. Pakai solusi yang sudah teruji.
- **Kompatibilitas Lintas Database:** Macro di dalam paket biasanya sudah didesain agar bisa jalan di BigQuery maupun Postgres tanpa perlu ubah kode SQL-nya.
- **Standarisasi:** Menggunakan paket populer membuat proyek lebih mudah dipahami oleh engineer lain karena mereka sudah familiar dengan fungsi-fungsinya.

---

## 📚 Apa yang Saya Pelajari

- **Efisiensi adalah Kunci:** Saya belajar bahwa sebagai Data Engineer, kita harus bekerja cerdas. Menggunakan `dbt-codegen` bisa menghemat waktu berjam-jam yang biasanya habis cuma buat ngetik nama kolom di YAML.
- **Keamanan & Kepercayaan:** Saya tahu sekarang bahwa paket yang ada di dbt Hub sudah melalui kurasi, jadi lebih aman digunakan daripada sekadar copy-paste kode dari internet.
- **Surrogate Keys yang Mudah:** Dulu saya bingung cara buat ID unik dari gabungan kolom (konkatenasi string itu rawan error). Sekarang cukup satu baris macro `dbt_utils.generate_surrogate_key`.
- **Komunitas yang Kuat:** Kekuatan dbt bukan cuma di software-nya, tapi di ekosistemnya. Dengan packages, kita "berdiri di atas bahu para raksasa".

---

## 📌 Summary Module-04

Kita sudah belajar:

1. **Arsitektur:** Core vs Cloud dan masa depan dengan Fusion.
2. **Struktur:** Folder staging, intermediate, dan marts.
3. **Transformasi:** Menggunakan SQL, Jinja, dan Macro.
4. **Governance:** Dokumentasi dan Testing yang ketat.
5. **Ekosistem:** Mempercepat kerja dengan Packages.

> **📝 Note:** _Gunakan paket seperlunya. Terlalu banyak paket juga bisa membuat proyek jadi berat saat di-load. Pilihlah yang benar-benar memberikan nilai tambah bagi workflow._

---

# ⌨️ 4.6.1 — dbt Commands: The Power User Guide

> **Topik:** Navigasi CLI, Automasi Workflow, dan Seleksi Node.

Di bagian ini, kita akan membedah perintah dari yang paling dasar hingga fitur canggih seperti `state:modified` yang sangat berguna untuk efisiensi biaya di cloud.

---

## **4.6.1.1 — Perintah Persiapan (Setup)**

Perintah ini biasanya dijalankan di awal proyek atau saat terjadi masalah koneksi.

- `dbt init`: Membangun fondasi. Hanya dijalankan sekali untuk membuat struktur folder.
- `dbt debug`: Sahabat terbaik saat error koneksi. Ia mengecek file `profiles.yml` dan memastikan "jembatan" ke database aman.
- `dbt deps`: Mengambil "buku library" (packages) yang kita daftarkan di `packages.yml`.
- `dbt clean`: Menghapus file sampah di folder `target/`. Gunakan ini jika dbt terasa "aneh" atau ingin kompilasi yang benar-benar baru.

---

## **4.6.1.2 — The Big Four: Penggerak Utama**

Ini adalah perintah yang akan paling sering diketik setiap harinya.

| Command         | Fungsi Utama                     | Kenapa Penting?                                                                                            |
| --------------- | -------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `dbt compile`   | Menerjemahkan Jinja ke SQL asli. | Gratis (tanpa biaya warehouse) dan sangat cepat untuk cek error typo.                                      |
| `dbt run`       | Mengeksekusi model di database.  | Mengubah kode SQL menjadi tabel/view nyata di warehouse.                                                   |
| `dbt test`      | Menjalankan validasi data.       | Memastikan data tidak "rusak" sebelum dikonsumsi pengguna.                                                 |
| **`dbt build`** | **The All-in-One**               | **Standard Industri.** Menjalankan seed -> run -> test -> snapshot secara otomatis dan cerdas (DAG-aware). |

> **Pro Tip:** Gunakan **`dbt build`** sebagai perintah utama di sistem produksi (CI/CD). Jika satu model gagal ditest, dbt akan otomatis berhenti dan tidak menjalankan model di bawahnya, mencegah data sampah menyebar.

---

## **4.6.1.3 — Navigasi dan Seleksi (Flags)**

Inilah senjatamu untuk menghemat waktu. Jangan jalankan seluruh proyek jika kamu hanya mengubah satu baris kode!

### **Seleksi dengan Operator `+` (Graph Operators)**

Gunakan tanda tambah untuk menentukan arah dependensi:

- `dbt run -s stg_green_tripdata+`: Jalankan model ini **DAN semua yang ada di bawahnya (descendants).**
- `dbt run -s +stg_green_tripdata`: Jalankan model ini **DAN semua sumbernya (ancestors).**
- `dbt run -s +stg_green_tripdata+`: Jalankan **seluruh jalur** yang melewati model ini.

### **State Selectors (Sihir CI/CD)**

`dbt build --select state:modified+ --state ./prod-artifacts`

- Ini adalah fitur tercanggih. dbt membandingkan kode kamu saat ini dengan file `manifest.json` dari proses sebelumnya.
- Ia hanya akan menjalankan model yang **berubah** saja. Sangat hemat waktu dan biaya!

---

## **4.6.1.4 — Perintah Tambahan yang Berguna**

- `dbt retry`: Jika mati lampu atau koneksi putus tengah jalan, jangan ulangi dari awal. Perintah ini akan melanjutkan dari model terakhir yang gagal.
- `dbt docs generate && dbt docs serve`: Membuat website katalog data instan untuk kamu jelajahi di browser.
- `dbt source freshness`: Pastikan data mentahmu tidak "basi" (masih update sesuai jadwal).

---

## 📚 Apa yang Berhasil Saya Pelajari

- **Efisiensi Terminal:** Saya belajar bahwa tidak perlu menjalankan `dbt run` untuk seluruh project. Flag `-s` (select) adalah kunci produktivitas.
- **Keamanan Produksi:** `dbt build` adalah pengaman. Ia memastikan data tidak hanya _selesai_ diproses, tapi juga _benar_ (lewat testing) sebelum lanjut ke tahap berikutnya.
- **Debugging Tanpa Biaya:** `dbt compile` adalah cara jenius untuk mengecek logika Jinja tanpa harus membayar biaya komputasi di BigQuery atau Snowflake.
- **Manajemen State:** Memahami bahwa `manifest.json` adalah "ingatan" dbt yang memungkinkan fitur seleksi cerdas seperti `state:modified`.

---

## 📌 Summary

Menguasai dbt CLI bukan hanya soal menghafal perintah, tapi tahu kapan harus menggunakan flag yang tepat. Sebagai pemula, mulailah membiasakan diri menggunakan `dbt build` dan flag `--select`. Di dunia kerja, kemampuanmu melakukan _selective run_ akan sangat dihargai karena menghemat ribuan dolar biaya cloud perusahaan.

> **📝 Note:** _Selalu ingat untuk menjalankan `dbt deps` jika kamu baru meng-clone proyek dbt dari GitHub, atau perintah `run` kamu akan gagal karena kehilangan library!_

---

### 💡 Tips

Selalu biasakan untuk menjalankan **`dbt build`** daripada hanya `dbt run`, karena `build` akan otomatis mengecek kualitas data melalui test segera setelah tabel dibuat. Jika test gagal, dbt akan menghentikan proses sebelum data "sampah" tersebut dipakai oleh model di bawahnya.

Jika ingin melihat video lengkapnya lagi, silakan akses di sini: [https://www.youtube.com/watch?v=t4OeWHW3SsA](https://www.youtube.com/watch?v=t4OeWHW3SsA)

---
