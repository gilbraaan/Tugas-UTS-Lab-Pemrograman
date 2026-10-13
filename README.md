# Aplikasi CRUD Data Mahasiswa

UTS Lab Pemrograman - Departemen Bisnis Digital, Universitas Diponegoro.

Stack: Python + Flask, SQLite, HTML + CSS. Pola MVC (models / controllers / templates).

## Menjalankan
```
python -m venv venv
venv\Scripts\activate        # Windows  (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
python app.py
```
Buka http://127.0.0.1:5000

## Fitur
- Create, Read (daftar + detail), Update, Delete data mahasiswa
- Validasi: nim/nama/program_studi/angkatan/ipk wajib, IPK 0.00-4.00, NIM unik
- Lama Studi = tahun sekarang - angkatan (dihitung otomatis)
- Data tersimpan di file SQLite `mahasiswa.db` (dibuat otomatis)
