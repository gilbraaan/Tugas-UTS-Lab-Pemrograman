# models/mahasiswa_model.py
# MODEL: tempat data hidup. Semua akses ke database SQLite ada di sini.
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mahasiswa.db")


def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row  # hasil query bisa diakses seperti dictionary
    return db


def init_db():
    """Membuat tabel jika belum ada. Dipanggil saat aplikasi start."""
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS mahasiswa (
            nim            INTEGER PRIMARY KEY,   -- unique otomatis
            nama           TEXT    NOT NULL,
            program_studi  TEXT    NOT NULL,
            angkatan       INTEGER NOT NULL,
            ipk            REAL    NOT NULL
        )
        """
    )
    db.commit()
    db.close()


def get_all():
    db = get_db()
    rows = db.execute("SELECT * FROM mahasiswa ORDER BY nim").fetchall()
    db.close()
    return [dict(r) for r in rows]


def get_by_nim(nim):
    db = get_db()
    row = db.execute("SELECT * FROM mahasiswa WHERE nim = ?", (nim,)).fetchone()
    db.close()
    return dict(row) if row else None


def create(nim, nama, program_studi, angkatan, ipk):
    db = get_db()
    db.execute(
        "INSERT INTO mahasiswa (nim, nama, program_studi, angkatan, ipk) "
        "VALUES (?, ?, ?, ?, ?)",
        (nim, nama, program_studi, angkatan, ipk),
    )
    db.commit()
    db.close()


def update(nim, nama, program_studi, angkatan, ipk):
    db = get_db()
    db.execute(
        "UPDATE mahasiswa SET nama = ?, program_studi = ?, angkatan = ?, ipk = ? "
        "WHERE nim = ?",
        (nama, program_studi, angkatan, ipk, nim),
    )
    db.commit()
    db.close()


def delete(nim):
    db = get_db()
    db.execute("DELETE FROM mahasiswa WHERE nim = ?", (nim,))
    db.commit()
    db.close()
