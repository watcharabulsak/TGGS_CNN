from Image_cls import predictImage
from flask import Flask, render_template,request,redirect,url_for, flash, send_file
import os
from werkzeug.utils import secure_filename

import firebase_admin
from firebase_admin import App, ml
from firebase_admin import credentials
import json5
 

# firebase_admin.initialize_app(
#   credentials.Certificate('/path/to/your/service_account_key.json'),
#   options={
#       'storageBucket': 'gs://tggs-cnn.appspot.com',
#   })


config = {
    #Hidden
    apiKey: "AIzaSyAJsdM1eZr0JYT1sFNfuCtLhIKK6N21Hm0",
    authDomain: "visaulab.firebaseapp.com",
    projectId: "visaulab",
    storageBucket: "visaulab.appspot.com",
    messagingSenderId: "650456939169",
    appId: "1:650456939169:web:83964f3d4d4192f89f8ee0"
}

firebase = firebase_admin.initialize_app(config)


app = Flask(__name__, template_folder= 'public')

# UPLOAD_FOLDER = '/Users/thiraprarom/TGGS/Project/upload_folder'
UPLOAD_FOLDER = firebase.app().storage('gs://visaulab.appspot.com')

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    # print('Test')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(url_for('index'))
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(url_for('index'))
        else:
            file = request.files['file']
            firebase.storage().put(file)
            filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      #send file name as parameter to downlad
            print("saved file successfully")
            print(filename)
            return render_template("index.html", result = filename)
            # return redirect('/return-files/'+ filename)






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
 

# @app.route('/messenger/message/send/picture/individual', methods=['post'])
# def send_individual_picture():
#     picture = request.files['picture']
#     temp = tempfile.namedtemporaryfile(delete= False)
#     picture.save(temp.name)
#     firebase.storage().put(temp.name)
#     # clean-up temp image
#     os.remove(temp.name) 
    
    
# @app.route('/messenger/message/send/picture/individual', methods=['post'])
# def send_individual_picture():
#     picture = request.files['picture']
#     firebase.storage().put(picture)

# @app.route('/messenger/message/send/picture/individual', methods=['post'])
# def send_individual_picture():
#     picture = request.files['picture']
#     firebase.storage().put(picture) 


# @app.route('/', methods=['GET', 'POST'])
# #Login
# def basic():
#     unsuccessful = 'Please check your credentials'
#     successful = 'Login successful'
#     if request.method == 'POST':
#         email = request.form['name']
#         password = request.form['pass']
#         try:
#             auth.sign_in_with_email_and_password(email, password)
#             return render_template('index.html', s=successful)
#         except:
#             return render_template('index.html', us=unsuccessful)
#     return render_template('index.html')