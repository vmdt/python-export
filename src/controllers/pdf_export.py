from xhtml2pdf import pisa
from flask import render_template, Response, request
from cryptography.hazmat.primitives.serialization import pkcs12
from endesive import pdf
import os
import tempfile
from src import app
import json
from io import BytesIO

@app.route("/pdf/itinerary", methods=["POST"])
def render_itinerary():
    params = request.form
    tour = json.loads(params['tour'])
    itinerary = tour.get("itinerary", [])
    html = render_template("itinerary/itinerary_tour.html", tour=tour, itinerary=itinerary)
    result = BytesIO()
    
    # Configure pisa with default font that supports Vietnamese
    pdf = pisa.pisaDocument(
        BytesIO(html.encode("UTF-8")), 
        result,
        encoding='UTF-8',
        link_callback=None,
        context={
            "pageSize": 1,
            "fontName": "Arial"
        }
    )

    if not pdf.err:
        return sign_to_file(result.getvalue())
    return None


def sign_to_file(pdf_render):
    fd, path = tempfile.mkstemp()

    # Load the PFX file using cryptography
    with open("src/media/RyanLieberman.pfx", "rb") as f:
        pfx_data = f.read()

    password = b"Welcome01"
    private_key, cert, additional_certs = pkcs12.load_key_and_certificates(pfx_data, password)

    # Sign the PDF document
    datau = pdf_render
    datas = pdf.cms.sign(
        datau,
        {
            "sigflags": 3,
            "contact": "vmdt03@gmail.com",
            "location": "Ho Chi Minh City, Viet Nam",
            "signingdate": "20180731082642+02'00'",
            "reason": "",
        },
        private_key,
        cert,
        [],
        "sha256",
    )

    with os.fdopen(fd, "wb") as fp:
        fp.write(datau)
        fp.write(datas)

    return Response(open(path, "rb").read(), mimetype="application/pdf")    