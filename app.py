from flask import Flask, redirect, render_template, request, session, url_for
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

import os
import model_predict

upload_path = "/home/manjeets/test/covid19track/uploads/"
app = Flask(__name__)


dropzone = Dropzone(app)

app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_REDIRECT_VIEW'] = 'results'

app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

app.config['SECRET_KEY'] = 'supersecretkeygoeshere'

session = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    
    # set session for image results
    if "file_urls" not in session:
        session['file_urls'] = []
    if "file_name" not in session:
        session['file_name'] = ""
    # list to hold our uploaded image urls
    file_urls = session['file_urls']
    file_name = session['file_name']
    # handle image upload from Dropzone
    if request.method == 'POST':
        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)
            
            # save the file with to our photos folder
            filename = photos.save(
                file,
                name=file.filename    
            )
            # append image urls
            file_urls.append(photos.url(filename))
            
        session['file_urls'] = file_urls
        session['file_name'] = filename
        return "uploading..."
    # return dropzone template on GET request    
    return render_template('index.html')

@app.route('/results')
def results():
    
    # redirect to home if no images to display
    if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('index'))
    if "file_name" not in session or session['file_name'] == "":
        return redirect(url_for('index'))
        
    # set the file_urls and remove the session variable
    file_urls = session['file_urls']
    file_name = session['file_name']

    filepath = os.path.join(upload_path, file_name)
    test_results = model_predict.predict_covid(filepath)
    print(test_results)
    session.pop('file_urls', None)
    session.pop('file_name', None)
    
    return render_template('results.html', file_urls=file_urls)

if __name__ == "__main__":
    app.run(host="192.168.0.30")
