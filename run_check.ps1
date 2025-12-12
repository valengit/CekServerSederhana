# --- run_check.ps1 ---
# Skrip ini menjalankan Python Health Check Script.
# PowerShell lebih stabil dalam menangani path dan seringkali lebih disukai untuk automasi IT.

# Tentukan lokasi yang absolut (WAJIB diganti jika lokasi berubah!)
$PythonExecutable = "C:\Users\Valentino\AppData\Local\Python\pythoncore-3.14-64\python.exe"
$ScriptPath = "D:\Program\server_check.py"

# --- DEBUGGING dan EKSEKUSI ---
Write-Host "Memulai Skrip Health Check..."

# Panggil interpreter Python untuk menjalankan skrip.
# Jika ada error, PowerShell akan menangkapnya dan menampilkannya di konsol.
& $PythonExecutable $ScriptPath

# Write-Host digunakan untuk menampilkan output di konsol.
Write-Host "Eksekusi Selesai."
# Perintah Read-Host akan berfungsi seperti 'pause', menunggu input sebelum jendela ditutup.
Read-Host "Tekan Enter untuk menutup jendela..."

# Skrip ini akan keluar setelah Enter ditekan.