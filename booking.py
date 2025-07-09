import csv
import datetime

BOOKING_FILE = 'booking.csv'
antrian_pemesan = []
jadwal_lapangan = {}

# Muat data dari CSV
def muat_data():
    try:
        with open(BOOKING_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                key = f"{row['tanggal']}|{row['jam']}|{row['lapangan']}"
                if row['status'] == 'dipesan':
                    jadwal_lapangan[key] = 'Terisi'
                    if row['nama'] not in antrian_pemesan:
                        antrian_pemesan.append(row['nama'])
                elif key not in jadwal_lapangan:
                    jadwal_lapangan[key] = 'Tersedia'
    except FileNotFoundError:
        with open(BOOKING_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['nama', 'tanggal', 'jam', 'lapangan', 'status'])
            writer.writeheader()

# Simpan booking ke file
def simpan_booking(nama, tanggal, jam, lapangan, status='dipesan'):
    with open(BOOKING_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['nama', 'tanggal', 'jam', 'lapangan', 'status'])
        writer.writerow({'nama': nama, 'tanggal': tanggal, 'jam': jam, 'lapangan': lapangan, 'status': status})

# Validasi input tanggal dan jam
def input_tanggal():
    while True:
        try:
            tanggal = input("Tanggal (YYYY-MM-DD): ")
            datetime.datetime.strptime(tanggal, '%Y-%m-%d')
            return tanggal
        except ValueError:
            print("Format tanggal salah. Gunakan YYYY-MM-DD")

def input_jam():
    pilihan_jam = ["09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:30", "19:30"] 
    print("==== Pilihan jam yang tersedia ====")
    for jam in pilihan_jam:
        print(f"• {jam}")
    
    while True:
        jam = input("Pilih jam (HH:MM): ")
        if jam in pilihan_jam:
            return jam
        else:
            print("Jam tidak valid. Pilih hanya dari daftar jam yang tersedia.")

def input_lapangan():
    while True:
        lapangan = input("Jenis Lapangan (Futsal/Bulutangkis/Basket): ").strip().capitalize()
        if lapangan in ['Futsal', 'Bulutangkis', 'Basket']:
            return lapangan
        else:
            print("Jenis lapangan tidak valid. Pilih hanya: Futsal, Bulutangkis, atau Basket.")


# Tambah Booking
def tambah_booking():
    nama = input("Masukkan nama Anda: ")
    tanggal = input_tanggal()
    jam = input_jam()
    
    try:
        waktu_booking = datetime.datetime.strptime(f"{tanggal} {jam}", '%Y-%m-%d %H:%M')
        if waktu_booking < datetime.datetime.now():
            print("Tidak bisa booking untuk waktu yang sudah lewat")
            return
    except ValueError:
        print("Format waktu tidak valid")
        return
    
    lapangan = input_lapangan()
    key = f"{tanggal}|{jam}|{lapangan}"

    if jadwal_lapangan.get(key, 'Tersedia') == 'Tersedia':
        jadwal_lapangan[key] = 'Terisi'
        antrian_pemesan.append(nama)
        simpan_booking(nama, tanggal, jam, lapangan)
        print("Booking berhasil dan masuk ke antrian")
    else:
        print("Jadwal tidak tersedia. Silakan pilih waktu lain")

# Tampilkan antrian booking
def tampilkan_antrian():
    try:
        with open(BOOKING_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader if row['status'] == 'dipesan']
            
            data.sort(key=lambda x: (x['tanggal'], x['jam']))
            
            print("\nAntrian booking saat ini:")
            for idx, row in enumerate(data, 1):
                print(f"{idx}. {row['nama']} - {row['tanggal']} {row['jam']} ({row['lapangan']})")
    except FileNotFoundError:
        print("Belum ada data booking")

# Batalkan booking
def batal_booking():
    nama = input("Masukkan nama untuk pembatalan: ")
    rows = []
    updated = False
    try:
        with open(BOOKING_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['nama'] == nama and row['status'] == 'dipesan' and not updated:
                    row['status'] = 'dibatalkan'
                    key = f"{row['tanggal']}|{row['jam']}|{row['lapangan']}"
                    jadwal_lapangan[key] = 'Tersedia'
                    updated = True
                rows.append(row)
        with open(BOOKING_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['nama', 'tanggal', 'jam', 'lapangan', 'status'])
            writer.writeheader()
            writer.writerows(rows)
        if updated:
            if nama in antrian_pemesan:
                antrian_pemesan.remove(nama)
            print("Booking berhasil dibatalkan.")
        else:
            print("Tidak ditemukan booking atas nama tersebut")
    except FileNotFoundError:
        print("Belum ada data booking")

# Cek ketersediaan
def cek_ketersediaan():
    tanggal = input_tanggal()
    jam = input_jam()
    lapangan = input_lapangan()
    key = f"{tanggal}|{jam}|{lapangan}"
    status = jadwal_lapangan.get(key, 'Tersedia')
    print(f"Status: {status}")

# Menu utama
def menu():
    muat_data()
    while True:
        print("\n==== SPORTBOOK MENU ====")
        print("1. Tambah Booking")
        print("2. Lihat Antrian Booking")
        print("3. Batalkan Booking")
        print("4. Cek Ketersediaan")
        print("5. Keluar")
        pilihan = input("Pilih menu (1-5): ")
        
        if pilihan == '1':
            tambah_booking()
        elif pilihan == '2':
            tampilkan_antrian()
        elif pilihan == '3':
            batal_booking()
        elif pilihan == '4':
            cek_ketersediaan()
        elif pilihan == '5':
            print("Terima kasih telah menggunakan SportBook!")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    menu()
