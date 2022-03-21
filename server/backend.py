from flask import Flask, request, send_from_directory, send_file
from ocr import OCR
from gdrive import GDrive

ocr = OCR()

app = Flask(__name__,
            static_url_path="")

@app.route("/")
def root():
    return send_file("static/index.html")


@app.route("/api/submit", methods=["POST"])
def submit():
    json = request.json
    info = ocr.get_info(json["image"])
    print(info)
    # gdrive = GDrive(json["auth"], text)
    # gdrive.make_doc(text)

app.run("localhost", 3000)