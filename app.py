from Image_cls import predictImage
from flask import Flask, render_template,request,redirect,url_for, flash, send_file
import pymysql
import os
from werkzeug.utils import secure_filename

import firebase_admin
from firebase_admin import ml
from firebase_admin import credentials


# firebase_admin.initialize_app(
#   credentials.Certificate('/path/to/your/service_account_key.json'),
#   options={
#       'storageBucket': 'gs://tggs-cnn.appspot.com',
#   })



# firebase_admin.initialize_app(
#   credentials.Certificate('/path/to/your/service_account_key.json'),
#   options={
#       'storageBucket': 'your-storage-bucket',
#   })



app = Flask(__name__, template_folder= 'public')

# UPLOAD_FOLDER = '/Users/thiraprarom/TGGS/Project/upload_folder'
# UPLOAD_FOLDER = 'gs://visaulab.appspot.com'

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template('index.html')

# @app.route('/uploadfile', methods=['GET', 'POST'])
# def upload_file():
#     # print('Test')
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             print('no file')
#             return redirect(url_for('index'))
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit a empty part without filename
#         if file.filename == '':
#             print('no filename')
#             return redirect(url_for('index'))
#         else:
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#       #send file name as parameter to downlad
#             print("saved file successfully")
#             print(filename)
#             return render_template("index.html", result = filename)
#             # return redirect('/return-files/'+ filename)



config = {
    #Hidden
    apiKey: "AIzaSyAJsdM1eZr0JYT1sFNfuCtLhIKK6N21Hm0",
    authDomain: "visaulab.firebaseapp.com",
    projectId: "visaulab",
    storageBucket: "visaulab.appspot.com",
    messagingSenderId: "650456939169",
    appId: "1:650456939169:web:83964f3d4d4192f89f8ee0"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
auth = firebase.auth()

@app.route('/', methods=['GET', 'POST'])
#Login
def basic():
    unsuccessful = 'Please check your credentials'
    successful = 'Login successful'
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['pass']
        try:
            auth.sign_in_with_email_and_password(email, password)
            return render_template('index.html', s=successful)
        except:
            return render_template('index.html', us=unsuccessful)
    return render_template('index.html')

#Posting function
@app.route('/uploadfile', methods=['GET','POST'])
def uploadfile():
    if request.method == 'POST':
        try:
            path_on_cloud = "images/newproduct.jpg"
            path_local=request.form['file']
            storage.child(path_on_cloud).put(path_local)
            return render_template("index.html")
        except:
            return render_template("index.html")






@app.route("/predict")
def predictimage():
    return_label = upload_file()
    if request.method == 'POST':
        print(return_label)
        if request.form["predict"] == "predict":
            # check if the post request has the file part
            path ="/Users/thiraprarom/TGGS/Project/upload_folder/"
            path = path + return_label
            print(path)
            # dirs = os.listdir( path )
            # print(dirs)
            # for p in dirs:
            #     p = p 
            #     p = path + p
            path = os.open(path)
            labels = predictImage(path)
            print(labels)
            return render_template('index.html',label = labels)
        else: 
            return render_template('index', code = "302")
    else:
        return redirect(url_for('index'))
        

if __name__ == "__main__":
    app.run(debug= True)

