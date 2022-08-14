from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, send_file
import urllib.request
import os
import cv2
import my_yolov6
import yaml
from random import random
from werkzeug.utils import secure_filename

app = Flask(__name__)

STATIC_DIR = 'static/'
PHOTO_DIR = 'photos/'

app.secret_key = "secretkey"
app.config['UPLOAD_FOLDER'] = STATIC_DIR + PHOTO_DIR
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# load model when create server
yolov6_model = my_yolov6.my_yolov6('./yolo_weights/yolov6s.pt', 'cpu', './data/coco.yaml', 640, True)


@app.route('/')
def home():
    clean_dir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', class_list=get_class_list())

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Read all YOLOv6 classes
    class_list = get_class_list()

    # RECEIVE Files
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

        input_img_url = url_for('get_file', filename=filename)
        print('input_img_url', input_img_url)
        frame = cv2.imread('.'+input_img_url)   # need: ./dir/filename (not /dir/filename)

        # Get checkbox results
        interested_class = request.form.getlist('mycheckbox')
        interested_class = set(class_list) if len(interested_class)==0 else set(interested_class)
        print('interested_class = ', interested_class)
        
        # Get YOLO result
        frame, num_objs, class_names = yolov6_model.infer(frame, interested_class=interested_class)
        print('detected class_names', class_names)
        print('num_objs && class_names', num_objs, len(class_names))

        # Save result
        return_file = str(random())+ '-' + input_img_url.split('/')[-1]
        output_img_url = os.path.join(app.config['UPLOAD_FOLDER'], return_file)
        print('output_img_url =', output_img_url)
        cv2.imwrite(output_img_url, frame)
        
        del frame
        
        return render_template('index.html', filename=output_img_url.split('/')[-1], class_list=class_list)

    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display<filename>')
def display_image(filename):
    return redirect(url_for('static', filename=PHOTO_DIR+filename), code=301)

@app.route('/%s/<filename>'%(app.config['UPLOAD_FOLDER']))
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(path, as_attachment=True)

def get_class_list():
    class_list = []
    with open('./data/coco.yaml', 'r') as file:
        data_load = yaml.safe_load(file)
        class_list = data_load['names']
    return sorted(class_list)

def clean_dir(path):
    list_dir = os.listdir(path)
    if list_dir and len(list_dir)>0:
        for file in list_dir:
            if file == '.gitkeep': continue
            os.remove(os.path.join(path, file))

if __name__ == "__main__":
    app.run(debug=True)