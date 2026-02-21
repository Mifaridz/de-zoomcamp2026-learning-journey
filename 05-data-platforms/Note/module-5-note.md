# 🧩 05 — Data Platforms Using Bruin

> **Topik:** Definisi Data Platform, Modern Data Stack, dan Pengenalan Bruin.

---

# 5.1 - Introduction to Bruin

## **5.1.1 — Apa itu Bruin?**

Bruin adalah _end-to-end data platform_ yang menggabungkan berbagai fungsi yang biasanya terpisah menjadi satu alat tunggal.

- **All-in-One:** Ingesti, transformasi, orkestrasi, pengecekan kualitas data, metadata, hingga _lineage_ ada di dalam satu platform.
- **Single Place of Truth:** Alih-alih mengonfigurasi 5 atau 6 alat berbeda secara terpisah, Bruin memungkinkan kita menaruh logika kode, konfigurasi, dependensi, dan _quality checks_ di tempat yang sama.

---

## **5.1.2 — Komponen Modern Data Stack**

Dalam ekosistem data modern, biasanya kita butuh komponen-komponen ini:

1. **Extract/Ingest:** Mengambil data mentah dari sumber pihak ketiga (API, database) ke _data warehouse_ atau _data lake_.
2. **Transformations:** Membersihkan data, membuat laporan, dan memindahkan hasilnya ke aplikasi atau warehouse.
3. **Orchestrate:** "Dirigen" yang mengatur kapan skrip berjalan, bagaimana urutannya, dan bagaimana antar layanan berkomunikasi.
4. **Data Quality & Governance:** Memastikan data akurat dan konsisten sebelum sampai ke tangan pengguna (user/stakeholder).

**Keunggulan Bruin:** Ia menyatukan keempatnya. Jadi, saya tidak perlu menjadi ahli DevOps, _infrastructure engineer_, atau _data architect_ sekaligus hanya untuk membangun satu pipeline data.

---

## **5.1.3 — Apa yang Akan Dipelajari di Sini?**

Di modul ini, fokus kita adalah memahami cara kerja Bruin melalui poin-poin berikut:

- **Project Structure:** Bagaimana anatomi proyek di dalam Bruin.
- **Pipelines & Assets:** Memahami apa itu pipeline dan apa itu aset data.
- **Materialization Strategies:** Strategi bagaimana data disimpan/dibangun di Bruin.
- **Lineage & Dependencies:** Bagaimana membangun hubungan antar aset agar data mengalir dengan benar.
- **Metadata:** Cara mengelola informasi tentang data secara otomatis maupun manual.
- **Parameterizing Pipelines:** Menggunakan variabel kustom agar pipeline kita fleksibel.

---

## 📚 Apa yang Saya Pelajari

- **Efisiensi Tooling:** Saya belajar bahwa mengelola banyak _tools_ terpisah itu melelahkan dan rawan error pada integrasinya. Platform seperti Bruin memangkas hambatan teknis tersebut.
- **Fokus pada Logika:** Dengan platform yang terintegrasi, saya bisa lebih fokus pada logika transformasi dan kualitas data, daripada pusing memikirkan cara menyambungkan alat Ingesti ke alat Transformasi.
- **Penyederhanaan Peran:** Ternyata untuk membangun pipeline yang canggih, kita tidak selalu harus menguasai infrastruktur yang sangat rumit jika menggunakan platform yang tepat.
- **Pentingnya Orkestrasi:** Saya semakin paham bahwa transformasi sehebat apa pun tidak akan berguna jika tidak diatur (orchestrate) dengan jadwal dan dependensi yang benar.

---

## 📌 Summary

Data Platform adalah pusat komando bagi seorang Data Engineer. Bruin memberikan kemudahan dengan menyatukan ingesti, transformasi, dan orkestrasi dalam satu tarikan napas. Ini sangat membantu pemula seperti saya untuk bisa membangun pipeline data _end-to-end_ tanpa harus tersesat dalam kerumitan konfigurasi banyak alat.

> **📝 Note:** _Bruin bukan sekadar alat baru, tapi cara baru untuk bekerja lebih efisien. Ingat: semakin sedikit alat yang perlu kita sambungkan secara manual, semakin kecil kemungkinan sistem kita akan 'patah' di tengah jalan._

---

# 5.2 — Getting Started with Bruin

> **Topik:** Instalasi, Struktur Proyek, Jenis Aset, dan CLI Commands.

Di bagian ini, saya belajar bahwa Bruin sangat memanjakan developer. Mulai dari integrasi AI (MCP) hingga kemudahan instalasi, semuanya didesain agar kita bisa langsung fokus membangun pipeline tanpa pusing urusan _boilerplate_.

---

## **5.2.1 — Instalasi & Persiapan Tooling**

Bruin tidak hanya berupa CLI, tapi juga ekosistem di dalam IDE (VS Code/Cursor).

- **Bruin CLI:** Instalasi super cepat lewat terminal.
- **VS Code Extension:** Menambahkan panel "Render" yang sangat berguna untuk menjalankan dan melihat hasil aset secara instan.
- **Bruin MCP (Model Context Protocol):** Ini fitur masa depan! Kita bisa menghubungkan AI agent di IDE untuk membantu membuat pipeline secara otomatis.

---

## **5.2.2 — Inisialisasi Proyek: `bruin init**`

Hanya dengan satu perintah, Bruin menyiapkan segalanya:

```bash
bruin init default my-first-pipeline

```

Perintah ini otomatis membuat struktur folder, menginisialisasi **Git** (wajib di Bruin), dan menyiapkan file konfigurasi dasar.

---

## **5.2.3 — Anatomi Proyek Bruin**

