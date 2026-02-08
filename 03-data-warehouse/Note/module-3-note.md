# 🏛️ 03-Data Warehouse and BigQuery

> **Topik:** Arsitektur Data Warehouse, Optimasi Query, dan Strategi Biaya

Sekarang saya belajar ke mana data tersebut harus bermuara. Di module ini, fokusnya bukan lagi soal cara memindahkan data, tapi bagaimana menyimpan dan mengolah data dalam skala _Petabyte_ secara efisien menggunakan **Google BigQuery**.

---

## **3.1 - OLAP vs OLTP**

Sebagai Data Engineer, saya harus tahu kapan menggunakan database biasa dan kapan menggunakan Data Warehouse. Berikut adalah perbandingan mendalam yang saya pelajari:

| Fitur             | OLTP (_Online Transactional Processing_)                 | OLAP (_Online Analytical Processing_)                        |
| ----------------- | -------------------------------------------------------- | ------------------------------------------------------------ |
| **Tujuan**        | Menjalankan operasional bisnis inti secara _real-time_.  | Perencanaan, pemecahan masalah, dan pencarian _insight_.     |
| **Update Data**   | Update singkat dan cepat oleh _user_ (misal: klik beli). | Di-refresh berkala lewat _scheduled batch jobs_ yang lama.   |
| **Desain DB**     | **Normalized** (untuk efisiensi transaksi).              | **Denormalized** (untuk efisiensi analisis).                 |
| **Space**         | Biasanya kecil (data historis sering diarsip).           | Sangat besar karena agregasi dataset masif.                  |
| **Backup**        | Sangat krusial untuk kontinuitas bisnis.                 | Data bisa di-load ulang dari OLTP jika diperlukan.           |
| **Produktivitas** | Meningkatkan produktivitas _end-user_ (staf/pembeli).    | Membantu manajer, analis, dan eksekutif mengambil keputusan. |
| **View Data**     | List transaksi harian.                                   | Tampilan multi-dimensi dari data perusahaan.                 |
| **User**          | Kasir, staf admin, pembeli online.                       | Data Analyst, Business Analyst, Eksekutif.                   |

---

## **3.2 - Data Warehouse & BigQuery**

**Data Warehouse** adalah solusi penyimpanan sentral yang mengonsolidasikan data dari berbagai sumber untuk tujuan pelaporan dan analisis.

### Mengapa BigQuery Sangat _Powerful_?

BigQuery bukan sekadar database, tapi platform analisis modern dengan karakteristik:

- **Serverless Data Warehouse:** Tidak ada server yang harus saya kelola atau software yang perlu di-install. Google menangani semuanya.
- **Scalability & High-Availability:** Infrastruktur dan skalabilitasnya sudah terjamin secara bawaan (_built-in_).
- **Built-in Features:** Sudah dilengkapi dengan **Machine Learning**, **Geospatial Analysis**, dan **Business Intelligence**.
- **Separation of Compute & Storage:** Ini fitur favorit saya. BigQuery memisahkan _engine_ komputasi (yang menganalisis data) dari tempat penyimpanannya. Artinya, saya bisa menyimpan banyak data tanpa harus membayar komputasi jika tidak sedang di-query.

---

## **3.3 - BigQuery Cost (Skema Biaya)**

Memahami biaya adalah tugas wajib Data Engineer agar tagihan GCP tidak "meledak". BigQuery menawarkan dua model utama:

1. **On-Demand Pricing (Pay-as-you-go):**

- Biaya dihitung berdasarkan jumlah data yang diproses.
- Standarnya: **$5 per 1 TB** data yang di-scan.
- _Catatan:_ Sangat cocok untuk _workload_ yang tidak menentu atau tahap belajar.

2. **Flat Rate (Capacity) Pricing:**

- Berdasarkan jumlah **Slots** (unit komputasi virtual) yang dipesan di awal.
- Contoh: **100 slots ≈ $2,000/bulan**.
- Ini setara dengan memproses **400 TB** data pada model _on-demand_. Jika query bulanan saya lebih dari 400 TB, model ini jauh lebih murah.

