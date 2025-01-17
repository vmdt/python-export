from io import BytesIO
from xhtml2pdf import pisa
from flask import render_template, Response, request
from endesive import pdf
import os
import tempfile
from src import app
from docxtpl import DocxTemplate

@app.route("/export/docs", methods=["POST"])
def export_docs():
    params = request.form
    print(params)
    doc_io = BytesIO()
    tpl = DocxTemplate("src/templates/template.docx")
    tpl.render(params)
    tpl.save(doc_io)
    doc_io.seek(0)
    return Response(doc_io.read(), mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
