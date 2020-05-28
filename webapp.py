#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, send_file, send_from_directory
from werkzeug.utils import secure_filename
import os, shutil

UPLOAD_FOLDER = 'files'
ALLOWED_EXTENSIONS = {'txt'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def run_timechecker(filepath):
    os.system('python3.7 timechecker.py ' + filepath)
    root_ext = os.path.splitext(filepath)
    file_xml_path = root_ext[0] + '.xml'
    return send_file(file_xml_path, as_attachment=True)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def index():
    shutil.rmtree(UPLOAD_FOLDER)
    os.mkdir(UPLOAD_FOLDER)
    return render_template('index.html')

@app.route('/', methods=['POST'])
def uplooad_xml():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return run_timechecker(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