---

## **3.4 - Partitioning and Clustering**

Di BigQuery, cara kita menyimpan data sangat menentukan seberapa cepat dan murah query kita nantinya. Dua teknik utamanya adalah Partitioning dan Clustering.

### **3.4.1 - BigQuery Partitioning**

Partitioning adalah cara membagi tabel besar menjadi segmen-segmen kecil (partisi). Ibarat membagi satu buku besar menjadi beberapa bab berdasarkan waktu.

**Jenis Partitioning:**

- **Time-unit column:** Berdasarkan kolom waktu (DATE, TIMESTAMP, atau DATETIME).
- **Ingestion time:** Berdasarkan waktu saat data masuk ke BigQuery (`_PARTITIONTIME`).
- **Integer range partitioning:** Berdasarkan rentang angka (misal: ID atau tahun dalam bentuk integer).

**Aturan Main:**

- **Granularitas:** Bisa diatur per jam (**Hourly**), per hari (**Daily** - _Default_), per bulan (**Monthly**), atau per tahun (**Yearly**).
- **Limit:** Maksimal **4000 partisi** per tabel. Jadi, jangan sampai bikin partisi harian untuk data lebih dari 10 tahun kalau tidak perlu!

---

### **3.4.2 - BigQuery Clustering**

Jika Partitioning membagi data ke "laci", **Clustering** adalah cara menyusun dokumen di dalam laci tersebut agar yang mirip selalu berdekatan (_colocated_).

**Karakteristik Utama:**

- **Urutan Kolom Sangat Penting:** Performa query bergantung pada urutan kolom yang kita pilih saat membuat tabel.
- **Meningkatkan Performa:** Sangat membantu untuk query yang menggunakan filter (`WHERE`) dan agregasi (`GROUP BY`).
- **Batasan:** - Maksimal **4 kolom** per tabel.
- Kolom harus di level teratas (_top-level_) dan bukan kolom berulang (_non-repeated_).
- Tipe data yang didukung: `DATE`, `BOOL`, `GEOGRAPHY`, `INT64`, `NUMERIC`, `BIGNUMERIC`, `STRING`, `TIMESTAMP`, `DATETIME`.

- **Minimal Size:** Kalau data tabel kamu **< 1 GB**, teknik ini biasanya tidak memberikan efek yang signifikan.

---

### **3.4.3 - Partitioning vs Clustering: Mana yang Dipilih?**

Saya belajar bahwa keduanya punya kelebihan masing-masing. Ini perbandingannya:

| Fitur              | Partitioning                                        | Clustering                                                         |
| ------------------ | --------------------------------------------------- | ------------------------------------------------------------------ |
| **Estimasi Biaya** | Bisa diketahui di depan (_upfront_).                | Tidak diketahui di depan (_unknown_).                              |
| **Manajemen**      | Perlu manajemen level partisi (hapus/copy partisi). | Otomatis dikelola oleh BigQuery.                                   |
| **Kegunaan**       | Filter pada satu kolom (biasanya waktu).            | Filter/Agregasi pada banyak kolom sekaligus.                       |
| **Granularitas**   | Terbatas (misal: hanya per hari/bulan).             | Sangat detail (berdasarkan nilai kolom).                           |
| **Kapan Dipakai?** | Saat kita tahu filter utama adalah waktu.           | Saat kolom filter punya banyak variasi nilai (_high cardinality_). |

---

### **3.4.4 - Kapan Memilih Clustering di atas Partitioning?**

Ada kalanya saya lebih baik menggunakan Clustering saja (atau kombinasi keduanya):

1. **Data Partisi Terlalu Kecil:** Jika satu partisi isinya **kurang dari 1 GB**, partitioning malah bikin berat metadata.
2. **Melebihi Limit:** Jika jumlah partisi potensial kamu lebih dari **4000**.
3. **Terlalu Sering Berubah (Mutasi):** Jika operasional kamu sering mengubah data di hampir semua partisi secara rutin (misal tiap beberapa menit), Clustering lebih efisien.

