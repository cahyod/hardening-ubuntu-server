#!/usr/bin/env python3

import subprocess
import sys
import os
import shutil

def run_command(command, check=True, sudo=False):
    """
    Jalankan perintah shell dan tampilkan outputnya.
    """
    if sudo:
        command = f"sudo {command}"
    print(f"Menjalankan perintah: {command}")
    try:
        result = subprocess.run(command, shell=True, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error menjalankan perintah: {command}")
        print(e.stderr)
        sys.exit(1)

def check_root():
    """
    Periksa apakah skrip dijalankan sebagai root.
    """
    if os.geteuid() != 0:
        print("Skrip ini harus dijalankan dengan hak akses root. Gunakan sudo.")
        sys.exit(1)

def update_and_upgrade():
    """
    Memperbarui daftar paket dan meningkatkan paket yang sudah ada.
    """
    print("\n--- Memperbarui dan Meningkatkan Sistem ---")
    run_command("apt-get update -y")
    run_command("apt-get upgrade -y")

def install_packages(packages):
    """
    Instalasi paket yang diperlukan.
    """
    print("\n--- Menginstal Paket yang Diperlukan ---")
    pkg_str = ' '.join(packages)
    run_command(f"apt-get install -y {pkg_str}")

def setup_firewall():
    """
    Mengonfigurasi UFW dengan aturan dasar.
    """
    print("\n--- Mengonfigurasi Firewall dengan UFW ---")
    run_command("ufw default deny incoming")
    run_command("ufw default allow outgoing")
    # Mengizinkan SSH pada port default 22; sesuaikan jika diubah
    run_command("ufw allow ssh")
    # Aktifkan UFW
    run_command("ufw --force enable")

def configure_fail2ban():
    """
    Instal dan konfigurasikan Fail2Ban.
    """
    print("\n--- Mengonfigurasi Fail2Ban ---")
    # Membackup konfigurasi asli jika belum dibackup
    jail_local = "/etc/fail2ban/jail.local"
    if not os.path.exists(jail_local):
        shutil.copy("/etc/fail2ban/jail.conf", jail_local)
        print(f"Backup konfigurasi fail2ban dibuat di {jail_local}")
    
    # Konfigurasi dasar
    fail2ban_config = """
[DEFAULT]
# Bantime set to 1 hour
bantime = 3600
# Findtime set to 10 minutes
findtime = 600
# Max retry set to 5
maxretry = 5

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
"""

    with open(jail_local, 'w') as f:
        f.write(fail2ban_config)
    print("Konfigurasi Fail2Ban telah diperbarui.")
    run_command("systemctl restart fail2ban")
    run_command("systemctl enable fail2ban")

def secure_ssh():
    """
    Mengamankan konfigurasi SSH.
    """
    print("\n--- Mengamankan Konfigurasi SSH ---")
    ssh_config = "/etc/ssh/sshd_config"
    backup_ssh = "/etc/ssh/sshd_config.backup"
    
    # Backup konfigurasi SSH jika belum dibackup
    if not os.path.exists(backup_ssh):
        shutil.copy(ssh_config, backup_ssh)
        print(f"Backup konfigurasi SSH dibuat di {backup_ssh}")
    
    # Membaca konfigurasi SSH saat ini
    with open(ssh_config, 'r') as f:
        lines = f.readlines()
    
    # Mengubah konfigurasi yang diperlukan
    new_lines = []
    for line in lines:
        if line.startswith("#Port "):
            new_lines.append("Port 22\n")  # Ubah jika Anda ingin port yang berbeda
        elif line.startswith("Port "):
            new_lines.append("Port 22\n")  # Sesuaikan port jika diubah
        elif line.startswith("#PermitRootLogin"):
            new_lines.append("PermitRootLogin no\n")
        elif line.startswith("PermitRootLogin"):
            new_lines.append("PermitRootLogin no\n")
        elif line.startswith("#PasswordAuthentication"):
            new_lines.append("PasswordAuthentication no\n")
        elif line.startswith("PasswordAuthentication"):
            new_lines.append("PasswordAuthentication no\n")
        else:
            new_lines.append(line)
    
    # Menulis kembali konfigurasi SSH
    with open(ssh_config, 'w') as f:
        f.writelines(new_lines)
    print("Konfigurasi SSH telah diperbarui.")
    
    # Restart layanan SSH
    run_command("systemctl restart sshd")

def disable_unnecessary_services():
    """
    Menonaktifkan layanan yang tidak diperlukan.
    """
    print("\n--- Menonaktifkan Layanan yang Tidak Diperlukan ---")
    services = ["telnet", "ftp", "nfs-common", "rpcbind", "samba"]
    for service in services:
        run_command(f"systemctl disable {service} --now", check=False)

def setup_auto_updates():
    """
    Mengatur pembaruan otomatis untuk keamanan.
    """
    print("\n--- Mengatur Pembaruan Otomatis ---")
    run_command("apt-get install -y unattended-upgrades")
    # Mengaktifkan pembaruan otomatis
    run_command("dpkg-reconfigure --priority=low unattended-upgrades")

def enable_audit_logging():
    """
    Mengaktifkan audit logging dengan auditd.
    """
    print("\n--- Mengaktifkan Audit Logging ---")
    run_command("apt-get install -y auditd audispd-plugins")
    run_command("systemctl enable auditd")
    run_command("systemctl start auditd")
    print("Auditd telah diaktifkan dan berjalan.")

def main():
    check_root()
    update_and_upgrade()
    # Paket yang diperlukan
    packages = ["ufw", "fail2ban", "auditd", "unattended-upgrades"]
    install_packages(packages)
    setup_firewall()
    configure_fail2ban()
    secure_ssh()
    disable_unnecessary_services()
    setup_auto_updates()
    enable_audit_logging()
    print("\n=== Hardening Sistem Selesai ===")
    print("Beberapa langkah tambahan yang dapat Anda lakukan:")
    print("- Konfigurasi SSH Key Authentication.")
    print("- Memasang dan mengkonfigurasi AppArmor atau SELinux.")
    print("- Mengatur Monitoring dan Alerting.")
    print("- Menetapkan Kebijakan Kata Sandi yang Kuat.")
    print("- Menggunakan Tools Keamanan Tambahan seperti Lynis atau Bastille.")

if __name__ == "__main__":
    main()

