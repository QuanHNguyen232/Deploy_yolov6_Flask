from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
import urllib.request
import os
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField


app = Flask(__name__)
UPLOADED_DIR = 'static'
app.config['UPLOADED_PHOTOS_DEST'] = UPLOADED_DIR
app.config['SECRET_KEY'] = 'asldfkjlj'

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
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
    else:
        file_url = None

    return render_template('index.html', form=form, file_url=file_url)




if __name__ == "__main__":
    app.run(debug=True)



# Followed https://www.youtube.com/watch?v=dP-2NVUgh50