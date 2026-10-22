#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validasi_ntb.py
Script otomatis untuk validasi dan pengecekan anomali Nilai Tambah Bruto (NTB)
serta Rasio Keuntungan Lapangan Usaha (KBLI) pada survei FASIH SM / PANTAU BPS.
Menghasilkan kolom 'Status' dengan nilai '#0' (Sesuai) dan '#1' (Perlu Perbaikan).
Catatan: Tidak menggunakan kolom 'Rasio NTB' bawaan sistem karena beranomali/salah.
"""

import sys
import os
import re
import argparse
import csv
from typing import Dict, List, Tuple, Optional, Any

# Pastikan output konsol Windows mendukung UTF-8
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Definisi Rentang NTB / Persentase Keuntungan Berdasarkan Kategori KBLI
KBLI_RANGES: Dict[str, Dict[str, Any]] = {
    'A': {'nama': 'Pertanian, Kehutanan, dan Perikanan', 'min': 19.0, 'max': 30.0},
    'B': {'nama': 'Pertambangan dan Penggalian', 'min': 28.0, 'max': 81.0},
    'C': {'nama': 'Industri Pengolahan', 'min': 33.0, 'max': 67.0},
    'D': {'nama': 'Pengadaan Listrik, Gas, Uap/Air Panas, Udara Dingin', 'min': 13.0, 'max': 68.0},
    'E': {'nama': 'Pengelolaan Air, Limbah, Penanganan Limbah, Remediasi', 'min': 29.0, 'max': 47.0},
    'F': {'nama': 'Konstruksi', 'min': 34.0, 'max': 44.0},
    'G': {'nama': 'Perdagangan Besar dan Eceran; Reparasi Mobil & Motor', 'min': 7.0, 'max': 60.0},
    'H': {'nama': 'Transportasi dan Pergudangan', 'min': 7.0, 'max': 60.0},
    'I': {'nama': 'Penyediaan Akomodasi dan Makan Minum', 'min': 7.0, 'max': 60.0},
    'J': {'nama': 'Informasi dan Komunikasi (Penerbitan, Penyiaran, Konten)', 'min': 7.0, 'max': 60.0},
    'K': {'nama': 'Aktivitas Telekomunikasi, Komputer, Jasa Informasi', 'min': 7.0, 'max': 60.0},
    'L': {'nama': 'Aktivitas Keuangan dan Asuransi', 'min': 15.0, 'max': 100.0},
    'M': {'nama': 'Aktivitas Real Estat', 'min': 15.0, 'max': 100.0},
    'N': {'nama': 'Aktivitas Profesional, Ilmiah, dan Teknis', 'min': 15.0, 'max': 100.0},
    'O': {'nama': 'Aktivitas Administratif dan Penunjang Usaha', 'min': 15.0, 'max': 100.0},
    'P': {'nama': 'Administrasi Pemerintahan, Pertahanan, Jamsostek', 'min': 15.0, 'max': 100.0},
    'Q': {'nama': 'Aktivitas Pendidikan', 'min': 15.0, 'max': 100.0},
    'R': {'nama': 'Aktivitas Kesehatan Manusia dan Sosial', 'min': 15.0, 'max': 100.0},
    'S': {'nama': 'Kesenian, Olahraga, dan Rekreasi', 'min': 15.0, 'max': 100.0},
    'T': {'nama': 'Aktivitas Jasa Lainnya', 'min': 15.0, 'max': 100.0},
    'U': {'nama': 'Aktivitas Rumah Tangga Pemberi Kerja', 'min': 15.0, 'max': 100.0},
    'V': {'nama': 'Aktivitas Badan Internasional', 'min': 15.0, 'max': 100.0}
}

def guess_kbli(nama_usaha: str) -> str:
    """Memperkirakan kategori KBLI berdasarkan nama dan jenis usaha."""
    n = (nama_usaha or '').lower()
    
    # 1. Makanan & Minuman (Kategori I)
    if any(k in n for k in ['warung makan', 'rumah makan', 'resto', 'kafe', 'cafe', 'warkop', 
                           'coto', 'bakso', 'batagor', 'nasi kuning', 'nasi campur', 
                           'nasi goreng', 'catering', 'jual kue', 'kue tradisional', 
                           'pisang ijo', 'gorengan', 'kedai kopi', 'penjual makanan']):
        return 'I'
        
    # 2. Transportasi (Kategori H)
    if any(k in n for k in ['bentor', 'becak', 'pete pete', 'pete-pete', 'ojek', 'sopir', 
                           'driver', 'angkot', 'ekspedisi', 'kurir', 'pengangkutan', 
                           'perahu', 'kapal', 'angkutan sewa', 'sewa bentor']):
        return 'H'
        
    # 3. Telekomunikasi / Komputer (Kategori K)
    if any(k in n for k in ['konter pulsa', 'jual pulsa', 'kartu data', 'kuota', 'warnet', 
                           'wifi koin', 'servis komputer', 'pulsa inna']):
        return 'K'
        
    # 4. Percetakan & Penerbitan (Kategori J)
    if any(k in n for k in ['genprint', 'citra print', 'percetakan', 'sablon', 'fotokopi', 
                           'studio foto', 'video shooting', 'shooting']):
        return 'J'
        
    # 5. Konstruksi (Kategori F)
    if any(k in n for k in ['konstruksi', 'kontruksi', 'tukang batu', 'tukang kayu', 
                           'borongan bangunan', 'pemborong', 'mandor']):
        return 'F'
        
    # 6. Air / Limbah (Kategori E)
    if any(k in n for k in ['pamsimas', 'air bersih', 'kelola limbah', 'pengolahan sampah', 'sedot tinja']):
        return 'E'
        
    # 7. Kesehatan (Kategori R)
    if any(k in n for k in ['klinik', 'kesehatan', 'bidan', 'dokter', 'praktik dokter', 
                           'puskesmas', 'apotek', 'terapi', 'fisioterapi', 'khitan']):
        return 'R'
        
    # 8. Jasa Perorangan (Kategori T)
    if any(k in n for k in ['barbershop', 'salon', 'pangkas rambut', 'laundry', 'jahit', 
                           'penjahit', 'servis hp', 'servis tv', 'reparasi elektronik', 
                           'reparasi jam']):
        return 'T'
        
    # 9. Industri Pengolahan (Kategori C)
    if any(k in n for k in ['parut kelapa', 'mebel', 'penggilingan padi', 'pabrik gabah', 
                           'pabrik gaba', 'konveksi', 'kerajinan', 'pandai besi', 
                           'produksi kerupuk', 'bengkel las', 'pembuatan']):
        return 'C'
        
    # 10. Kesenian & Rekreasi (Kategori S)
    if any(k in n for k in ['ngamen', 'senam', 'sanggar seni', 'sewa lapangan', 'futsal', 'rental ps', 'playstation']):
        return 'S'
        
    # 11. Keuangan (Kategori L)
    if any(k in n for k in ['koperasi', 'simpan pinjam', 'brilink', 'bri link', 'agen bank', 'laku pandai']):
        return 'L'
        
    # 12. Perdagangan (Kategori G): Kios, Toko, Warung, Jual Ikan/Sayur/Gas, dsb.
    if any(k in n for k in ['jual', 'jualan', 'kios', 'toko', 'warung', 'kelontong', 
                           'campuran', 'eceran', 'pedagang', 'agen', 'distributor', 
                           'olshop', 'online shop', 'bengkel motor', 'bengkel mobil', 
                           'sembako', 'lpg', 'gas 3kg', 'beras']):
        return 'G'
        
    # 13. Pertanian, Peternakan, Perikanan Primer (Kategori A)
    if any(k in n for k in ['utp', 'ternak', 'itik', 'sapi', 'kambing', 'tambak', 
                           'empang', 'nelayan', 'petani', 'tani', 'padi', 'jagung', 
                           'rumput laut', 'kebun', 'sawah', 'budidaya', 'kolam ikan', 
                           'bebek', 'petelur', 'peternak']):
        return 'A'
        
    return 'G'

def parse_html_table(html_content: str) -> List[Dict[str, str]]:
    """Parse tabel HTML yang diekspor dari PANTAU / FASIH."""
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html_content, re.DOTALL | re.IGNORECASE)
    if not rows:
        return []
    
    header_cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', rows[0], re.DOTALL | re.IGNORECASE)
    headers = [re.sub(r'<[^>]+>', '', c).strip().replace('\n', ' ') for c in header_cells]
    
    std_headers = []
    for h in headers:
        clean_h = ' '.join(h.split())
        clean_h = clean_h.replace('&amp;', '&')
        std_headers.append(clean_h)
    
    records = []
    for r in rows[1:]:
        cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, re.DOTALL | re.IGNORECASE)
        cleaned_cells = [re.sub(r'<[^>]+>', '', c).strip().replace('\n', ' ') for c in cells]
        cleaned_cells = [' '.join(c.split()).replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>') for c in cleaned_cells]
        
        link_match = re.search(r'href=[\'"]([^\'"]+)[\'"]', r, re.IGNORECASE)
        link = link_match.group(1) if link_match else ''
        
        row_dict = dict(zip(std_headers, cleaned_cells))
        if link and ('Link Edit FASIH' not in row_dict or not row_dict['Link Edit FASIH']):
            row_dict['Link Edit FASIH'] = link
        records.append(row_dict)
        
    return records

def load_data(file_path: str) -> List[Dict[str, str]]:
    """Membaca file data (.xls frameset, .xls html, .csv, atau .xlsx)."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File tidak ditemukan: {file_path}")
    
    base_name = os.path.splitext(file_path)[0]
    sheet_htm = os.path.join(base_name + '_files', 'sheet001.htm')
    if os.path.exists(sheet_htm):
        with open(sheet_htm, 'r', encoding='utf-8', errors='ignore') as f:
            return parse_html_table(f.read())
            
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    if '<table' in content.lower() or '<tr' in content.lower():
        return parse_html_table(content)
        
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        return list(reader)

