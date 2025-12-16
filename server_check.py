import psutil # Digunakan untuk mengambil informasi sistem (CPU, Disk, Memori)
import requests # Digunakan untuk melakukan permintaan HTTP (mengecek status Web Service)
import smtplib # Digunakan untuk mengirim email menggunakan protokol SMTP
from email.mime.text import MIMEText # Digunakan untuk membuat badan email dalam format HTML
from datetime import datetime # Digunakan untuk mendapatkan waktu dan tanggal saat ini (untuk laporan)

# --- PENGATURAN KONFIGURASI ---
# Variabel-variabel di bawah ini dapat diubah sesuai kebutuhan IT Anda.

# Ambang batas ruang disk (persentase) yang dianggap kritis.
# Jika ruang disk kurang dari nilai ini, akan muncul peringatan KRITIS.
DISK_THRESHOLD_PERCENT = 20  # Peringatan jika sisa kurang dari 20%

# Daftar URL aplikasi web yang perlu dicek statusnya (simulasi)
# Skrip akan mengecek apakah URL ini mengembalikan status code 200 (OK)
WEB_SERVICES = {
    "Aplikasi Utama Perusahaan": "https://www.google.com",  # Ganti dengan URL aplikasi nyata
    "Portal Internal Server": "https://github.com/",
}

# --- KONFIGURASI EMAIL (Ganti dengan data Anda!) ---
# Pengaturan ini diperlukan agar skrip dapat terhubung dan login ke server email.
SMTP_SERVER = "smtp.gmail.com"  # Contoh menggunakan Gmail
SMTP_PORT = 587 # Port standar untuk koneksi SMTP TLS (StartTLS)
SENDER_EMAIL = "email pengirim"  # Ganti dengan email pengirim
SENDER_PASSWORD = "password google app email pengirim"  # Ganti dengan password aplikasi (BUKAN password email biasa!)
RECEIVER_EMAIL = "email yang ingin dituju"  # Ganti dengan email penerima laporan

# ----------------------------------------------------

def check_disk_usage(threshold):
    """
    Fungsi: Memeriksa penggunaan disk di semua partisi (Drive C:, D:, dll.)
    
    Apa yang dikerjakan:
    1. Mengambil data semua partisi yang terpasang (mount point).
    2. Menghitung persentase ruang kosong yang tersisa.
    3. Jika persentase ruang kosong di bawah 'threshold', status diubah menjadi KRITIS.
    """
    disk_data = []
    is_critical = False
    
    # psutil.disk_partitions(all=False) hanya mengambil partisi fisik utama
    for partition in psutil.disk_partitions(all=False):
        usage = psutil.disk_usage(partition.mountpoint)
        
        # Hitung sisa ruang disk dalam persen (100 - yang sudah terpakai)
        free_percent = 100 - usage.percent
        
        status = "OK"
        if free_percent < threshold:
            status = f"KRITIS (Sisa {free_percent:.2f}%)"
            is_critical = True # Menandai bahwa setidaknya ada 1 partisi yang kritis

        # Menyimpan data setiap drive ke dalam list
        disk_data.append({
            "drive": partition.device,
            "total": f"{usage.total / (1024**3):.2f} GB", # Konversi byte ke GB
            "free": f"{usage.free / (1024**3):.2f} GB",
            "percent_used": f"{usage.percent:.2f}%",
            "status": status
        })
    return disk_data, is_critical # Mengembalikan data drive dan status kritis keseluruhan

def check_web_services(services):
    """
    Fungsi: Memeriksa status layanan web (konektivitas HTTP).
    
    Apa yang dikerjakan:
    1. Mengiterasi setiap URL dalam dictionary WEB_SERVICES.
    2. Mengirim permintaan GET ke URL tersebut.
    3. Jika status code = 200 (berhasil), status dicatat sebagai OK.
    4. Jika kode lain (404, 500) atau terjadi error koneksi, status dicatat sebagai GAGAL/ERROR.
    """
    web_status = []
    is_critical = False
    for name, url in services.items():
        try:
            # Timeout 5 detik agar skrip tidak menunggu terlalu lama jika server tidak merespons
            response = requests.get(url, timeout=5)
            status_code = response.status_code
            status = "OK"
            if status_code != 200:
                status = f"GAGAL (Kode: {status_code})"
                is_critical = True # Menandai adanya kegagalan
        except requests.exceptions.RequestException as e:
            # Menangkap semua error yang berhubungan dengan koneksi (timeout, DNS error, dll.)
            status = f"ERROR KONEKSI ({e.__class__.__name__})"
            is_critical = True
        
        web_status.append({
            "service": name,
            "url": url,
            "status": status
        })
    return web_status, is_critical

