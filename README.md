# Dashboard-Kas-Kelas

# Deskripsi
sesuai dengan namanya yaitu dashboard kas kelas. fungsi dashboard ini adalah menambah, menyimpan dan memanajemen semua keuangan baik secara pemasukan dan pengeluaran secara real time, serta menerima saran dari anggota untuk pengurus kas kelas

# Nama Anggota 
1. Ahmad Jaka Nugraha (25051204077)
2. Muhammad Dzaky Andika (25051204027)
3. Nabil Lingga Yostaka (25051204081)
4. Rafiul Zuhri (25051204122)

# Fitur Utama
1. Halaman Login untuk admin dan anggota
2. Pada Dashboar utama menampilkan grafik pemasukan dan pengeluaran secara real time
3. Pemasukan yang didalamnya terdapat keterangan dan sumber dana (Admin)
4. Pengeluaran juga yang didalamya terdapat keterangan (Admin)
5. pada fitur Kotak Saran, terdapat perbedaan antara anggota dan admin

   a. pada anggota bisa mengirim saran dari admin  
   b. pada admin hanya menerima kotak saran yang dikirim dari anggota dan bisa menghapusnya

# Cara menjalankan Project
1. install di cmd "pip install streamlit pandas plotly openpyxl"
2. Download extension streamlit runner di VS Code
3. siapkan file python khusus streamlit untuk dijalankan
4. klik kanan file python yang akan dijalankan
5. pilih run with streamlit

# Penjelasan Implementasi OOP
1. Inheritance
pada Class Pengurus dan Anggota, merupakan turunan dari class User. selain itu kode ini juga menerapkan pada class pemasukan dan pengeluaran yang merupakan turunan dari class Transaksi
2. Encapsulation
Konsep enkapsulasi pada kode ini diterapkan dengan membungkus data dan fungsi ke dalam sebuah class. sebagai contoh pada class dashboard menyimpan daftar transaksi dan menyediakan method lain yaitu tambah transaksi, dan hapus transaksi sehingga pengelolahan transaksi lebig terstruktur
3. Abstraction
Konsep Abstraksi diterapkan di kode ini pada bagian "dashboard.hitung_saldo()". Pengguna cukup memanggil method tersebut tanpa perlu mengetahui proses perhitungan total pemasukan dan pengeluaran yang terjadi di dalam program.
4. Polymorphism
Polimorfisme diterapkan melalui method overriding pada class transaksi dengan method "to_dict(self)". Method tersebut kemudian dioverride pada class Pemasukan dan Pengeluaran untuk menghasilkan struktur data yang berbeda sesuai jenis transaksi. Dengan demikian, method yang sama dapat menghasilkan perilaku yang berbeda tergantung objek yang memanggilnya.

# Screenshot 
<img width="1365" height="627" alt="WhatsApp Image 2026-06-03 at 22 24 43" src="https://github.com/user-attachments/assets/2a840009-573d-4f83-a131-921da7a6326b" />
<img width="1366" height="768" alt="WhatsApp Image 2026-06-03 at 22 24 44" src="https://github.com/user-attachments/assets/5c0cf44e-b52e-4fbe-94f3-3001d6a8e0f1" />
<img width="1366" height="768" alt="WhatsApp Image 2026-06-03 at 22 24 44 (1)" src="https://github.com/user-attachments/assets/5fedee89-ddaf-47ae-9c5f-0fde8b17590a" />
<img width="1366" height="768" alt="WhatsApp Image 2026-06-03 at 22 24 43 (2)" src="https://github.com/user-attachments/assets/82410041-d61c-4ff6-87bc-2998599ebbd9" />
<img width="1366" height="768" alt="WhatsApp Image 2026-06-03 at 22 24 43 (1)" src="https://github.com/user-attachments/assets/4e8ca100-a768-4209-bd81-07ee1443f630" />
