from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, send_file
import urllib.request
import os
import cv2
import my_yolov6
import yaml
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField


app = Flask(__name__)

UPLOADED_DIR = 'static/uploaded_photos'
DETECTED_DIR = 'static/detected_photos'
app.config['UPLOADED_PHOTOS_DEST'] = UPLOADED_DIR
app.config['SECRET_KEY'] = 'asldfkjlj'

# load model when create server
yolov6_model = my_yolov6.my_yolov6('./yolo_weights/yolov6s.pt', 'cpu', './data/coco.yaml', 640, True)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Images only'),
            FileRequired('File field should not be empty')
        ]
    )
    submit = SubmitField('Upload')

@app.route('/%s/<filename>'%(UPLOADED_DIR))
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)


@app.route('/', methods=['GET', 'POST'])
def detect():
    form = UploadForm()
    input_img_url = None
    output_img_url = None
    
    # Read all YOLOv6 classes
    class_list = []
    with open('./data/coco.yaml', 'r') as file:
        data_load = yaml.safe_load(file)
        class_list = data_load['names']

    # Uploaded images
    if form.validate_on_submit():
        
        filename = photos.save(form.photo.data)
        input_img_url = url_for('get_file', filename=filename)
        
        frame = cv2.imread('.'+input_img_url)   # need: ./dir/filename (not /dir/filename)
        
        # Get checkbox results
        interested_class = request.form.getlist('mycheckbox')
        interested_class = set(class_list) if len(interested_class)==0 else set(interested_class)

        frame, num_objs, class_names = yolov6_model.infer(frame, interested_class=interested_class)
        
        if num_objs > 0:
            output_img_url = DETECTED_DIR+ '/' + input_img_url.split('/')[-1]
            cv2.imwrite(output_img_url, frame)
        
        del frame
        
        if num_objs > 0:
            return render_template('index.html', form=form, file_url=output_img_url, num_objs=num_objs, class_list=class_list, class_names=list(set(class_names)))
        return render_template('index.html', form=form, file_url=input_img_url, num_objs=num_objs, class_list=class_list)

    return render_template('index.html', form=form, file_url=None, num_objs=None, class_list=class_list)



if __name__ == "__main__":
    app.run(debug=True)



# Followed https://www.youtube.com/watch?v=dP-2NVUgh50