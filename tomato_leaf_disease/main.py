from flask import Flask,flash, request, redirect, url_for, render_template
import numpy as np
from keras.preprocessing import image
from keras.models import load_model
UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

import os
from app import app
import urllib.request
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		return redirect(url_for('predict',filename=filename))
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)



@app.route('/predict/<filename>')
def predict(filename):
    test = image.load_img("static/uploads/"+filename,target_size=(150,150,3))
    model = load_model('test_model.h5')
    test=np.array(test)
    test=test/255
    test=np.expand_dims(test,axis=0)
    result=model.predict(test)
    pred_name = np.argmax(result)
    if pred_name==0:
	     pred_name="Bacterial spot"
    elif pred_name==1:
	    pred_name="Early blight"
    elif pred_name==2:
	    pred_name="Late blight"
    elif pred_name==3:
	    pred_name="Leaf Mold"
    elif pred_name==4:
	    pred_name="Septoria leaf spot"
    elif pred_name==5:
	     pred_name="Spider mites Two spotted spider mite"
    elif pred_name==6:
         pred_name="Target Spot"
    elif pred_name==7:
	    pred_name="Tomato Yellow Leaf Curl Virus"
    elif pred_name==8:
	    pred_name="Tomato mosaic virus"
    else:
	    pred_name="Healthy"	 		 		 		 		 		 		 		 		 
    return render_template('display.html',pred_name=pred_name,filename='uploads/' + filename)

    
if __name__ == "__main__":
    app.run()