Ada tiga file/folder utama yang harus dipahami:

1. **`.bruin.yml` (Pusat Rahasia):**

- Isinya: Koneksi database dan _secrets_.
- **Penting:** File ini otomatis masuk `.gitignore`. **Jangan pernah** push file ini ke GitHub karena berisi kredensial sensitif.

2. **`pipeline.yml` (Pusat Kendali):**

- Isinya: Nama pipeline, jadwal (_schedule_), dan koneksi default.

3. **`assets/` (Tempat Kerja):**

- Di sinilah kita menaruh file Python, SQL, atau YAML ingestor.

---

## **5.2.4 — Mengenal Jenis-Jenis Asset**

Bruin mendukung berbagai cara untuk mengolah data:

- **Python Asset:** Untuk pemrosesan data yang fleksibel menggunakan skrip Python.
- **YAML Ingestor Asset:** Fitur paling keren! Kita cukup menulis YAML untuk memindahkan data dari _Source_ (misal: Postgres) ke _Destination_ (misal: BigQuery). Bruin akan membuatkan tabelnya secara otomatis jika belum ada.
- **SQL Asset:** Untuk transformasi data di dalam warehouse. Di sini kita juga bisa menentukan **dependensi** (aset mana yang harus jalan duluan).

---

## **5.2.5 — Perintah CLI yang Sering Dipakai**

Sebagai Data Engineer, terminal adalah rumah kedua. Berikut "mantra" yang sering saya gunakan:

| Command                    | Kegunaan                                                     |
| -------------------------- | ------------------------------------------------------------ |
| `bruin validate`           | Cek typo dan error logika sebelum dijalankan.                |
| `bruin run`                | Menjalankan aset atau seluruh pipeline.                      |
| `bruin lineage`            | Melihat visualisasi hubungan antar data (siapa butuh siapa). |
| `bruin run --full-refresh` | Menghapus tabel lama dan membangun ulang dari nol.           |

---

## 📚 Apa yang Saya Pelajari

- **Keamanan Data:** Saya belajar bahwa memisahkan `.bruin.yml` adalah standar industri untuk menjaga agar _password_ database tidak bocor ke publik.
- **Kemudahan Ingesti:** Dengan YAML Ingestor, tugas "memindahkan data" yang biasanya rumit jadi sangat sederhana. Tidak perlu menulis ribuan baris kode Python hanya untuk _copy-paste_ tabel.
- **Lineage Otomatis:** Saya suka bagaimana Bruin bisa tahu urutan jalan aset hanya berdasarkan dependensi yang kita tulis. Ini membuat orkestrasi jadi sangat visual dan mudah dilacak.
- **AI-Ready:** Adanya Bruin MCP menunjukkan bahwa platform ini sangat adaptif dengan perkembangan AI, membantu DE mempercepat pembuatan kode yang repetitif.

---

## 📌 Summary

Memulai Bruin terasa sangat _seamless_. Dari instalasi hingga menjalankan pipeline pertama, alurnya sangat logis. Struktur proyeknya memaksa kita untuk bekerja rapi (memisahkan koneksi, jadwal, dan logika bisnis). Ini adalah awal yang bagus untuk membangun sistem data yang _scalable_.

> **📝 Note:** _Selalu jalankan `bruin validate` sebelum `bruin run`. Lebih baik menemukan error di validasi daripada melihat pipeline mati di tengah jalan saat sedang memproses data besar._

---

# 5.3 — Building an End-to-End Pipeline with NYC Taxi Data

> **Topik:** Arsitektur 3-Layer, Ingesti Python, Transformasi SQL Incremental, dan Orkestrasi.

Di sini, Bruin akan menggunakan **DuckDB** sebagai database lokal. Arsitekturnya mirip dengan apa yang kita pelajari di dbt, tapi dengan sentuhan integrasi ingesti yang lebih "wah".

---

## **5.3.1 — Arsitektur Pipeline 3 Lapis**

Kita membagi kerja menjadi tiga tahap yang rapi:

1. **Ingestion Layer:** Mengambil data mentah (API/CSV) dan menyimpannya apa adanya.
2. **Staging Layer:** Pembersihan, _joining_ dengan tabel lookup, dan deduplikasi.
3. **Reports Layer:** Agregasi akhir (hitung total trip, rata-rata tarif) untuk dikonsumsi bisnis.

---

## **5.3.2 — Layer Ingesti: Python & Seed**

Bruin memberikan dua cara hebat untuk memasukkan data:

- **Python Asset (`trips.py`):** Digunakan untuk menarik file Parquet dari cloud.
- **Keunggulan:** Kita bisa menggunakan variabel `BRUIN_START_DATE` untuk menentukan bulan mana yang mau ditarik.
- **Strategy `append`:** Data baru ditambahkan di bawah data lama tanpa menghapus yang sudah ada.

- **Seed Asset (`payment_lookup`):** Mengubah file CSV lokal menjadi tabel database.
- **Built-in Checks:** Kita bisa langsung pasang `unique` dan `not_null` di dalam YAML-nya.

---

## **5.3.3 — Layer Staging: SQL dengan Strategi Pintar**

Di `staging/trips.sql`, kita melakukan pembersihan data. Ada dua hal teknis yang sangat penting di sini:

1. **Strategy `time_interval`:** Ini adalah cara cerdas untuk menangani data berkala. Bruin akan menghapus data di rentang waktu tertentu, lalu memasukkan data yang baru. Ini mencegah data ganda jika kita menjalankan ulang pipeline untuk tanggal yang sama.
2. **Deduplikasi dengan `QUALIFY`:** Kita menggunakan `ROW_NUMBER()` untuk memastikan setiap perjalanan hanya tercatat satu kali (menghilangkan duplikat dari sumber).

