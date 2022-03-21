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
    json = request.get_json(force=True)
    text, title = ocr.get_info(json["image"])
    title = title or 'My Docly Document'
    print(title)
    print(text)
    gdrive = GDrive(json["auth"])
    id = gdrive.upload_file(title, text)
    return {'url': f"https://docs.google.com/document/d/{id}/edit"}

app.run("localhost", 1234)