def validate_row(d: Dict[str, str]) -> Dict[str, Any]:
    """
    Melakukan validasi NTB dan rasio keuntungan untuk satu baris usaha.
    PENTING: Tidak menggunakan kolom 'Rasio NTB' dari sistem karena salah.
    Rasio dihitung ulang: NTB Hitung / Total Pendapatan * 100%.
    """
    nama_usaha = d.get('Nama Usaha', '') or d.get('nama_usaha', '')
    
    def parse_num(val):
        if not val or val == '&nbsp;':
            return 0.0
        v = re.sub(r'[^\d.-]', '', str(val))
        try:
            return float(v)
        except ValueError:
            return 0.0

    pengeluaran = parse_num(d.get('Total Pengeluaran', d.get('total_pengeluaran', 0)))
    pend_bj = parse_num(d.get('Pendapatan Barang & Jasa', d.get('pendapatan_barang_jasa', 0)))
    pend_lain = parse_num(d.get('Pendapatan Lainnya', d.get('pendapatan_lainnya', 0)))
    total_aset = parse_num(d.get('Total Aset', d.get('total_aset', 0)))
    rasio_sistem_raw = parse_num(d.get('Rasio NTB', d.get('rasio_ntb', 0)))
    rasio_sistem_pct = rasio_sistem_raw * 100.0 if 0 < rasio_sistem_raw <= 1.5 else rasio_sistem_raw

    # HITUNG SENDIRI NTB DAN RASIO NTB (JANGAN PAKAI KOLOM SISTEM)
    total_pendapatan = pend_bj + pend_lain
    ntb_hitung = total_pendapatan - pengeluaran
    
    if total_pendapatan > 0:
        rasio_hitung = (ntb_hitung / total_pendapatan) * 100.0
    else:
        rasio_hitung = 0.0
        
    # KBLI & Batas Acuan
    kat = guess_kbli(nama_usaha)
    info_kat = KBLI_RANGES.get(kat, KBLI_RANGES['G'])
    min_pct = info_kat['min']
    max_pct = info_kat['max']
    range_str = f"{min_pct:.0f}% - {max_pct:.0f}%"
    
    diagnosa = []
    rekomendasi = []
    
    # PENENTUAN STATUS: #0 vs #1
    if total_pendapatan <= 0:
        status = '#1'
        diagnosa.append("Pendapatan tercatat Rp 0 / kosong")
        rekomendasi.append("Lakukan konfirmasi omzet sebenarnya kepada responden")
    elif ntb_hitung < 0:
        status = '#1'
        diagnosa.append(f"Rasio Negatif ({rasio_hitung:.2f}%), Pengeluaran melebihi Pendapatan")
        rekomendasi.append("Periksa biaya operasional/produksi yang terlalu tinggi atau omzet belum tercatat lengkap")
    elif rasio_hitung < min_pct:
        status = '#1'
        diagnosa.append(f"Rasio terlalu rendah ({rasio_hitung:.2f}% < batas bawah {min_pct}%)")
        rekomendasi.append(f"Periksa kelengkapan pendapatan atau kemungkinan pengeluaran dilaporkan berlebihan")
    elif rasio_hitung > max_pct:
        status = '#1'
        diagnosa.append(f"Rasio terlalu tinggi ({rasio_hitung:.2f}% > batas atas {max_pct}%)")
        rekomendasi.append("Kemungkinan biaya kulakan dagangan (26c) atau bahan baku (26b) belum dimasukkan")
    else:
        status = '#0'
        diagnosa.append(f"Sesuai batas wajar ({rasio_hitung:.2f}% dalam rentang {range_str})")
        rekomendasi.append("Data wajar, siap dikonfirmasi Status #0 di sistem")
        
    # Catatan mismatch jika rasio kolom sistem berbeda jauh dari rasio riil
    if abs(rasio_sistem_pct - rasio_hitung) > 5.0 and total_pendapatan > 0:
        diagnosa.append(f"Mismatch kolom sistem: Sistem mencatat {rasio_sistem_pct:.1f}% (salah), hitungan riil {rasio_hitung:.2f}%")
        
    if pend_lain > 0:
        rekomendasi.append(f"Pendapatan lainnya Rp {pend_lain:,.0f} dapat disatukan ke pendapatan utama (27a)")
        
    if status == '#1' and total_pendapatan > 0:
        target_mid_pct = (min_pct + min(max_pct, 60.0)) / 2.0
        target_pengeluaran = total_pendapatan * (1.0 - target_mid_pct / 100.0)
        rekomendasi.append(f"Pengeluaran wajar estimasi: Rp {target_pengeluaran:,.0f} (agar rasio ~{target_mid_pct:.1f}%)")

    return {
        'no': d.get('No', ''),
        'assignment_id': d.get('Assignment ID', ''),
        'kecamatan': d.get('Kecamatan', ''),
        'desa': d.get('Desa/Kel', ''),
        'nama_usaha': nama_usaha,
        'kategori_kbli': kat,
        'nama_kbli': info_kat['nama'],
        'range_acuan': range_str,
        'pengeluaran': pengeluaran,
        'pendapatan_bj': pend_bj,
        'pendapatan_lain': pend_lain,
        'total_pendapatan': total_pendapatan,
        'total_aset': total_aset,
        'ntb_hitung': ntb_hitung,
        'rasio_hitung_pct': round(rasio_hitung, 2),
        'rasio_sistem_pct': round(rasio_sistem_pct, 2),
        'Status': status,  # NAMA KOLOM SPESIFIK: 'Status' dengan nilai '#0' atau '#1'
        'diagnosa': " | ".join(diagnosa),
        'saran_perbaikan': " | ".join(rekomendasi),
        'link_fasih': d.get('Link Edit FASIH', '')
    }

