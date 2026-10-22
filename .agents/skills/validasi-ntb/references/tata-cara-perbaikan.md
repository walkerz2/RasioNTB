# Tata Cara Edit dan Perbaikan Anomali NTB

Panduan langkah demi langkah untuk memeriksa, memperbaiki, dan menandai hasil verifikasi anomali data survei pada aplikasi PANTAU dan FASIH SM.

---

## 1. Kredensial & Akses Sistem

### A. Aplikasi PANTAU
- **Tujuan**: Memantau daftar anomali, mengunduh data mikro, dan memeriksa ringkasan assignment.
- **Password PANTAU**: `statistikpangkep`
- **Menu Akses**:
  1. Pilih **Anomali Flag 3 NTB**
  2. Klik tab / tombol **Data Mikro**
  3. Unduh data atau klik **Buka Assignment** untuk meninjau kuesioner individual.

### B. Aplikasi FASIH SM (Survei Mandiri / Eksternal)
- **Metode Login**: Pilih opsi **Login SSO Eksternal**
- **Akun Percobaan / Sobat**:
  - **Email**: `uji.coba7309@dummy.sobat.id`
  - **Password**: `Pangk3p7309`
- **Opsi Alternatif**: Dapat menggunakan akun Google / Gmail pribadi masing-masing yang telah terdaftar sebagai petugas/supervisor.

---

## 2. Alur Pemeriksaan Lapangan Usaha (Assignment)

Ketika membuka lembar kuesioner/assignment per usaha di FASIH SM:

1. **Periksa Kesesuaian Kode KBLI**:
   - Cocokkan nama usaha (`Nama Usaha`) dan uraian kegiatan usaha dengan kode KBLI 5 digit yang diisikan.
   - Jika usaha dagang kelontong namun dikodekan sebagai industri atau pertanian, ubah kode KBLI ke kelompok `47...` (Kategori G).

2. **Periksa Nilai Rasio NTB**:
   - Bandingkan rasio NTB hasil perhitungan dengan rentang acuan:
     - **Kategori A** (Pertanian/Perikanan): `19% – 30%`
     - **Kategori B** (Pertambangan): `28% – 81%`
     - **Kategori C** (Industri Pengolahan): `33% – 67%`
     - **Kategori D** (Listrik/Gas): `13% – 68%`
     - **Kategori E** (Pengelolaan Air/Limbah): `29% – 47%`
     - **Kategori F** (Konstruksi): `34% – 44%`
     - **Kategori G, H, I, J, K** (Perdagangan, Transport, Mamin, Komunikasi): `7% – 60%`
     - **Kategori L, M, N, O, P, Q, R, S, T, U, V** (Jasa, Kesehatan, dsb.): `Positif, umumnya min 15%`

3. **Pemberian Tanda Konfirmasi**:
   - **Tanda `#0`**: Jika setelah diteliti, rasio NTB dan data usaha memang **sudah berada pada range yang sesuai** dan kondisi lapangan mencerminkan data tersebut.
   - **Tanda `#1`**: Jika data tidak sesuai (misal rasio ekstrem > 90% atau < 0%), lakukan perbaikan data angka terlebih dahulu, lalu beri tanda `#1`.

---

## 3. Strategi dan Cara Memperbaiki Data (Flag `#1`)

Terapkan 3 kaidah utama perbaikan berikut:

### Kaidah 1: Evaluasi Pendapatan vs Pengeluaran
- Periksa konsistensi antara pengeluaran bulanan dan omzet:
  - Pada usaha dagang (Kategori G), margin keuntungan bersih (NTB) berkisar **7% – 60%** (umumnya rata-rata 15% – 30%). Jika rasio NTB mencapai 90%+, hampir pasti **biaya kulakan/pembelian barang dagangan (26c)** belum tercatat.
  - Tambahkan biaya pembelian barang dagangan atau biaya operasional yang tertinggal sehingga pengeluaran mencerminkan realitas usaha.
  - Sebaliknya, jika rasio NTB negatif atau sangat kecil (< 5%), periksa apakah responden melebih-lebihkan pengeluaran atau belum melaporkan pendapatan kotor seutuhnya.

### Kaidah 2: Penanganan Pendapatan Lainnya
- Perhatikan kolom **Pendapatan Lainnya**:
  - Sering kali pendapatan utama usaha dicatat di kolom pendapatan lainnya atau sebaliknya.
  - Jika kolom "Pendapatan Lainnya" terisi signifikan sementara pendapatan utama kosong atau terlalu kecil, pindahkan/gabungkan nilai tersebut ke **Pendapatan Utama (Blok 27a)**.

### Kaidah 3: Penyandingan dengan Total Aset Usaha
- Bandingkan nilai omzet (pendapatan) bulanan/tahunan dengan **Total Aset Usaha**:
  - Usaha dengan aset berupa gerobak senilai Rp 5.000.000 tidak wajar memiliki omzet ratusan juta per bulan tanpa pengeluaran yang memadai.
  - Sebaliknya, usaha dengan aset peralatan/kendaraan bernilai puluhan juta wajar menghasilkan omzet yang proporsional dengan skala modalnya.
  - Gunakan total aset sebagai parameter kewajaran skala usaha (*sanity check*).

---

## 4. Format Catatan Pemeriksaan di Sistem

Saat menyelesaikan assignment di FASIH SM / PANTAU:
- **Jika Valid**:
  ```text
  #0 - Rasio NTB sudah sesuai dengan range Kategori [Kategori] ([Persentase]%). KBLI sesuai.
  ```
- **Jika Diperbaiki**:
  ```text
  #1 - Perbaikan data pendapatan/pengeluaran: [Uraian singkat penyesuaian, misal: penambahan biaya pembelian dagangan 26c sehingga rasio menjadi 22.5% sesuai Kategori G].
  ```
