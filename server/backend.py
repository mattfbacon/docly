from flask import Flask, request
from ocr import OCR
from gdrive import GDrive

ocr = OCR()

app = Flask(__name__,
            static_url_path="", 
            static_folder="client/build/")

@app.route("/api/submit", methods=["POST"])
def submit():
    json = request.json
    text = ocr.get_text(json["image"])
    gdrive = GDrive(json["auth"])
    gdrive.make_doc(text)