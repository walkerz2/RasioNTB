# Aturan Validasi NTB dan Kategori KBLI

Dokumen ini berisi standar acuan pengecekan dan validasi Nilai Tambah Bruto (NTB) / Rasio Keuntungan usaha per Lapangan Usaha (KBLI) berdasarkan pedoman verifikasi data survei (FASIH SM / PANTAU BPS).

---

## 1. Tabel Range Keuntungan / NTB Berdasarkan Kategori KBLI

| Kategori | Deskripsi Lapangan Usaha | Range NTB / Keuntungan (%) | Keterangan Batas |
| :---: | :--- | :---: | :--- |
| **A** | Pertanian, Kehutanan, dan Perikanan | **19% – 30%** | Batas wajar usaha tani, tambak, nelayan, peternakan |
| **B** | Pertambangan dan Penggalian | **28% – 81%** | Galian C, tambang batu, pasir |
| **C** | Industri Pengolahan | **33% – 67%** | Pabrik, pengolahan makanan, mebel, konveksi, parut kelapa |
| **D** | Pengadaan Listrik, Gas, Uap/Air Panas, dan Udara Dingin | **13% – 68%** | Distribusi gas, pembangkit listrik mandiri |
| **E** | Pengelolaan Air, Air Limbah, Penanganan Limbah, Remediasi | **29% – 47%** | PAMSIMAS, depot air minum, daur ulang |
| **F** | Konstruksi | **34% – 44%** | Tukang/mandor bangunan, instalasi listrik bangunan |
| **G** | Perdagangan Besar dan Eceran; Reparasi Mobil & Motor | **7% – 60%** | Toko kelontong, kios campuran, eceran gas LPG, agen, bengkel |
| **H** | Transportasi dan Pergudangan | **7% – 60%** | Ojek, sopir angkot, perahu/kapal penyeberangan, kurir |
| **I** | Aktivitas Penyediaan Akomodasi dan Makan Minum | **7% – 60%** | Warung makan, kedai kopi, kafe, catering, penginapan |
| **J** | Informasi dan Komunikasi (Penerbitan, Penyiaran, Konten) | **7% – 60%** | Percetakan, studio foto, pembuatan konten, media |
| **K** | Aktivitas Telekomunikasi, Komputer, Jasa Informasi | **7% – 60%** | Konter pulsa/data, servis komputer, wifi koin |
| **L** | Aktivitas Keuangan dan Asuransi | **Positif, min 15%** | Koperasi simpan pinjam, agen bank/laku pandai |
| **M** | Aktivitas Real Estat | **Positif, min 15%** | Sewa ruko, kontrakan, agen properti |
| **N** | Aktivitas Profesional, Ilmiah, dan Teknis | **Positif, min 15%** | Jasa akuntansi, hukum, arsitektur, konsultasi |
| **O** | Aktivitas Administratif dan Penunjang Usaha | **Positif, min 15%** | Rental kendaraan, fotokopi, agen perjalanan |
| **P** | Administrasi Pemerintahan, Pertahanan, Jaminan Sosial | **Positif, min 15%** | Jasa terkait administrasi publik |
| **Q** | Aktivitas Pendidikan | **Positif, min 15%** | Bimbel, kursus keterampilan, PAUD/TK swasta |
| **R** | Aktivitas Kesehatan Manusia dan Aktivitas Sosial | **Positif, min 15%** | Praktik dokter, bidan mandiri, klinik kesehatan |
| **S** | Kesenian, Olahraga, dan Rekreasi | **Positif, min 15%** | Sanggar seni, sewa lapangan futsal, game/PS |
| **T** | Aktivitas Jasa Lainnya | **Positif, min 15%** | Pangkas rambut, salon kecantikan, laundry, penjahit |
| **U** | Aktivitas Rumah Tangga sebagai Pemberi Kerja | **Positif, min 15%** | Pekerja rumah tangga untuk keperluan sendiri |
| **V** | Aktivitas Badan Internasional dan Ekstra Internasional | **Positif, min 15%** | Lembaga perwakilan internasional |

---

## 2. Rumus Perhitungan NTB dan Persentase Keuntungan