def run_validation(file_path: str, filter_status: Optional[str] = None, 
                   filter_kec: Optional[str] = None, search_term: Optional[str] = None,
                   export_path: Optional[str] = None):
    """Menjalankan validasi menyeluruh pada dataset."""
    records = load_data(file_path)
    if not records:
        print(f"[!] Tidak ada data ditemukan pada file: {file_path}")
        return
        
    results = [validate_row(r) for r in records]
    
    if filter_status:
        st = '#0' if filter_status in ['0', '#0'] else '#1'
        results = [r for r in results if r['Status'] == st]
        
    if filter_kec:
        results = [r for r in results if filter_kec.lower() in r['kecamatan'].lower()]
        
    if search_term:
        s = search_term.lower()
        results = [r for r in results if s in r['nama_usaha'].lower() or s in r['assignment_id'].lower()]

    total = len(results)
    tag_0_count = sum(1 for r in results if r['Status'] == '#0')
    tag_1_count = sum(1 for r in results if r['Status'] == '#1')
    
    print("=" * 80)
    print(f"📊 HASIL VALIDASI NTB & RASIO KEUNTUNGAN LAPANGAN USAHA")
    print(f"Sumber Data : {os.path.basename(file_path)}")
    print(f"Total Sampel: {total} Usaha")
    print(f"Status '#0' (Sesuai Rentang Wajar)   : {tag_0_count} usaha ({tag_0_count/total*100:.2f}%)" if total else "0")
    print(f"Status '#1' (Tidak Sesuai / Anomali) : {tag_1_count} usaha ({tag_1_count/total*100:.2f}%)" if total else "0")
    print("=" * 80)

    cat_summary: Dict[str, Dict[str, int]] = {}
    for r in results:
        k = r['kategori_kbli']
        if k not in cat_summary:
            cat_summary[k] = {'#0': 0, '#1': 0}
        cat_summary[k][r['Status']] += 1

    print("\n📌 Ringkasan per Kategori KBLI:")
    print(f"{'Kat':<5} | {'Deskripsi':<35} | {'Range':<11} | {'Total':<6} | {'Status #0':<11} | {'Status #1':<11}")
    print("-" * 90)
    for k in sorted(cat_summary.keys()):
        info = KBLI_RANGES.get(k, KBLI_RANGES['G'])
        t = cat_summary[k]['#0'] + cat_summary[k]['#1']
        valid_c = cat_summary[k]['#0']
        invalid_c = cat_summary[k]['#1']
        print(f"{k:<5} | {info['nama'][:35]:<35} | {info['min']:.0f}-{info['max']:.0f}%{'':<4} | {t:<6} | {valid_c:<11} | {invalid_c:<11}")

    # Simpan ke CSV
    out_csv = export_path or 'hasil_validasi_ntb.csv'
    fieldnames = [
        'no', 'assignment_id', 'kecamatan', 'desa', 'nama_usaha', 'kategori_kbli',
        'nama_kbli', 'range_acuan', 'pengeluaran', 'pendapatan_bj', 'pendapatan_lain',
        'total_pendapatan', 'total_aset', 'ntb_hitung', 'rasio_hitung_pct',
        'rasio_sistem_pct', 'Status', 'diagnosa', 'saran_perbaikan', 'link_fasih'
    ]
    with open(out_csv, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(results)
    print(f"\n💾 Data CSV lengkap tersimpan di : {os.path.abspath(out_csv)}")

def main():
    parser = argparse.ArgumentParser(description="Pengecekan dan Validasi Anomali NTB / Rasio Keuntungan KBLI")
    parser.add_argument('--file', '-f', type=str, default=None, help="Path ke file data (.xls/.xlsx/.csv)")
    parser.add_argument('--status', '-s', type=str, choices=['0', '1', '#0', '#1'], default=None, help="Filter Status (#0 atau #1)")
    parser.add_argument('--kecamatan', '-k', type=str, default=None, help="Filter nama kecamatan")
    parser.add_argument('--search', '-q', type=str, default=None, help="Cari nama usaha atau assignment ID")
    parser.add_argument('--export', '-o', type=str, default=None, help="Path output file CSV")

    args = parser.parse_args()
    
    target_file = args.file
    if not target_file:
        candidates = [
            'anomali-ntb-flag-3-2026-10-20.xls',
            'anomali-ntb-flag-3-2026-10-20_files/sheet001.htm'
        ]
        for c in candidates:
            if os.path.exists(c):
                target_file = c
                break
        if not target_file:
            for f in os.listdir('.'):
                if ('anomali' in f.lower() or 'ntb' in f.lower()) and f.endswith(('.xls', '.xlsx', '.csv', '.htm', '.html')):
                    target_file = f
                    break
                    
    if not target_file:
        print("[!] File data anomali NTB tidak ditemukan di direktori saat ini.")
        print("    Gunakan opsi: python validasi_ntb.py --file <path_file>")
        sys.exit(1)

    run_validation(
        file_path=target_file,
        filter_status=args.status,
        filter_kec=args.kecamatan,
        search_term=args.search,
        export_path=args.export
    )

if __name__ == '__main__':
    main()