---

## **5.3.4 — Layer Reports: Hasil Akhir**

Tabel `reports.trips_report` adalah tempat kita melakukan "hitung-hitungan" (GROUP BY). Di sini kita mengelompokkan data berdasarkan tanggal, tipe taksi, dan jenis pembayaran.

---

## **5.3.5 — Strategi Materialisasi di Bruin**

Ini adalah ringkasan bagaimana Bruin menyimpan data ke tabel:

| Strategi        | Perilaku                                                          |
| --------------- | ----------------------------------------------------------------- |
| `table`         | Hapus dan buat ulang tabel setiap kali jalan.                     |
| `append`        | Tambahkan data baru saja.                                         |
| `time_interval` | Hapus data di rentang tanggal tertentu, lalu isi ulang.           |
| `merge`         | Update data lama jika ID sama, jika tidak ada maka masukkan baru. |

---

## 📚 Apa yang Saya Pelajari

- **Power of `time_interval`:** Sebagai _Data Engineer_ pemula, menangani data _incremental_ (bertambah seiring waktu) itu menantang. Strategi `time_interval` di Bruin membuat proses "hapus-lalu-isi-lagi" jadi otomatis dan aman.
- **Integrasi Python & SQL:** Saya suka bagaimana Bruin memperlakukan skrip Python dan file SQL sebagai "Aset" yang setara. Mereka bisa saling menunggu (dependensi) tanpa perlu alat tambahan.
- **Pentingnya Deduplikasi:** Data taksi NYC sering punya data ganda. Belajar menggunakan `QUALIFY ROW_NUMBER()` di level staging adalah _best practice_ yang akan sering saya pakai.
- **Variabel Dinamis:** Menggunakan `{{ start_datetime }}` di dalam SQL membuat kode kita tidak kaku (_hardcoded_) dan bisa berjalan untuk tanggal berapa pun.

---

## 📌 Summary

Membangun pipeline dengan Bruin terasa sangat "mengalir". Kita mendefinisikan sumbernya, cara membersihkannya, dan cara melaporkannya. Bruin kemudian menggambar **Lineage Graph** dan menjalankan semuanya sesuai urutan. Jika Ingesti gagal, Staging tidak akan jalan—ini menjamin integritas data kita.

> **📝 Note:** _Deduplikasi di layer Staging adalah investasi terbaik. Jika data di Staging sudah bersih, laporan di layer Report pasti akan akurat._

---

# 5.4 — Using Bruin MCP with AI Agents

> **Topik:** Model Context Protocol (MCP), Integrasi AI, dan Otomasi Pipeline.

Sebagai _Data Engineer_ yang baru belajar, Bruin MCP adalah _cheat code_ yang legal. MCP memungkinkan AI (seperti di Cursor atau VS Code) untuk "berbicara" langsung dengan Bruin. AI jadi tahu struktur tabel kita, bisa menjalankan perintah, bahkan bisa bantu _debugging_ kalau ada yang error.

---

## **5.4.1 — Apa yang Bisa Dilakukan Bruin MCP?**

Bukan sekadar _copy-paste_ dari ChatGPT, Bruin MCP membuat AI agent bisa:

- **Menulis Kode:** Membuat file `.sql` atau `.py` beserta konfigurasinya secara otomatis.
- **Troubleshooting:** Menganalisis log error dan langsung memperbaikinya.
- **Analisis Data:** Kita bisa bertanya "Hari apa yang paling ramai?" dan AI akan menulis serta menjalankan query SQL untuk menjawabnya.
- **Dokumentasi:** Menulis metadata dan deskripsi kolom tanpa perlu kita ketik manual.

---

## **5.4.2 — Instalasi (Menghubungkan AI ke Bruin)**

Agar AI di editor (seperti Cursor) bisa mengakses Bruin, kita perlu menambahkan konfigurasi MCP Server.

**Contoh Konfigurasi untuk Cursor:**
Cukup ke **Settings → Tools & MCP** dan masukkan perintah `bruin mcp`. Setelah statusnya "Enabled", AI sudah punya "kekuatan" Bruin.

---

## **5.4.3 — Membangun Pipeline dengan AI**

Ada dua cara untuk bekerja dengan AI di Bruin:

1. **Metode Sekali Jalan (Template Prompt):**
   Di dalam _template_ Zoomcamp, sudah disediakan "mantra" atau _prompt_ di file `README.md`. Kamu cukup _copy-paste_ ke AI agent, dan dia akan membuatkan seluruh pipeline (Ingestion, Staging, Reports) dalam hitungan detik.
2. **Metode Inkremental (Aset per Aset):**
   Ini cara yang saya lebih suka untuk belajar. Kita minta AI buatkan satu bagian dulu (misal: Ingesti), kita cek, lalu lanjut ke bagian berikutnya. Ini membuat kita tetap punya kendali atas desain pipeline-nya.

---

## **5.4.4 — Bertanya pada Data (Conversational Query)**

Ini bagian yang paling keren. Setelah pipeline berjalan, kamu tidak perlu selalu menulis SQL manual untuk sekadar cek data. Kamu bisa bertanya langsung ke AI:

> _"Coba cek tabel staging, ada berapa hari data yang sudah masuk?"_
> _"Tunjukkan 5 lokasi jemput yang paling sering muncul di data taksi kuning."_

AI akan menerjemahkan bahasa manusia kamu menjadi SQL, menjalankannya lewat Bruin, dan memberikan jawabannya.

---

## 📚 Apa yang Saya Pelajari