def generate_report(disk_data, web_status, overall_status):
    """
    Fungsi: Membuat laporan dalam format HTML agar mudah dibaca di email.
    
    Apa yang dikerjakan:
    1. Membuat struktur dasar HTML (styling inline di tag <style>).
    2. Menyisipkan data disk dan status web ke dalam tabel-tabel HTML.
    3. Menggunakan class CSS ('status-critical' atau 'status-ok') untuk memberikan highlight warna Merah atau Hijau.
    4. Menyertakan status keseluruhan di bagian atas laporan.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # (Kode HTML yang berisi layout, styling, dan penyisipan data)
    # [Immersive content redacted for brevity.]
    html_content = f"""
    <html>
    <head>
        <title>Laporan Health Check Server Harian</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; background-color: #f4f4f9; color: #333; padding: 20px; }}
            .container {{ max-width: 800px; margin: auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
            h2 {{ color: #0056b3; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
            .status-ok {{ color: green; font-weight: bold; }}
            .status-critical {{ color: red; font-weight: bold; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
            th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
            th {{ background-color: #f0f0f0; }}
            .alert-box {{ padding: 15px; margin-top: 20px; border-radius: 5px; }}
            .alert-box.ok {{ background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }}
            .alert-box.critical {{ background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Laporan Kesehatan Server Harian</h1>
            <p><strong>Tanggal Laporan:</strong> {now}</p>
            
            <div class="alert-box {'critical' if overall_status else 'ok'}">
                Status Keseluruhan: <span class="{'status-critical' if overall_status else 'status-ok'}">{'PERLU TINDAKAN' if overall_status else 'SEMUA BAIK (OK)'}</span>
            </div>

            <h2>1. Pengecekan Ruang Disk (Threshold < {DISK_THRESHOLD_PERCENT}%)</h2>
            <table>
                <tr>
                    <th>Drive</th>
                    <th>Total Kapasitas</th>
                    <th>Sisa Ruang Kosong</th>
                    <th>Digunakan</th>
                    <th>Status</th>
                </tr>
                {"".join([f'<tr><td>{d["drive"]}</td><td>{d["total"]}</td><td>{d["free"]}</td><td>{d["percent_used"]}</td><td class="status-{'critical' if d["status"].startswith("KRITIS") else 'ok'}">{d["status"]}</td></tr>' for d in disk_data])}
            </table>

            <h2>2. Pengecekan Layanan Web</h2>
            <table>
                <tr>
                    <th>Layanan</th>
                    <th>URL</th>
                    <th>Status</th>
                </tr>
                {"".join([f'<tr><td>{w["service"]}</td><td>{w["url"]}</td><td class="status-{'critical' if w["status"].startswith("GAGAL") or w["status"].startswith("ERROR") else 'ok'}">{w["status"]}</td></tr>' for w in web_status])}
            </table>
        </div>
    </body>
    </html>
    """
    return html_content

def send_email(subject, body):
    """
    Fungsi: Mengirim email laporan ke penerima yang telah dikonfigurasi.
    
    Apa yang dikerjakan:
    1. Membuat objek MIMEText dengan isi HTML.
    2. Menggunakan smtplib untuk terhubung ke server SMTP.
    3. Melakukan login dengan kredensial SENDER_EMAIL dan SENDER_PASSWORD.
    4. Mengirimkan email.
    5. Menyertakan blok 'try...except' untuk menangani error koneksi atau login.
    """
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        # Menghubungkan ke server SMTP
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Mengamankan koneksi dengan TLS (wajib untuk sebagian besar server)
        
        # Login dengan kredensial
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # Mengirim email
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print(f"Sukses: Laporan terkirim ke {RECEIVER_EMAIL}")
    except Exception as e:
        print(f"ERROR: Gagal mengirim email. Pastikan Anda menggunakan 'App Password' jika menggunakan Gmail. Detail Error: {e}")

def main():
    """
    Fungsi Utama: Mengkoordinasikan semua fungsi pengecekan dan pengiriman laporan.
    """
    # 1. Jalankan Pengecekan
    disk_data, disk_critical = check_disk_usage(DISK_THRESHOLD_PERCENT)
    web_status, web_critical = check_web_services(WEB_SERVICES)

    # 2. Tentukan Status Keseluruhan
    # Jika salah satu dari disk atau web kritis, maka status keseluruhan adalah kritis.
    overall_critical = disk_critical or web_critical
    
    # Tentukan Subjek Email berdasarkan status keseluruhan
    if overall_critical:
        subject = f"[KRITIS] Laporan Health Check Server - {datetime.now().strftime('%Y-%m-%d')}"
    else:
        subject = f"[OK] Laporan Health Check Server - {datetime.now().strftime('%Y-%m-%d')}"
        
    # 3. Buat Laporan HTML
    report_body = generate_report(disk_data, web_status, overall_critical)

    # 4. Kirim Email
    send_email(subject, report_body)

if __name__ == "__main__":
    # Ini memastikan bahwa fungsi main() hanya dijalankan saat skrip dieksekusi langsung

    main()
