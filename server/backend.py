from flask import Flask, request, send_from_directory, send_file
from ocr import OCR
from gdrive import GDrive, make_url

ocr = OCR()

app = Flask(__name__,
            static_url_path="")

@app.route("/")
def root():
    return send_file("static/index.html")


@app.route("/api/submit", methods=["POST"])
def submit():
    json = request.get_json(force=True)
    text, title = ocr.get_info(json["image"])
    title = title or 'My Docly Document'
    print(title)
    print(text)
    gdrive = GDrive(json["auth"])
    id = gdrive.upload_file(title, text)
    return {'url': make_url(id)}

app.run("localhost", 0)