- **AI sebagai Rekan Kerja:** Saya belajar bahwa AI bukan untuk menggantikan _Data Engineer_, tapi untuk mempercepat tugas-tugas yang repetitif (seperti ngetik deskripsi kolom atau buat konfigurasi YAML).
- **Kekuatan Konteks:** MCP sangat kuat karena AI tahu **konteks** proyek kita. Dia tahu hubungan antara `ingestion.trips` dan `staging.trips` karena dia bisa membaca seluruh project.
- **Debugging Lebih Cepat:** Biasanya saya pusing baca log error yang panjang. Dengan MCP, saya tinggal bilang "Tolong benerin error ini," dan AI akan mencari letak salahnya di file mana.
- **Analisis Ad-hoc:** Kemampuan untuk bertanya ke data pakai bahasa sehari-hari sangat membantu saat kita ingin melakukan validasi cepat tanpa harus buka-tutup editor SQL.

---

## 📌 Summary

Bruin MCP mengubah cara kita bekerja. Kita berpindah dari "mengetik kode" menjadi "mengarahkan AI". Dengan integrasi ini, membangun pipeline _end-to-end_ yang dulunya butuh berhari-hari, sekarang bisa diselesaikan jauh lebih cepat dengan kualitas yang tetap terjaga.

> **📝 Note:** _Meskipun AI bisa membuatkan segalanya, kamu tetap harus mengerti logika di baliknya. Gunakan AI untuk mempercepat kerja, tapi pastikan kamu tetap melakukan review pada setiap baris kode yang dia buat._

---

# 5.5 — Deploying to Bruin Cloud

> **Topik:** Managed Infrastructure, GitHub Integration, dan Cloud Monitoring.

Sebagai _Data Engineer_, kamu tidak mungkin menjalankan pipeline secara manual setiap hari dari terminal laptop. **Bruin Cloud** adalah tempat di mana pipeline kamu "hidup" secara mandiri, berjalan sesuai jadwal, dan diawasi secara otomatis.

---

## **5.5.1 — Apa itu Bruin Cloud?**

Bruin Cloud adalah infrastruktur yang dikelola penuh (_fully managed_) untuk menjalankan pipeline kamu. Isinya sama persis dengan apa yang kamu gunakan di CLI, tapi dengan fitur tambahan:

- **Otomasi:** Penjadwalan (_scheduling_) tanpa perlu server tambahan.
- **Monitoring:** Dashboard visual untuk melihat aset mana yang sukses atau gagal.
- **Keamanan:** Penyimpanan kredensial database (secrets) yang aman.
- **AI Terintegrasi:** Fitur analisis data berbasis AI tetap tersedia di versi cloud.

---

## **5.5.2 — Menghubungkan Kode (GitHub Integration)**

Bruin Cloud bekerja dengan prinsip **GitOps**. Artinya, apa yang ada di repositori GitHub kamu adalah apa yang akan dijalankan di Cloud.

- **Direct Connection:** Cara paling mudah. Cukup hubungkan akun GitHub dan pilih repositori pipeline kamu.
- **Sinkronisasi Otomatis:** Setiap kali kamu melakukan `git push` ke branch utama, Bruin Cloud akan langsung mendeteksi perubahan tersebut.

---

## **5.5.3 — Mengelola Koneksi & Secrets**

Ingat file `.bruin.yml` yang tidak kita push ke GitHub? Di Bruin Cloud, kita memasukkan informasi koneksi tersebut (seperti token MotherDuck atau kredensial BigQuery) melalui dashboard **Connections**.

- **Nama Harus Sama:** Pastikan nama koneksi di Cloud sama persis dengan nama koneksi yang kamu tulis di kode lokal agar tidak terjadi error.
- **Validasi Otomatis:** Bruin akan langsung mengetes apakah koneksi tersebut berhasil atau tidak.

---

## **5.5.4 — Menjalankan & Memantau Pipeline**

Setelah repositori dan koneksi terhubung:

1. **Enable Pipeline:** Aktifkan tombol _schedule_. Bruin akan langsung menjalankan satu _run_ untuk interval terakhir (misal: jika bulanan, ia akan memproses data bulan lalu).
2. **Lineage View:** Kamu bisa melihat grafik hubungan antar data secara visual di web.
3. **Quality Check Monitoring:** Jika ada data yang tidak lolos tes (misal: ada ID yang null), Bruin Cloud akan memberi tahu kamu lewat dashboard.

---

## 📚 Apa yang Saya Pelajari

- **Data Engineering Lifecycle:** Saya sekarang paham alur lengkap kerja DE: Mulai dari inisialisasi lokal (`bruin init`), ngoding di IDE, testing di terminal (`bruin run`), push ke GitHub, hingga akhirnya aktif di Cloud.
- **Pemisahan Kredensial:** Saya belajar bahwa memisahkan logika kode (di GitHub) dengan kredensial (di Cloud/Secrets) adalah standar keamanan yang wajib dilakukan.
- **Kekuatan Penjadwalan:** Senang rasanya tahu bahwa data taksi NYC saya akan terupdate otomatis setiap hari tanpa saya harus menyalakan komputer.
- **Skalabilitas:** Bruin Cloud memudahkan kita untuk mengelola puluhan bahkan ratusan pipeline tanpa pusing urusan server (DevOps).

---

## 📌 Summary

Di Module 05 ini telah membawa saya dari pemahaman konsep hingga deployment produksi. Saya mengerti arsitektur modern data stack, mampu membangun pipeline _end-to-end_ dengan ingesti-staging-reports, memanfaatkan AI melalui Bruin MCP untuk mempercepat development, dan akhirnya men-deploy ke Cloud dengan GitHub integration. Bruin mengubah kompleksitas infrastruktur menjadi simplifikasi tooling, memungkinkan saya fokus pada logika bisnis tanpa pusing DevOps. Sekarang kamu saya untuk membangun sistem data yang _scalable_, _reliable_, dan _maintainable_.