### Komponen Data:
- **Pendapatan Utama (Blok 27a)**: Pendapatan Barang & Jasa usaha.
- **Pendapatan Lainnya**: Pendapatan sampingan dari usaha.
- **Total Pengeluaran (Blok 26)**:
  - `26b`: Biaya Produksi (bahan baku, bibit, pakan, dsb.)
  - `26c`: Biaya Pembelian Barang Dagangan (khusus perdagangan)
  - `26d`: Biaya Operasional (listrik, BBM, transportasi, sewa, tenaga kerja)

### Formula:
$$\text{Total Pendapatan} = \text{Pendapatan (27a)} + \text{Pendapatan Lainnya}$$

$$\text{Total Pengeluaran} = \text{Biaya Produksi (26b)} + \text{Biaya Pembelian (26c)} + \text{Biaya Operasional (26d)}$$

$$\text{NTB (Nilai Tambah Bruto)} = \text{Total Pendapatan} - \text{Total Pengeluaran}$$

$$\text{Persentase Keuntungan (Rasio NTB)} = \left( \frac{\text{NTB}}{\text{Total Pendapatan}} \right) \times 100\%$$

---

## 3. Logika Penentuan Tag (#0 vs #1)

- **Beri Tanda `#0` (Sesuai / Valid)**:
  - Nilai Rasio NTB berada di dalam rentang wajar kategori KBLI yang bersangkutan.
  - Kegiatan usaha sudah sesuai dengan kode KBLI.
  - Nilai pendapatan dan pengeluaran logis.

- **Beri Tanda `#1` (Perlu Perbaikan / Anomali)**:
  - Nilai Rasio NTB berada di **luar rentang** wajar (terlalu tinggi atau terlalu rendah).
  - Nilai Rasio NTB bernilai **negatif** (Pengeluaran > Pendapatan).
  - Kode KBLI salah kamar / tidak sesuai dengan kegiatan usaha sebenarnya.
  - Terjadi anomali teknis (misal sistem mencatat rasio = 1.0 atau 100% padahal data pengeluaran ada).

---

## 4. Panduan Pemetaan KBLI Berdasarkan Kata Kunci Usaha

| Kategori | Kata Kunci Nama Usaha (Inference Helper) |
| :---: | :--- |
| **A** | ternak, itik, ayam, sapi, kambing, tambak, empang, nelayan, ikan, tani, padi, jagung, rumput laut, utp perikanan, utp peternakan |
| **B** | tambang, galian, pasir, batu gunung, kapur, marmer |
| **C** | parut kelapa, mebel, penggilingan padi, gaba, pabrik, roti, konveksi, pandai besi, kerajinan, pembuatan |
| **D** | plts komersil, genset sewa, gas distribusi |
| **E** | pamsimas, air bersih, kelola limbah, pengolahan sampah |
| **F** | konstruksi, tukang batu, tukang kayu, borongan bangunan, instalasi listrik rumah |
| **G** | jual, jualan, kios, toko, warung kelontong, barang campuran, agen gas, lpg 3kg, beras, online shop, olshop, distributor |
| **H** | ojek, sopir, angkutan, perahu jolloro, kapal kayu, ekspedisi, kurir, antar barang |
| **I** | warung makan, nasi kuning, coto, bakso, batagor, warkop, kafe, catering, penginapan, kos-kosan |
| **J** | percetakan, sablon, fotokopi, media online, penerbitan, studio foto, video shooting |
| **K** | konter pulsa, jual kuota, warnet, wifi koin, jasa instalasi komputer |
| **L** | koperasi, simpan pinjam, agen bri link, agen bni 46, agen bank |
| **M** | sewa ruko, sewa kontrakan, kontrakan rumah |
| **N** | konsultan, biro jasa, notaris, arsitek |
| **O** | rental mobil, cuci motor/mobil, outsourcing, jasa fotokopi perkantoran |
| **Q** | les privat, bimbingan belajar, bimbel, kursus, paud |
| **R** | klinik kesehatan, bidan, dokter praktik, pengobatan, apotek |
| **S** | ngamen, senam, sanggar, sewa lapangan futsal, rental ps / playstation |
| **T** | salon, barbershop, pangkas rambut, laundry, tukang jahit, permak, servis elektronik/hp |
