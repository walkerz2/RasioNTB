---
name: validasi-ntb
description: >-
  Validasi dan perbaikan anomali Nilai Tambah Bruto (NTB) dan rasio keuntungan usaha berdasarkan kategori KBLI (A sampai U) pada survei FASIH SM / PANTAU BPS. Gunakan skill ini saat memeriksa anomali NTB Flag 3, menentukan status konfirmasi #0 (sesuai batas wajar) atau #1 (anomali/perlu perbaikan), menghitung persentase keuntungan, memetakan kode KBLI, serta memberikan rekomendasi perbaikan pendapatan, pengeluaran, dan aset.
---

# Skill Validasi NTB & Rasio Keuntungan Lapangan Usaha

Skill ini memandu AI Agent dalam melakukan pengecekan, diagnosis anomali, penentuan tag status (`#0` vs `#1`), dan pemberian rekomendasi perbaikan data Nilai Tambah Bruto (NTB) pada survei ekonomi BPS (seperti PL-KUMKM, SBR, FASIH SM, dan PANTAU).

---

## 1. Konsep dan Formula Utama

### Formula NTB:
$$\text{Total Pendapatan} = \text{Pendapatan Barang \& Jasa (27a)} + \text{Pendapatan Lainnya}$$

$$\text{Total Pengeluaran} = \text{Biaya Produksi (26b)} + \text{Biaya Pembelian Barang Dagangan (26c)} + \text{Biaya Operasional (26d)}$$

$$\text{NTB (Nilai Tambah Bruto)} = \text{Total Pendapatan} - \text{Total Pengeluaran}$$

$$\text{Persentase Keuntungan (Rasio NTB)} = \left(\frac{\text{NTB}}{\text{Total Pendapatan}}\right) \times 100\%$$

---

## 2. Acuan Range Keuntungan / NTB per Kategori KBLI

| Kategori | Sektor Lapangan Usaha | Rentang Wajar (%) | Keterangan Singkat |
| :---: | :--- | :---: | :--- |
| **A** | Pertanian, Kehutanan, dan Perikanan | **19% – 30%** | Tanaman pangan, perkebunan, ternak, tambak, nelayan |
| **B** | Pertambangan dan Penggalian | **28% – 81%** | Galian C, tambang pasir, batu |
| **C** | Industri Pengolahan | **33% – 67%** | Pabrik gaba, parut kelapa, mebel, konveksi, roti |
| **D** | Listrik, Gas, Uap/Air Panas, Udara Dingin | **13% – 68%** | Distribusi gas, pembangkit mandiri |
| **E** | Pengelolaan Air, Air Limbah, Sampah | **29% – 47%** | PAMSIMAS, air isi ulang, daur ulang |
| **F** | Konstruksi | **34% – 44%** | Tukang/mandor bangunan, borongan |
| **G** | Perdagangan Besar dan Eceran; Reparasi Motor | **7% – 60%** | Kios, toko, eceran sembako/gas, olshop, bengkel |
| **H** | Transportasi dan Pergudangan | **7% – 60%** | Ojek, sopir angkot, perahu/kapal kayu, kurir |
| **I** | Penyediaan Akomodasi dan Makan Minum | **7% – 60%** | Warung makan, warkop, kafe, catering, losmen |
| **J** | Informasi dan Komunikasi (Penerbitan, Konten) | **7% – 60%** | Percetakan, studio foto, media |
| **K** | Telekomunikasi, Komputer, Jasa Informasi | **7% – 60%** | Konter pulsa/kuota, wifi, servis komputer |
| **L – V** | Jasa Keuangan, Real Estat, Pendidikan, Kesehatan, Jasa Lainnya | **Positif, min 15%** | L, M, N, O, P, Q, R, S, T, U, V |

> Dokumen lengkap referensi kategori dan kata kunci: [aturan-kategori-kbli.md](./references/aturan-kategori-kbli.md)

---

## 3. Logika Penentuan Tag (#0 vs #1)

1. **Tag `#0` (Sesuai / Valid)**:
   - Nilai Rasio NTB berada di dalam rentang wajar kategori KBLI.
   - Jenis usaha konsisten dengan klasifikasi KBLI.
   - Tindakan: Beri konfirmasi `#0` pada kolom catatan/pemeriksaan di sistem.

2. **Tag `#1` (Perlu Perbaikan / Anomali)**:
   - Nilai Rasio NTB berada di **luar rentang** (terlalu tinggi atau terlalu rendah).
   - Nilai Rasio NTB **negatif** (Pengeluaran > Pendapatan / usaha rugi tidak wajar).
   - KBLI salah kamar (misal: "Jualan Ikan" dikodekan A padahal seharusnya G).
   - Terjadi anomali sistem (sistem mencatat rasio 100% atau 975% karena bug input/formula).
   - Tindakan: Lakukan koreksi data pendapatan/pengeluaran di FASIH SM, lalu beri tanda `#1`.

---

## 4. Prosedur Perbaikan Data (Jika `#1`)

Ikuti 3 prinsip perbaikan sesuai petunjuk teknis:
1. **Evaluasi Pendapatan vs Pengeluaran**:
   - Jika rasio **terlalu tinggi** (> batas atas): Biasanya pengeluaran belum mencatat biaya kulakan dagangan (26c) atau bahan baku (26b). Sesuaikan pengeluaran ke nilai wajar.
   - Jika rasio **terlalu rendah / negatif** (< batas bawah): Periksa apakah omzet sebulan penuh belum terinput atau pengeluaran dicatat berlebihan.
2. **Periksa Pendapatan Lainnya**:
   - Jika kolom Pendapatan Lainnya terisi sedangkan Pendapatan Utama kosong/kecil, satukan ke Pendapatan Utama (27a).
3. **Sandingkan dengan Total Aset**:
   - Bandingkan omzet usaha dengan Total Aset sebagai parameter kewajaran skala usaha (*sanity check*).

> Panduan login dan alur teknis di portal: [tata-cara-perbaikan.md](./references/tata-cara-perbaikan.md)

---

## 5. Menjalankan Skrip Validasi Otomatis

Gunakan skrip Python pembantu di folder `scripts/` untuk memproses seluruh baris data survei:

```bash
# Jalankan validasi pada file anomali di workspace:
python .agents/skills/validasi-ntb/scripts/validasi_ntb.py

# Filter hanya data yang perlu diperbaiki (#1):
python .agents/skills/validasi-ntb/scripts/validasi_ntb.py --status 1

# Filter hanya data yang sudah sesuai (#0):
python .agents/skills/validasi-ntb/scripts/validasi_ntb.py --status 0

# Filter berdasarkan nama kecamatan:
python .agents/skills/validasi-ntb/scripts/validasi_ntb.py --kecamatan BALOCCI

# Cari berdasarkan nama usaha atau Assignment ID:
python .agents/skills/validasi-ntb/scripts/validasi_ntb.py --search "parut kelapa"

# Ekspor hasil ke file CSV khusus:
python .agents/skills/validasi-ntb/scripts/validasi_ntb.py --export "d:/NTB/laporan_anomali_flag3.csv"
```

Skrip akan menghasilkan:
- Statistik total usaha, jumlah `#0` (valid), dan `#1` (perlu perbaikan).
- Breakdown distribusi kategori KBLI.
- Diagnosa penyebab anomali dan estimasi angka pengeluaran/pendapatan yang wajar.
- File CSV lengkap dengan link edit langsung ke FASIH SM untuk setiap assignment.