---

## **3.5 - BigQuery Best Practices**

Setelah menguasai teknik penyimpanan, sekarang saya fokus pada efisiensi operasional. BigQuery itu sangat _powerful_, tapi kalau tidak hati-hati, kita bisa "menghamburkan" uang dan waktu.

### **3.5.1 - Strategi Penghematan Biaya (Cost Reduction)**

Menghemat biaya di BigQuery bukan cuma soal irit, tapi soal efisiensi desain.

- **Haram Hukumnya `SELECT *`:** Selalu ambil kolom yang memang dibutuhkan. BigQuery menarik biaya berdasarkan volume data yang dibaca per kolom.
- **Cek Harga Sebelum Eksekusi:** Biasakan melihat estimasi _bytes processed_ di pojok kanan atas UI BigQuery sebelum menekan tombol _Run_.
- **Maksimalkan Partisi & Cluster:** Selalu gunakan tabel yang sudah dipartisi/cluster untuk membatasi data yang di-scan.
- **Waspada Streaming Inserts:** Gunakan _streaming inserts_ hanya jika benar-benar butuh data _real-time_, karena biayanya jauh lebih mahal daripada _batch load_.
- **Materialisasi Bertahap:** Jika query sangat kompleks dan panjang, lebih baik simpan hasil sementara ke dalam tabel permanen (_materialize_) daripada menjalankan query yang sama berulang kali.

---

### **3.5.2 - Optimasi Performa Query (Query Performance)**

Kecepatan query sangat bergantung pada cara kita menulis SQL dan struktur data.

- **Filter di Kolom Partisi:** Pastikan `WHERE` clause selalu menyasar kolom yang dipartisi.
- **Denormalisasi & Nested Fields:** Jangan takut dengan data yang "lebar". Gunakan _Nested_ atau _Repeated columns_ (format JSON-like) untuk mengurangi kebutuhan _JOIN_ yang berat.
- **Gunakan External Data Source Secara Bijak:** Mengambil data langsung dari GCS atau Google Sheets memang praktis, tapi jangan berharap performa tinggi. Pindahkan data ke _native storage_ BigQuery untuk kecepatan maksimal.
- **Kurangi Data Sebelum JOIN:** Lakukan agregasi atau filter sebanyak mungkin sebelum menggabungkan dua tabel besar.
- **Hati-hati dengan `WITH` Clause:** Jangan anggap CTE (`WITH`) sebagai _prepared statements_. BigQuery akan mengevaluasi CTE setiap kali dipanggil, bukan menyimpannya di memori satu kali saja.
- **Hindari Oversharding:** Jangan pecah tabel menjadi ribuan tabel kecil (misal: tabel per hari `taxi_data_20240101`). Lebih baik gunakan **Partitioning**.

---

### **3.5.3 - Teknik Lanjutan untuk Performa Maksimal**

- **Hindari JavaScript UDF:** Jika bisa pakai SQL murni, pakai SQL. JavaScript UDF jauh lebih lambat.
- **Gunakan Agregasi Perkiraan (Approximate Functions):** Untuk dataset raksasa yang tidak butuh presisi 100% (misal: jumlah user unik), gunakan `HyperLogLog++` (fungsi `APPROX_COUNT_DISTINCT`). Ini jauh lebih cepat daripada `COUNT(DISTINCT)`.
- **`ORDER BY` Taruh di Paling Akhir:** Pengurutan data adalah operasi yang sangat mahal. Lakukan hanya jika benar-benar diperlukan di hasil akhir.
- **Optimasi Pola JOIN:** Aturan emasnya adalah: **Letakkan tabel terbesar di urutan pertama**, diikuti oleh tabel yang lebih kecil, lalu sisa tabel lainnya berdasarkan ukuran yang semakin mengecil. Ini membantu BigQuery mendistribusikan data ke _worker_ secara efisien.

---

## **3.6 - Machine Learning in Big Query (BQML)**

