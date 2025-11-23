import os
import hashlib
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = set(["txt", "pdf", "png", "jpg", "jpeg", "gif", "doc", "docx", "xls", "xlsx", "csv", "zip", "rar"])

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024  # 32 MB
app.secret_key = "change-this-secret-key"

HASH_ALGOS = [
    "md5",
    "sha1",
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
]


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def compute_hashes(file_stream):
    """
    Recibe un file-like object (ya posicionado al inicio) y calcula
    múltiples hashes leyendo en chunks para soportar archivos grandes.
    """
    hash_objs = {name: hashlib.new(name) for name in HASH_ALGOS}

    # leer en bloques
    while True:
        chunk = file_stream.read(8192)
        if not chunk:
            break
        for h in hash_objs.values():
            h.update(chunk)

    # regresar hex digests
    return {name: h.hexdigest() for name, h in hash_objs.items()}


@app.route("/", methods=["GET", "POST"])
def index():
    hashes_1 = None
    hashes_2 = None
    same_file = None
    filename_1 = None
    filename_2 = None

    if request.method == "POST":
        # Primer archivo (obligatorio)
        file1 = request.files.get("file1")
        file2 = request.files.get("file2")

        if not file1 or file1.filename == "":
            flash("Debes seleccionar al menos el primer archivo.", "error")
            return redirect(url_for("index"))

        if not allowed_file(file1.filename):
            flash("Extensión no permitida para el primer archivo.", "error")
            return redirect(url_for("index"))

        filename_1 = secure_filename(file1.filename)
        # clonar el stream para poder reutilizarlo si es necesario
        file1.stream.seek(0)
        hashes_1 = compute_hashes(file1.stream)

        # segundo archivo opcional (para comparación)
        if file2 and file2.filename != "":
            if not allowed_file(file2.filename):
                flash("Extensión no permitida para el segundo archivo.", "error")
                return redirect(url_for("index"))

            filename_2 = secure_filename(file2.filename)
            file2.stream.seek(0)
            hashes_2 = compute_hashes(file2.stream)

            # comparamos usando un algoritmo fuerte, por ejemplo sha256
            same_file = hashes_1["sha256"] == hashes_2["sha256"]

    return render_template(
        "index.html",
        hashes_1=hashes_1,
        hashes_2=hashes_2,
        same_file=same_file,
        filename_1=filename_1,
        filename_2=filename_2,
        hash_algos=HASH_ALGOS,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