> **📝 Note:** _Deployment bukan akhir dari segalanya. Setelah pipeline aktif di Cloud, tugas kamu selanjutnya adalah memantau dashboard secara berkala untuk memastikan tidak ada data yang 'pecah' atau koneksi yang terputus._

---

# 5.6 — Core Concepts: Projects

> **Topik:** Anatomi Root Directory, Manajemen Environment, dan Keamanan Koneksi.

Sebagai _Data Engineer_ yang sedang belajar, saya baru menyadari bahwa mengelola "di mana data diproses" sama pentingnya dengan "bagaimana data diproses". Konsep **Project** di Bruin memastikan kita tidak sengaja merusak data produksi saat sedang bereksperimen.

---

## **5.6.1 — Apa itu Project di Bruin?**

**Project** adalah direktori utama (root) yang membungkus seluruh pipeline data kamu. Ini adalah tempat di mana semua aset, konfigurasi, dan koneksi saling mengenal satu sama lain.

- **Inisialisasi:** Wajib menggunakan `bruin init` agar CLI Bruin bisa mengenali struktur folder dan menavigasi file dengan benar.

---

## **5.6.2 — File `.bruin.yml`: Sang Penjaga Gerbang**

File ini adalah jantung dari sebuah project, tapi ia sangat pemalu—ia tidak boleh keluar dari komputer lokalmu (selalu ada di `.gitignore`).

### **Manajemen Environments**

Di dalam file ini, kita bisa membagi "dunia" kerja kita menjadi beberapa bagian:

1. **Default/Dev:** Tempat kita bermain dengan database lokal seperti DuckDB.
2. **Production:** Koneksi sungguhan ke warehouse besar seperti BigQuery atau Snowflake.

**Keuntungan Memisahkan Environment:**

- **Keamanan:** Kredensial produksi tidak akan pernah bocor ke GitHub.
- **Safety:** Kita bisa mengatur agar secara default Bruin selalu jalan di `dev`, jadi tidak ada insiden "salah hapus tabel produksi" karena lupa ganti setting.

---

## **5.6.3 — Jenis Koneksi & Rahasia (Secrets)**

Bruin mendukung banyak sekali jenis koneksi bawaan (_built-in_):

- **Local/Cloud DB:** DuckDB, MotherDuck, Postgres, MySQL.
- **Enterprise Warehouse:** BigQuery, Redshift, Snowflake.
- **Custom:** Untuk menyimpan API Key atau rahasia kustom lainnya yang dibutuhkan skrip Python.

---

## **5.6.4 — Quick Commands Cheat Sheet**

Berikut adalah perintah cepat untuk mengelola project kamu:

- `bruin init zoomcamp my-pipeline`: Membuat project baru dari template.
- `bruin validate .`: Mengecek apakah struktur project dan koneksi kamu sudah valid.

---

## 📚 Apa yang Saya Pelajari

- **Root Directory adalah Jangkar:** Saya paham sekarang bahwa menjalankan perintah `bruin` harus dilakukan di dalam folder project agar ia bisa menemukan file `.bruin.yml`.
- **Pentingnya `.gitignore`:** Saya belajar bahwa keamanan data dimulai dari hal sederhana seperti memastikan file kredensial tidak ikut ter-push ke repositori publik.
- **Fleksibilitas Tim:** Dengan sistem environment, setiap orang di tim bisa punya file `.bruin.yml` yang berbeda (koneksi masing-masing) tapi tetap mengerjakan kode pipeline yang sama.
- **Pencegahan Error Manusia:** Pengaturan `default_environment: dev` adalah fitur favorit saya. Ini memberikan rasa tenang karena saya tahu eksperimen saya tidak akan mengganggu data kantor yang sudah jadi.

---

## 📌 Summary

Sebuah **Project** di Bruin bukan sekadar kumpulan folder, melainkan sebuah ekosistem yang mengatur keamanan dan lingkungan kerja seorang _Data Engineer_. Dengan pondasi project yang kuat, kita bisa dengan mudah berpindah dari tahap _development_ di laptop ke tahap _production_ di cloud tanpa mengubah logika kode transformasi kita.

> **📝 Note:** _Setiap kali membuat project baru, hal pertama yang harus kita cek adalah apakah `.bruin.yml` sudah benar-benar masuk ke dalam `.gitignore`. Keamanan adalah prioritas utama!_

---

# 5.7 — Core Concepts: Pipelines

> **Topik:** Pengelompokan Aset, Penjadwalan Tunggal, dan Isolasi Koneksi.

Sebagai _Data Engineer_, saya belajar bahwa tidak semua data harus diperbarui di waktu yang sama. Ada data yang butuh update setiap jam, ada yang cukup sebulan sekali. Di sinilah peran **Pipeline** untuk merapikan itu semua.

---

## **5.7.1 — Apa itu Pipeline?**

**Pipeline** adalah cara kita mengelompokkan berbagai aset data berdasarkan **jadwal eksekusi** yang sama.

- **Satu Jadwal, Satu Pipeline:** Ini adalah aturan emasnya. Jika kamu punya aset yang harus jalan harian (`daily`) dan aset lain yang bulanan (`monthly`), mereka harus berada di pipeline yang berbeda.
- **Organisasi Folder:** Setiap pipeline memiliki folder sendiri yang berisi file `pipeline.yml` dan folder `assets/`.

---

