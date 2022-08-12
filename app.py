from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
import urllib.request
import os
import cv2
import my_yolov6

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


# @app.route('/', methods=['GET', 'POST'])
# def upload_image():
#     form = UploadForm()
#     if form.validate_on_submit():
#         filename = photos.save(form.photo.data)
#         file_url = url_for('get_file', filename=filename)
#     else:
#         file_url = None

#     return render_template('index.html', form=form, file_url=file_url)

@app.route('/', methods=['GET', 'POST'])
def detect():
    form = UploadForm()

    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        input_img_url = url_for('get_file', filename=filename)
        
        print('input_img_url', input_img_url)
        frame = cv2.imread('.'+input_img_url)   # need: ./dir/filename (not /dir/filename)
        
        frame, num_objs = yolov6_model.infer(frame)
        print('type(frame) = %s'%(type(frame)))
        print('frame.shape = ', frame.shape)
        
        if num_objs > 0:
            output_img_url = DETECTED_DIR+ '/' + input_img_url.split('/')[-1]
            print('save_path', output_img_url)
            cv2.imwrite(output_img_url, frame)
            # cv2.imwrite('test_img.jpg', frame)
            print('frame exits \t num_objs=', num_objs)
        else:
            print('no obj detected')
        
        del frame
        
    else:
        output_img_url = None

    return render_template('index.html', form=form, file_url=output_img_url)




if __name__ == "__main__":
    app.run(debug=True)



# Followed https://www.youtube.com/watch?v=dP-2NVUgh50