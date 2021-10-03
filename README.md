# tes_beban_odoo
Script untuk tes beban Odoo versi 8 dan 12

Install Locust untuk tes beban Odoo

0. Install yang diperlukan
   sudo apt install -y python3 python3-venv git

1. Buat user bernama locust
   sudo useradd -m -d /home/locust -s /bin/bash locust

2. Buat virtual environment di user locust
   sudo su - locust
   python -m venv ve

3. Aktifkan virtual environment, lalu update pip
   source ve/bin/activate
   pip3 install --upgrade pip setuptools

4. Download dan install OdooLocust
   git clone https://github.com/odoo/OdooLocust.git
   cd OdooLocust
   python3 setup.py install

5. Untuk keperluan tes, install Faker
   pip3 install faker faker_vehicle

6. Download script tes
   git clone https://github.com/maizarrahman/tes_beban_odoo

7. Buat database kosong di Odoo
   Install Sale dan Inventory
   Atur sequence penomoran Sale Order agar cukup, misal 12 digit

8. Edit file init_odoo12.py (untuk Odoo 8: init_odoo8.py) untuk mengatur inisialisasi data
   Edit cust_num untuk mengatur jumlah data customer
   Edit prod_num untuk mengatur jumlah data produk
   Edit so_num untuk mengatur jumlah data sale order
   Edit line_num untuk mengatur jumlah baris maksimum dalam satu sale order

9. Jalankan inisialisasi data
   python3 init_odoo12.py

10. Agar cepat, bisa dipisah per data lalu dijalankan paralel
    Atau upload dari CSV.

11. Edit locust.conf 
    Edit host untuk mengatur target aplikasi Odoo

12. Jalankan locust
    ulimit -n 65535
    locust -f my_so12.py

13. Buka web browser di alamat localhost:8089

14. Tentukan jumlah user dan kecepatan munculnya user
    Klik Start Swarming

15. Jika sudah selesai, klik Download Data, klik Download Report

16. Sebaiknya diaktifkan monitoring pada database yang dibuat untuk mengetahui kinerjanya, terutama parameter database connection, query length, dan buffer cache. 