## **5.7.2 — File `pipeline.yml`: Kontrak Kerja Pipeline**

File ini memberi tahu Bruin bagaimana dan kapan pipeline ini harus bekerja.

- **`name`**: Nama unik untuk identifikasi (misal: `nyc_taxi`).
- **`schedule`**: Kapan pipeline ini bangun dan bekerja (bisa pakai kata kunci seperti `daily` atau kode _cron_ yang lebih spesifik).
- **`start_date`**: Titik awal kapan pipeline ini mulai dianggap aktif.
- **`default_connections`**: Menentukan "kabel" mana yang dicolokkan ke pipeline ini (mengambil dari `.bruin.yml`).

---

## **5.7.3 — Keamanan: Connection Scoping**

Meskipun semua koneksi database ada di level Project, setiap Pipeline harus memilih koneksi mana yang ia gunakan.

- **Isolasi Keamanan:** Tim Finance mungkin punya pipeline sendiri dengan akses ke data sensitif, sementara tim Marketing tidak bisa melihatnya karena koneksi mereka dibatasi di level pipeline.
- **Efisien:** Bruin hanya akan menyiapkan koneksi yang benar-benar dibutuhkan saat pipeline tersebut dijalankan.

---

## **5.7.4 — Quick Reference Commands**

- `bruin validate [path/ke/pipeline.yml]`: Memastikan semua aset di dalam pipeline tersebut sudah "nyambung" dan tidak ada typo.
- `bruin lineage [path/ke/pipeline.yml]`: Melihat peta perjalanan data khusus untuk pipeline tersebut.
- `bruin run [path/ke/pipeline.yml]`: Menjalankan seluruh aset di dalam pipeline tersebut sesuai urutan dependensinya.

---

## 📚 Apa yang Saya Pelajari

- **Filosofi Pengelompokan:** Saya paham sekarang bahwa alasan utama membagi pipeline bukan cuma soal jenis datanya, tapi soal **kapan** data itu harus diproses. Ini membuat manajemen _resource_ jadi lebih hemat.
- **Modularitas:** Dengan membagi-bagi menjadi beberapa pipeline, proyek besar jadi terasa lebih kecil dan mudah dikelola (_manageable_).
- **Fleksibilitas Variabel:** Saya melihat ada opsi `variables` di `pipeline.yml`. Ini sangat berguna untuk membuat pipeline yang dinamis (misal: menjalankan untuk tipe taksi tertentu saja).
- **Visibilitas Lineage:** Melihat lineage per pipeline membantu saya fokus pada alur data yang sedang saya kerjakan tanpa terganggu oleh aset dari pipeline lain.

---

## 📌 Summary

**Pipeline** di Bruin adalah unit orkestrasi. Ia menyatukan aset-aset yang memiliki irama kerja yang sama ke dalam satu wadah yang aman dan terisolasi. Memahami cara mengatur `pipeline.yml` dengan benar adalah kunci agar data kamu selalu segar (_fresh_) dan biaya komputasi kamu tetap terkontrol.

> **📝 Note:** _Jangan menumpuk semua aset dalam satu pipeline raksasa hanya karena 'malas' buat folder baru. Pisahkan berdasarkan kebutuhan bisnis dan jadwal agar proses debugging jauh lebih mudah jika terjadi kegagalan._

---

# 5.8 — Core Concepts: Assets

> **Topik:** Definisi Aset, Jenis-Jenis Kode, Strategi Materialisasi, dan Lineage.

Sebagai _Data Engineer_, saya belajar bahwa **Asset** adalah unit terkecil yang menghasilkan nilai. Hampir selalu, tugas akhir sebuah aset adalah membuat atau memperbarui sebuah tabel di database kita.

---

## **5.8.1 — Apa itu Asset?**

Sebuah Aset terdiri dari dua bagian penting dalam satu file:

1. **Definisi (Konfigurasi):** Berisi metadata seperti nama, tipe aset, koneksi yang dipakai, hingga jadwal. Biasanya ditulis dalam blok komentar `@bruin`.
2. **Isi (Konten):** Kode aslinya, baik itu SQL untuk transformasi, Python untuk ingesti, atau CSV untuk data referensi.

---

## **5.8.2 — Jenis-Jenis Asset di Bruin**

| Tipe          | Kegunaan Utama                                                                           |
| ------------- | ---------------------------------------------------------------------------------------- |
| **Python**    | **Ingesti.** Sangat fleksibel untuk narik data dari API atau proses ML.                  |
| **SQL**       | **Transformasi.** Standar untuk cleaning dan agregasi data di warehouse.                 |
| **YAML/Seed** | **Lookup.** Mengubah file CSV lokal menjadi tabel database (misal: daftar kode wilayah). |
| **R**         | **Analisis.** Jika tim kamu butuh perhitungan statistik yang spesifik.                   |

---

## **5.8.3 — Strategi Materialisasi: Bagaimana Data Disimpan?**

Ini menentukan bagaimana Bruin memperlakukan tabel di database setiap kali aset dijalankan:

- **`table`**: Hapus tabel lama, buat baru (cocok untuk data kecil/staging).
- **`view`**: Tidak menyimpan data fisik, hanya menyimpan logika query-nya.
- **`insert`**: Tambahkan data baru terus-menerus (cocok untuk log/history).
- **`incremental`**: Strategi paling cerdas—hanya update data yang berubah atau tambah yang belum ada berdasarkan kunci tertentu.

---

## **5.8.4 — Lineage & Dependensi Otomatis**

Ini adalah fitur favorit saya di Bruin. Bruin cukup pintar untuk membaca kode kita:

