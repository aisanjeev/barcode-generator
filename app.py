from flask import Flask, render_template,request,make_response, session
# from werkzeug.utils import secure_filename
import pandas as pd
from flask_session import Session
import barcode
from barcode.writer import ImageWriter
import PIL
from PIL import Image
import pdfkit
import random
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
    session["name"] = "Sanjeev"
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        ExcelFileName=str(random.randrange(1, 10000000000))
        session["fileExe"] = ExcelFileName+'-output.csv'
        f = request.files['the_file']
        f.save('static/upload/'+ExcelFileName+'.xlsx')
        # # f.save(f"static/upload/{secure_filename(f.filename)}")
        df=pd.read_excel(r'static/upload/'+ExcelFileName+'.xlsx')
        TotalOrder=df['userid'].count()
        FinalOutput=[]
        for i in range(TotalOrder):
            FileName=str(random.randrange(1, 10000000000))
            OrderID=df['Order ID'][i]
            PostalCode=df['Postal code'][i]
            TrackingNumber=df['Tracking number'][i]
            BarcodeNumber='420'+str(PostalCode)+str(TrackingNumber)
            FirstName=df['First name'][i]
            LastName=df['Last name'][i]
            Street=df['Street'][i]
            City=df['City'][i]
            State=df['Province / State'][i]
            SKU=df['SKU'][i]
            date=df['order create time'][i]
            bar_class = barcode.get_barcode_class('Gs1_128')
            number = BarcodeNumber
            writer=ImageWriter()
            Gs1_128 = bar_class(number, writer)
            Gs1_128.save('static/temp/'+FileName) # save the originally generated image
            im = Image.open('static/temp/'+FileName+'.png') # open in a PIL Image object

            # Size of the image in pixels (size of original image)
            # (This is not mandatory)
            width, height = im.size
            
            # Setting the points for cropped image
            left = 2
            top = 0
            right =760
            bottom = 200
            
            # Cropped image of above dimension
            # (It will not change original image)
            im1 = im.crop((left, top, right, bottom))
            im1.save('static/upload/'+FileName+'.png') 
            # Shows the image in image viewer
            # im1.show()
            BarcodeFileName=FileName+'.png'
            tmp={"FirstName":FirstName,"LastName":LastName,"Street":Street,"City":City,"State":State,"BarcodeNumber":BarcodeNumber,"OrderID":OrderID,"BarcodeFileName":BarcodeFileName,"SKU":SKU,"date":date}
            FinalOutput.append(tmp)
        df1 = pd.DataFrame(FinalOutput)
        df1.to_csv('static/upload/'+ExcelFileName+'-output.csv')
        fileName=session.get('fileExe')
        # print(fileName)
        df=pd.read_csv(r'static/upload/'+fileName)
        options = {
            'page-height': '250',
            'page-width': '105',
            'margin-top': '0.1in',
            'margin-right': '0.1in',
            'margin-bottom': '0.1in',
            'margin-left': '0.1in',
            'encoding': "UTF-8",
            'custom-header': [('Accept-Encoding', 'gzip')],
            'no-outline': None
            }
        htmlData = render_template(
            "file.html",
            data=df.values.tolist())
        # print(html)
        pdfkit.from_string(htmlData, 'static/upload/'+ExcelFileName+'.pdf',options=options)

    return render_template('home.html', file=ExcelFileName+'.pdf')

@app.route('/test')
def test():
    fileName=session.get('fileExe')
        # print(fileName)
    df=pd.read_csv(r'static/upload/'+fileName)
    return render_template(
            "file.html",
            data=df.values.tolist())




if __name__ =="__main__":
    app.debug=True
    app.run()