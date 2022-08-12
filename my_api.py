from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request
import os
import cv2
import my_yolov6

# Create Flask Server Backend
app = Flask(__name__)

# Apply Flask CORS
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = "./static/"

# load model when create server
yolov6_model = my_yolov6.my_yolov6('./my_weights/yolov6s.pt', 'cpu', './data/coco.yaml', 640, True)

@app.route('/', methods=['POST'] )
# @cross_origin(origin='*')
def predict_yolov6():

    if request.method == 'POST':
        image = request.files.get('file', None)
        if image:
            # save file
            path_to_save = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            print("Save = ", path_to_save)
            image.save(path_to_save)

            frame = cv2.imread(path_to_save)

            # detect via Yolov6 -> return img + bbox
            frame, num_objs = yolov6_model.infer(frame)

            if num_objs >0:
                cv2.imwrite(path_to_save, frame)

            # remove from memory
            del frame

            return path_to_save # http://server.com/static/path_to_save
        
        return 'Upload file to detect'
    return 'predict_yolov6 method'



# Start Backend
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='6868')