- Jika di file SQL kamu menulis `SELECT * FROM raw.trips`, Bruin otomatis tahu bahwa aset SQL tersebut **bergantung** pada aset `raw.trips`.
- **Visualisasi:** Kita bisa melihat "peta" hubungan ini langsung di VS Code, sehingga kita tahu jika ada perubahan di hulu (_upstream_), bagian mana yang akan terdampak di hilir (_downstream_).

---

## **5.8.5 — Perintah Cepat untuk Eksekusi Aset**

Kadang kita hanya ingin menjalankan satu bagian saja, tidak perlu seluruh pipeline:

- `bruin run --asset [nama_aset]`: Jalankan satu aset saja.
- `bruin run --asset [nama_aset] --downstream`: Jalankan aset tersebut dan **semua yang butuh dia** (ke bawah).
- `bruin run --asset [nama_aset] --upstream`: Jalankan aset tersebut dan **semua sumbernya** (ke atas).

---

## 📚 Apa yang Saya Pelajari

- **Satu File, Satu Tugas:** Saya paham bahwa prinsip _Data Engineering_ yang baik adalah memecah tugas besar menjadi aset-aset kecil yang fokus (misal: satu aset buat bersihin tanggal, satu lagi buat hitung total).
- **Python Return DataFrame:** Di Bruin, skrip Python cukup melakukan `return pd.DataFrame()`, dan Bruin yang akan repot-repot memasukkannya ke database. Ini sangat memudahkan!
- **Dinamis dengan Variabel:** Saya belajar cara pakai `{{ start_date }}` di dalam SQL agar aset saya hanya memproses data di rentang waktu yang diinginkan.
- **Lineage sebagai Dokumentasi:** Saya tidak perlu menggambar diagram manual. Dengan menulis kode yang benar, diagram hubungan datanya sudah digambarkan otomatis oleh Bruin.

---

## 📌 Summary

**Asset** adalah tulang punggung dari pipeline data kita. Dengan memahami berbagai tipe aset dan cara mereka "berbicara" satu sama lain lewat dependensi, kita bisa membangun sistem data yang sangat rapi dan mudah diperbaiki jika ada kesalahan.

> **📝 Note:** _Gunakanlah penamaan aset yang konsisten (misal: `staging.nama_tabel`). Ini akan sangat membantu saat proyekmu sudah memiliki ratusan aset, agar tidak bingung mencari di mana sebuah data berasal._

---

# 5.9 — Core Concepts: Variables

> **Topik:** Built-in Variables, Custom Parameters, dan Injeksi Jinja vs Python.

Sebagai _Data Engineer_, variabel adalah kunci agar pipeline kita tidak kaku. Bayangkan jika kamu punya data 10 tahun, kamu tidak mau menulis 120 skrip untuk setiap bulan. Dengan variabel, kamu cukup tulis **satu skrip** yang bisa berjalan untuk bulan apa pun secara dinamis.

---

## **5.9.1 — Jenis-Jenis Variabel**

Ada dua kategori besar variabel di Bruin yang harus kita kuasai:

### **1. Built-in Variables (Otomatis)**

Bruin secara otomatis menyediakan dua variabel sakti di setiap _run_:

- **`start_date`**: Awal dari interval jadwal (misal: tanggal 1 jam 00:00).
- **`end_date`**: Akhir dari interval jadwal (misal: tanggal 31 jam 23:59).

**Cara Menggunakannya:**

- **Di SQL:** Pakai format Jinja `{{ start_date }}`. Sangat berguna untuk filter `WHERE`.
- **Di Python:** Diakses melalui _environment variables_ dengan awalan `BRUIN_VAR_` (misal: `os.environ['BRUIN_VAR_START_DATE']`).

### **2. Custom Variables (Buatan Sendiri)**

Kamu bisa mendefinisikan variabel sendiri di file `pipeline.yml`. Misalnya, untuk menentukan tipe taksi mana yang mau diproses (`yellow`, `green`, dsb).

**Keuntungan Custom Variables:**

- **Runtime Override:** Kamu bisa mengubah nilai variabel lewat terminal saat menjalankan pipeline tanpa mengubah kode:
  `bruin run ./pipeline.yml --var taxi_types=["green"]`

---

## **5.9.2 — Cara Kerja di SQL vs Python**

| Fitur          | SQL Asset                         | Python Asset                       |
| -------------- | --------------------------------- | ---------------------------------- |
| **Format**     | Jinja Templating `{{ ... }}`      | Environment Variables `os.environ` |
| **Pengecekan** | Pakai **Bruin Render** di VS Code | Pakai `print()` atau Debugger      |
| **Tipe Data**  | String (SQL-ready)                | Biasanya JSON (perlu `json.loads`) |

---

## **5.9.3 — Contoh Kasus Penggunaan Nyata**

- **Date-based Partitioning:** Menarik data hanya untuk bulan Januari 2024 agar prosesnya cepat dan murah (tidak _scan_ seluruh tabel).
- **Multi-tenant:** Menjalankan pipeline yang sama untuk ID Customer yang berbeda-beda hanya dengan mengganti variabel.
- **A/B Testing:** Mengetes logika transformasi baru pada sebagian data saja sebelum dilepas ke produksi.

---

## **5.9.4 — Quick Reference Commands**

Berikut "mantra" terminal untuk bermain dengan variabel:

- `bruin run ... --start-date 2024-01-01`: Memaksa pipeline jalan untuk tanggal tertentu.
- `bruin run ... --var key=value`: Mengganti nilai variabel kustom.
- `bruin run ... --full-refresh`: Menghapus semua data lama dan menjalankan ulang dari `start_date` awal proyek.

---

## 📚 Apa yang Saya Pelajari

