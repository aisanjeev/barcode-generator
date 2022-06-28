from flask import Flask, render_template,request,make_response
# from werkzeug.utils import secure_filename
import pandas as pd
import barcode
import pdfkit
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        # f = request.files['the_file']
        # f.save('static/upload/uploaded_file.xlsx')
        # # f.save(f"static/upload/{secure_filename(f.filename)}")
        df=pd.read_excel(r'static/upload/uploaded_file.xlsx')
        TotalOrder=df['userid'].count()
        for i in range(TotalOrder):
            PostalCode=df['Postal code'][i]
            TrackingNumber=df['Tracking number'][i]
            BarcodeNumber='420'+str(PostalCode)+'94'+str(TrackingNumber)
            print(BarcodeNumber)
            barcode_format = barcode.get_barcode_class('Gs1_128')
            my_barcode = barcode_format(BarcodeNumber, writer=None)
            my_barcode.save("generated_barcode")
    return "test"

@app.route("/test")
def test():
    options = {
    'page-height': '250',
    'page-width': '105',
    'margin-top': '0.1in',
    'margin-right': '0.1in',
    'margin-bottom': '0.1in',
    'margin-left': '0.1in',
    'encoding': "UTF-8",
    'custom-header': [
        ('Accept-Encoding', 'gzip')
    ],
    'no-outline': None
}
    pdfkit.from_url('http://127.0.0.1:5000/file','test.pdf',options=options)
    # name = "Giovanni Smith"
    # html = render_template("home.html",name=name)
    # pdf = pdfkit.from_string(html, False)
    # response = make_response(pdf)
    # response.headers["Content-Type"] = "application/pdf"
    # response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return "test"

@app.route('/file')
def file():
    return render_template('file.html')

        


if __name__ =="__main__":
    app.debug=True
    app.run()