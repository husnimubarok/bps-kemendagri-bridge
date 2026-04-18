# Bridging Kode Wilayah BPS ↔ Kemendagri

Script Python sederhana untuk mengunduh tabel relasi **Kode Wilayah Kerja Statistik (BPS)** dengan **Kode Wilayah Administrasi (Kemendagri)** untuk **seluruh Indonesia** dalam sekali jalan — tanpa harus klik tombol *download* per kecamatan di [sig.bps.go.id/bridging-kode](https://sig.bps.go.id/bridging-kode/).

Sumber data: REST endpoint internal SIG BPS (`https://sig.bps.go.id/rest-bridging/getwilayah`) yang dipakai oleh halaman resmi BPS itu sendiri.

## Output

File `bridging_bps_kemendagri.csv` berisi ±83.000 baris sampai level desa/kelurahan, dengan kolom:

| Kolom | Keterangan |
|---|---|
| `kode_bps` | Kode Wilkerstat BPS (2/4/7/10 digit) |
| `nama_bps` | Nama wilayah versi BPS |
| `kode_dagri` | Kode Kemendagri (format titik, mis. `33.29.11.2001`) |
| `nama_dagri` | Nama wilayah versi Kemendagri |

## Cara pakai

```bash
pip install requests pandas tqdm
python bridging_scraper.py
```

Proses memakan waktu sekitar 3–5 menit dengan 16 worker paralel. Hasil langsung tersimpan sebagai `bridging_bps_kemendagri.csv` di folder yang sama.

## Cara kerja

Script menelusuri hierarki wilayah secara berurutan:

1. **Provinsi** — 1 request awal ke `getwilayah` tanpa parameter
2. **Kabupaten/Kota** — ±38 request, satu per provinsi
3. **Kecamatan** — ±514 request, satu per kab/kota
4. **Desa/Kelurahan** — ±7.160 request, satu per kecamatan (ini bagian paling lama)

Setiap level di-fetch paralel pakai `ThreadPoolExecutor`.

## Catatan

- **Jangan agresif** dengan jumlah worker. Default 16 sudah cukup nyaman; jangan naikkan ke ratusan — ini server pemerintah.
- Data yang diambil adalah periode Wilkerstat default yang ditampilkan halaman BPS. Untuk periode lain (misalnya Semester 1 vs Semester 2 tahun tertentu), cek parameter tambahan di DevTools → Network saat mengubah dropdown periode, lalu tambahkan ke `fetch()`.
- Untuk bridging **BPS ↔ Kode Pos**, ganti base URL ke `https://sig.bps.go.id/rest-bridging-kodepos/getwilayah` dengan pola parameter yang sama.
- Endpoint ini bukan API publik resmi — sewaktu-waktu bisa berubah tanpa pemberitahuan. Jika script gagal, buka DevTools di [halaman sumber](https://sig.bps.go.id/bridging-kode/) dan bandingkan format respons terbaru.

## Disclaimer

Data milik [Badan Pusat Statistik](https://bps.go.id) dan [Kemendagri](https://kemendagri.go.id). Repositori ini hanya menyediakan tool pengambilan data untuk keperluan analisis. Gunakan dengan bijak dan cantumkan sumber jika dipublikasikan ulang.

## Lisensi

MIT
