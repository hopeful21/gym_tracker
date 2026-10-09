
Siapkan project Django FORM / FITNESS yang ada di folder ini untuk deployment gratis ke Render dengan database PostgreSQL dari Neon.

Persyaratan:

1. Periksa struktur project dan konfigurasi Django yang sudah ada sebelum mengubah file.
2. Pertahankan semua fitur, desain UI, autentikasi username/password jika sudah ada, dan data workout.
3. Tambahkan dukungan PostgreSQL menggunakan DATABASE_URL dari environment variable. Tetap izinkan SQLite untuk development lokal.
4. Konfigurasikan SECRET_KEY melalui environment variable, DEBUG=False saat production, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS, dan pengaturan keamanan production.
5. Siapkan Gunicorn dan WhiteNoise untuk menjalankan Django serta menyajikan static files.
6. Pastikan requirements.txt berisi seluruh dependency production yang diperlukan.
7. Siapkan build command untuk instalasi dependency, collectstatic, dan migration.
8. Jangan menghapus db.sqlite3, jangan mereset database, dan jangan menjalankan migrasi destruktif. Jelaskan cara memindahkan data SQLite yang sudah ada ke PostgreSQL secara aman.
9. Periksa apakah file gambar exercise disimpan lokal atau menggunakan URL eksternal, dan pastikan gambar yang dibutuhkan ikut tersedia saat deployment.
10. Tambahkan petunjuk deployment Render dan variabel environment yang harus diisi. Jangan menampilkan atau menanamkan secret asli ke source code.
11. Jalankan pengujian Django dan perbaiki masalah yang ditemukan sebelum menyatakan project siap deploy.
