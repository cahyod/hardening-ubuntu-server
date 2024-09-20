### **Skrip Otomasi Hardening Ubuntu Server 22.04.4 menggunakan python3**

Skrip Python3 yang dirancang untuk melakukan **hardening** pada **Ubuntu Server 22.04** secara otomatis. Skrip ini mencakup berbagai langkah keamanan penting untuk memperkuat sistem Anda. Sebelum menjalankan skrip ini, pastikan untuk memahami setiap langkah yang diambil dan lakukan pengujian di lingkungan yang aman terlebih dahulu.

### **Fitur Utama Skrip:**

1. **Memeriksa Hak Akses Root:** Skrip ini harus dijalankan dengan hak akses root atau menggunakan `sudo`.
2. **Memperbarui dan Meningkatkan Sistem:** Memastikan semua paket sistem terbaru.
3. **Mengonfigurasi Firewall dengan UFW (Uncomplicated Firewall):** Menetapkan aturan dasar firewall.
4. **Menginstal dan Mengonfigurasi Fail2Ban:** Melindungi dari serangan brute-force.
5. **Mengamankan SSH:** Menonaktifkan login root, mengubah port SSH, dan mengaktifkan autentikasi kunci SSH.
6. **Menghapus Paket yang Tidak Diperlukan:** Mengurangi potensi vektor serangan.
7. **Mengatur Pembaruan Otomatis:** Memastikan sistem selalu menerima pembaruan keamanan terbaru.
8. **Mengaktifkan Audit Logging:** Memantau aktivitas sistem untuk deteksi dini.

### **Peringatan:**

- **Backup Konfigurasi:** Sebelum menjalankan skrip ini, disarankan untuk melakukan backup konfigurasi sistem Anda.
- **Pengujian:** Jalankan skrip ini di lingkungan pengujian terlebih dahulu untuk memastikan tidak ada konflik atau masalah.
- **Kustomisasi:** Sesuaikan parameter seperti port SSH atau aturan firewall sesuai kebutuhan spesifik Anda.

### **Cara Menggunakan Skrip Ini**

1. **Simpan Skrip:**
   Simpan skrip di atas ke dalam file, misalnya `hardening_ubuntu.py`.

2. **Beri Izin Eksekusi:**
   Buka terminal dan beri izin eksekusi pada skrip:
   ```bash
   chmod +x hardening_ubuntu.py
   ```

3. **Jalankan Skrip dengan Hak Akses Root:**
   Karena skrip ini memerlukan hak akses root untuk mengubah pengaturan sistem dan memasang paket, jalankan dengan `sudo`:
   ```bash
   sudo ./hardening_ubuntu.py
   ```

### **Penjelasan Skrip**

1. **Fungsi `run_command`:**
   - Menjalankan perintah shell dan menampilkan outputnya.
   - Jika terjadi kesalahan, skrip akan berhenti dan menampilkan pesan error.

2. **Fungsi `check_root`:**
   - Memastikan skrip dijalankan dengan hak akses root. Jika tidak, skrip akan berhenti.

3. **Fungsi `update_and_upgrade`:**
   - Memperbarui daftar paket dengan `apt-get update`.
   - Meningkatkan paket yang sudah ada dengan `apt-get upgrade`.

4. **Fungsi `install_packages`:**
   - Menginstal paket-paket yang diperlukan seperti `ufw`, `fail2ban`, `auditd`, dan `unattended-upgrades`.

5. **Fungsi `setup_firewall`:**
   - Mengonfigurasi UFW dengan aturan dasar:
     - Menolak semua koneksi masuk secara default.
     - Mengizinkan semua koneksi keluar.
     - Mengizinkan koneksi SSH.
     - Mengaktifkan UFW.

6. **Fungsi `configure_fail2ban`:**
   - Membuat backup konfigurasi `jail.local` jika belum ada.
   - Menulis konfigurasi dasar Fail2Ban untuk melindungi layanan SSH.
   - Merestart dan mengaktifkan layanan Fail2Ban.

7. **Fungsi `secure_ssh`:**
   - Membuat backup konfigurasi SSH jika belum ada.
   - Mengubah konfigurasi SSH untuk:
     - Menonaktifkan login root (`PermitRootLogin no`).
     - Menonaktifkan autentikasi password (`PasswordAuthentication no`).
     - (Opsional) Mengubah port SSH jika diinginkan.
   - Merestart layanan SSH untuk menerapkan perubahan.

8. **Fungsi `disable_unnecessary_services`:**
   - Menonaktifkan dan menghentikan layanan yang tidak diperlukan seperti `telnet`, `ftp`, `nfs-common`, `rpcbind`, dan `samba`.

9. **Fungsi `setup_auto_updates`:**
   - Menginstal `unattended-upgrades` untuk mengatur pembaruan otomatis.
   - Mengaktifkan pembaruan otomatis menggunakan `dpkg-reconfigure`.

10. **Fungsi `enable_audit_logging`:**
    - Menginstal `auditd` dan plugin terkait untuk audit logging.
    - Mengaktifkan dan memulai layanan `auditd`.

11. **Fungsi `main`:**
    - Menjalankan semua fungsi di atas secara berurutan.
    - Menampilkan pesan selesai dan beberapa rekomendasi langkah tambahan.

### **Langkah Tambahan yang Direkomendasikan:**

- **Autentikasi Kunci SSH:**
  - Mengonfigurasi autentikasi kunci SSH untuk meningkatkan keamanan.
  
- **Menggunakan AppArmor atau SELinux:**
  - Memasang dan mengonfigurasi modul keamanan tambahan untuk kontrol akses yang lebih ketat.
  
- **Monitoring dan Alerting:**
  - Menggunakan tools seperti `Nagios`, `Zabbix`, atau `Prometheus` untuk memantau kesehatan dan keamanan sistem.
  
- **Kebijakan Kata Sandi yang Kuat:**
  - Mengatur kebijakan kata sandi yang kompleks dan mengimplementasikan password aging.

- **Pemasangan Tools Keamanan Tambahan:**
  - Tools seperti `Lynis` atau `Bastille` dapat digunakan untuk audit keamanan lebih lanjut.

### **Selesai**
