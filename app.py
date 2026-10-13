# app.py
# Titik awal aplikasi: membuat app, menyiapkan database, dan mendaftarkan controller.
from flask import Flask, render_template

from controllers.mahasiswa_controller import mahasiswa_bp
from models.mahasiswa_model import init_db

app = Flask(__name__)
app.secret_key = "ganti-dengan-kunci-rahasia-anda"  # dibutuhkan untuk flash message

app.register_blueprint(mahasiswa_bp)


@app.errorhandler(404)
def tidak_ditemukan(e):
    return render_template("404.html"), 404


# Pastikan tabel ada setiap kali aplikasi dijalankan
init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5001)