Biasanya, untuk melakukan Machine Learning, kita harus memindahkan data dari database ke _environment_ lain (seperti Jupyter Notebook) menggunakan Python atau R. Tapi di BigQuery, saya belajar bahwa kita bisa melakukannya **langsung di dalam gudang data**.

### **3.6.1 - Mengapa BQML Sangat Revolusioner?**

- **Target Audience:** Sangat cocok untuk **Data Analyst** dan **Manager**. Kamu tidak perlu menjadi seorang _Hardcore Programmer_ untuk bisa membuat model prediksi.
- **No Python/Java Needed:** Cukup gunakan **SQL**. Jika kamu bisa menulis `SELECT`, kamu bisa membuat model ML.
- **Data Residency:** Data tidak perlu diekspor ke sistem lain. Ini jauh lebih aman (security) dan lebih cepat karena tidak ada proses _data movement_ yang memakan waktu.

---

### **3.6.2 - Skema Harga BQML (ML in BigQuery Pricing)**

Google menyediakan _Free Tier_ yang cukup murah hati untuk kita yang sedang belajar:

| Kategori                 | Batas Gratis (Per Bulan)                    |
| ------------------------ | ------------------------------------------- |
| **Data Storage**         | 10 GB pertama gratis.                       |
| **Queries Processed**    | 1 TB pertama gratis.                        |
| **ML Create Model Step** | 10 GB pertama untuk pembuatan model gratis. |

_Setelah melewati batas ini, biaya akan dihitung berdasarkan model pricing BigQuery yang sudah kita bahas sebelumnya._

---

## 📚 Apa yang Berhasil Saya Pelajari

- **Paradigma Denormalisasi:** Jika di Module-01 (Postgres) saya belajar menormalisasi data, di BigQuery saya belajar bahwa tabel yang "lebar" (denormalized) justru lebih baik untuk kecepatan analisis.
- **Pentingnya Cost Management:** Dengan harga **$5/TB**, saya harus sangat hati-hati dengan `SELECT *`. Mengambil kolom yang diperlukan bukan cuma soal rapi, tapi soal hemat uang.
- **Serverless adalah penyelamat:** Saya bisa fokus pada logika SQL dan arsitektur data tanpa perlu pusing memikirkan _patching_ OS atau konfigurasi server hardware.
- **Fleksibilitas Komputasi & Storage:** Pemisahan _compute_ dan _storage_ memungkinkan saya menyimpan data historis NYC Taxi bertahun-tahun dengan biaya murah, dan hanya membayar mahal saat saya benar-benar melakukan analisis besar.
- **Demokratisasi AI:** Machine Learning bukan lagi "barang mewah" yang hanya bisa disentuh oleh Data Scientist dengan gelar PhD. Dengan BQML, Data Engineer bisa menyiapkan pipeline yang langsung menghasilkan prediksi.
- **Efisiensi Alur Kerja:** Mengurangi proses _Export-Transform-Load_ ke sistem ML eksternal sangat menghemat waktu. Ini adalah prinsip **"Bring the code to the data, not the data to the code"**.
- **SQL Power-Up:** Kemampuan SQL saya sekarang tidak hanya untuk melihat masa lalu (laporan), tapi juga untuk memprediksi masa depan (forecast).
- **Belajar Tanpa Takut:** Adanya _Free Tier_ (10GB/1TB) membuat saya merasa tenang untuk mencoba-coba membuat model regresi linear atau klasifikasi sederhana menggunakan data NYC Taxi tanpa takut tagihan membengkak di awal.

---

## 📌 Summary

BigQuery ML melengkapi ekosistem Data Warehouse menjadi sebuah platform analitik yang utuh. Dengan menghilangkan kebutuhan untuk memindahkan data dan menggunakan bahasa SQL yang sudah umum, BQML memungkinkan kita untuk mendapatkan _insight_ prediktif lebih cepat daripada metode tradisional.

> **📝 Note:** _Jangan meremehkan kekuatan SQL. Di dalam BigQuery, SQL bukan lagi sekadar bahasa query, tapi sudah menjadi bahasa pemrograman untuk kecerdasan buatan (AI)._

---