- **Hindari Hardcoding:** Saya belajar bahwa menulis tanggal manual di dalam SQL adalah "dosa" besar. Gunakan selalu `{{ start_date }}` agar pipeline bisa diotomatisasi.
- **Kekuatan Render:** Panel Bruin Render di VS Code sangat membantu untuk memastikan Jinja kita diterjemahkan menjadi SQL yang benar sebelum kita jalankan di database.
- **Python Environment:** Baru tahu kalau di Python, semua variabel dari Bruin masuk ke `os.environ`. Ini memudahkan integrasi dengan library lain seperti Pandas atau Requests.
- **Fleksibilitas Tanpa Batas:** Dengan `custom variables`, satu pipeline bisa punya ribuan wajah tergantung parameter yang kita masukkan saat _runtime_.

---

## 📌 Summary

Kita sudah belajar:

1. **Project:** Pondasi dan manajemen environment.
2. **Pipelines:** Orkestrasi dan penjadwalan.
3. **Assets:** Pekerja (SQL/Python/Seed) yang mengolah data.
4. **Variables:** Bahan bakar dinamis yang menjalankan semuanya.
5. **Cloud:** Tempat di mana semua itu berjalan secara otomatis di internet.

> **📝 Note:** _Variabel adalah teman terbaikmu saat debugging. Jika ada data yang salah di bulan tertentu, kamu tinggal jalankan `bruin run` dengan `--start-date` bulan tersebut tanpa mengganggu data bulan lainnya._

---

# 5.10 — Core Concepts: Commands

> **Topik:** Eksekusi Pipeline, Validasi, Lineage, dan Manajemen "Run".

Sebagai seseorang yang sedang belajar _Data Engineering_, saya melihat perintah CLI Bruin bukan sekadar instruksi ketik, tapi alat untuk mengontrol siklus hidup data kita secara presisi.

---

## **5.10.1 — Perintah Utama: `bruin run**`

Ini adalah perintah yang paling sering digunakan. Ia membuat sebuah **Run**—satu instansi eksekusi pipeline pada waktu tertentu.

### **Cakupan Eksekusi (Run Scope)**

Kita bisa mengatur seberapa banyak aset yang mau dijalankan:

- **Seluruh Pipeline:** Jalankan semua dari awal sampai akhir.
- **Single Asset:** `--asset staging.trips_summary` (Hanya jalankan satu tabel ini).
- **With Upstream:** Jalankan aset X dan **semua sumbernya** (ke atas).
- **With Downstream:** Jalankan aset X dan **semua yang butuh dia** (ke bawah).

### **Flag Penting yang Harus Diingat**

- `--full-refresh`: "Tombol Reset". Menghapus tabel dan membangun ulang dari nol (sangat berguna jika logika berubah total).
- `--start-date` & `--end-date`: Menentukan jendela waktu data yang mau diproses.
- `--var KEY=VALUE`: Mengubah variabel secara instan tanpa menyentuh file YAML.

---

## **5.10.2 — Perintah Pendukung: Validate, Lineage, & Query**

Sebelum dan sesudah menjalankan `run`, kita butuh alat bantu ini:

1. **`bruin validate` (The Safety Net):**

- **Wajib** dijalankan sebelum `run`.
- Mengecek apakah ada dependensi yang berputar (_circular_), koneksi yang mati, atau referensi file yang hilang.

2. **`bruin lineage` (The Map):**

- Visualisasi hubungan antar aset. Membantu kita paham "siapa butuh data dari siapa".

3. **`bruin query` (The Inspector):**

- Menjalankan query SQL cepat langsung ke database tanpa harus pindah ke aplikasi database lain. Sangat efisien untuk cek hasil akhir.

---

## **5.10.3 — Apa itu "Run"?**

Sebuah **Run** adalah satu momen eksekusi. Setiap run itu unik karena:

- Punya log eksekusi sendiri (untuk _troubleshooting_).
- Punya nilai variabel sendiri.
- Bisa menjalankan seluruh aset atau hanya sebagian kecil.

---

## **5.10.4 — Alur Kerja Lengkap Bruin (The Big Picture)**

Berikut adalah rangkuman bagaimana semua materi di Module 05 bersatu:

1. **Project:** Fondasi & Koneksi (`.bruin.yml`).
2. **Pipeline:** Jadwal & Pengelompokan (`pipeline.yml`).
3. **Assets:** Kode Nyata (Python untuk Ingest, SQL untuk Transform).
4. **Commands:** Eksekusi (`run`), Cek (`validate`), Inspeksi (`query`).

---

## 📚 Apa yang Saya Pelajari

- **Budaya "Validate First":** Saya belajar bahwa menghemat 5 detik dengan melewati `validate` bisa menyebabkan pusing 5 jam karena error di tengah jalan.
- **Fleksibilitas Downstream:** Fitur `--downstream` sangat membantu. Jika saya hanya mengubah tabel staging, saya cukup jalankan tabel itu dan semua laporan di bawahnya akan otomatis terupdate.
- **Efisiensi Query:** Dengan `bruin query`, saya bisa bekerja sepenuhnya di terminal/IDE tanpa perlu membuka banyak _tools_ lain.
- **Manajemen Environment:** Saya bisa mengetes pipeline saya di `dev` dulu dengan flag `--environment default` sebelum benar-benar yakin mengirimnya ke `production`.

---

## 📌 Summary

> Sebagai pemula, biasakanlah untuk selalu menulis perintah secara lengkap (termasuk start-date) agar kamu punya kontrol penuh atas apa yang database kamu kerjakan. Jangan biarkan pipeline berjalan 'buta' tanpa validasi.\_

---
