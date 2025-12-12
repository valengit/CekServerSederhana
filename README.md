# ⚙️ Skrip Health Check Server Harian (Daily Server Health Check Script)

Proyek otomatisasi ini dibuat menggunakan Python untuk memantau status kritis sebuah sistem (ruang disk dan ketersediaan layanan web) secara periodik dan mengirimkan laporan ringkasan via email HTML.

Tujuan utama skrip ini adalah untuk mengadopsi pendekatan **proaktif** dalam pemeliharaan sistem, mengurangi risiko *downtime* yang disebabkan oleh ruang disk penuh atau kegagalan koneksi layanan.

## Fitur Utama

- **Pengecekan Ruang Disk (Disk Usage Check):** Memantau semua partisi lokal. Status `KRITIS` akan dipicu jika ruang kosong di bawah ambang batas (default 20%).
- **Pengecekan Layanan Web (Web Service Monitoring):** Memastikan konektivitas layanan web dengan mengecek status kode HTTP.
- **Laporan HTML Berwarna:** Laporan dikirim dalam format HTML yang mudah dibaca, dengan indikator warna Merah/Hijau untuk status kritis.
- **Otomasi Siap *Deployment*:** Dirancang untuk dijalankan tanpa pengawasan menggunakan PowerShell.

## 🛠️ Teknologi yang Digunakan

* **Bahasa Pemrograman:** Python 3.x
* **Platform Otomasi:** Windows PowerShell
* **Library Python:**
    * `psutil`: Untuk interaksi dengan informasi sistem (penggunaan CPU, Disk, Memori).
    * `requests`: Untuk melakukan permintaan HTTP (pengecekan status web).
    * `smtplib` & `email.mime`: Untuk koneksi dan pengiriman email.

## 🚀 Cara Menjalankan Skrip (Deployment)

### A. Persiapan Lingkungan

1. **Instalasi Python:** Pastikan Python 3.x terinstal.
2. **Instalasi Dependensi:** Jalankan perintah berikut di terminal:
   ```bash
   pip install -r requirements.txt
