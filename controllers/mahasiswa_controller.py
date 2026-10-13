# controllers/mahasiswa_controller.py
# CONTROLLER: menerima request, validasi, memutuskan, memakai Model, lalu merespons.
from datetime import datetime

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from models import mahasiswa_model as model

mahasiswa_bp = Blueprint("mahasiswa_bp", __name__)


def tahun_sekarang():
    return datetime.now().year


def tambah_lama_studi(m):
    """Lama Studi dihitung program: tahun sekarang - angkatan (bukan input pengguna)."""
    m["lama_studi"] = tahun_sekarang() - m["angkatan"]
    return m


def validasi(form, nim_wajib=True):
    """Membaca & memvalidasi input form.
    Mengembalikan (data_bersih, daftar_error)."""
    errors = []

    nim_raw = (form.get("nim") or "").strip()
    nama = (form.get("nama") or "").strip()
    program_studi = (form.get("program_studi") or "").strip()
    angkatan_raw = (form.get("angkatan") or "").strip()
    ipk_raw = (form.get("ipk") or "").strip().replace(",", ".")

    nim = None
    if nim_wajib:
        if not nim_raw:
            errors.append("NIM wajib diisi.")
        else:
            try:
                nim = int(nim_raw)
                if nim <= 0 or nim > 9223372036854775807:
                    raise ValueError
            except ValueError:
                errors.append("NIM harus berupa angka bulat positif.")

    if not nama:
        errors.append("Nama wajib diisi.")
    if not program_studi:
        errors.append("Program studi wajib diisi.")

    angkatan = None
    if not angkatan_raw:
        errors.append("Angkatan wajib diisi.")
    else:
        try:
            angkatan = int(angkatan_raw)
            if angkatan < 1950 or angkatan > tahun_sekarang():
                errors.append(f"Angkatan harus antara 1950 dan {tahun_sekarang()}.")
        except ValueError:
            errors.append("Angkatan harus berupa angka bulat.")

    ipk = None
    if not ipk_raw:
        errors.append("IPK wajib diisi.")
    else:
        try:
            ipk = float(ipk_raw)
            if not (0.0 <= ipk <= 4.0):  # juga menolak nan
                errors.append("IPK harus berada pada rentang 0.00 - 4.00.")
        except ValueError:
            errors.append("IPK harus berupa angka (contoh: 3.75).")

    data = {
        "nim": nim if nim is not None else nim_raw,
        "nama": nama,
        "program_studi": program_studi,
        "angkatan": angkatan if angkatan is not None else angkatan_raw,
        "ipk": ipk if ipk is not None else ipk_raw,
    }
    return data, errors


# READ (daftar) -> GET /
@mahasiswa_bp.route("/", methods=["GET"])
def index():
    daftar = [tambah_lama_studi(m) for m in model.get_all()]
    return render_template("index.html", daftar=daftar, tahun=tahun_sekarang())


# READ (detail) -> GET /mahasiswa/<nim>
@mahasiswa_bp.route("/mahasiswa/<int:nim>", methods=["GET"])
def detail(nim):
    m = model.get_by_nim(nim)
    if m is None:
        abort(404)
    return render_template("detail.html", m=tambah_lama_studi(m), tahun=tahun_sekarang())


# CREATE (form) -> GET /mahasiswa/tambah
@mahasiswa_bp.route("/mahasiswa/tambah", methods=["GET"])
def form_tambah():
    return render_template("form.html", mode="tambah", data={}, errors=[])


# CREATE (proses) -> POST /mahasiswa/tambah
@mahasiswa_bp.route("/mahasiswa/tambah", methods=["POST"])
def proses_tambah():
    data, errors = validasi(request.form, nim_wajib=True)

    # NIM harus unik
    if not errors and model.get_by_nim(data["nim"]) is not None:
        errors.append(f"NIM {data['nim']} sudah terdaftar.")

    if errors:
        return render_template("form.html", mode="tambah", data=data, errors=errors), 400

    model.create(data["nim"], data["nama"], data["program_studi"], data["angkatan"], data["ipk"])
    flash(f"Mahasiswa {data['nama']} berhasil ditambahkan.", "sukses")
    return redirect(url_for("mahasiswa_bp.index"))


# UPDATE (form) -> GET /mahasiswa/<nim>/edit
@mahasiswa_bp.route("/mahasiswa/<int:nim>/edit", methods=["GET"])
def form_edit(nim):
    m = model.get_by_nim(nim)
    if m is None:
        abort(404)
    return render_template("form.html", mode="edit", data=m, errors=[])


# UPDATE (proses) -> POST /mahasiswa/<nim>/edit
@mahasiswa_bp.route("/mahasiswa/<int:nim>/edit", methods=["POST"])
def proses_edit(nim):
    if model.get_by_nim(nim) is None:
        abort(404)

    data, errors = validasi(request.form, nim_wajib=False)
    data["nim"] = nim  # NIM adalah kunci, tidak boleh diubah

    if errors:
        return render_template("form.html", mode="edit", data=data, errors=errors), 400

    model.update(nim, data["nama"], data["program_studi"], data["angkatan"], data["ipk"])
    flash(f"Data {data['nama']} berhasil diubah.", "sukses")
    return redirect(url_for("mahasiswa_bp.index"))


# DELETE -> POST /mahasiswa/<nim>/hapus
@mahasiswa_bp.route("/mahasiswa/<int:nim>/hapus", methods=["POST"])
def hapus(nim):
    m = model.get_by_nim(nim)
    if m is None:
        abort(404)
    model.delete(nim)
    flash(f"Mahasiswa {m['nama']} (NIM {nim}) berhasil dihapus.", "sukses")
    return redirect(url_for("mahasiswa_bp.index"))
