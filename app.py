from flask import Flask, request, jsonify
import pdfplumber
import io

app = Flask(__name__)

@app.route("/extract", methods=["POST"])
def extract_table():
    file = request.files["file"]
    pdf_bytes = file.read()
    line_items = []

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if row and any(cell and cell.strip() for cell in row):
                        line_items.append(row)

    return jsonify(line_items)

if __name__ == "__main__":
    app.run(debug=True)
