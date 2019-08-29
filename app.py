from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from filters import applyFilters
from PIL import Image


#Flask App Structure
app = Flask(__name__)
app.config.from_object(__name__)


CORS(app)


#server route working
@app.route('/')
def hello_world():
   return jsonify({"resp": "server is running!"})

#AddFormData
@app.route('/predict', methods=['POST'])
# @cross_origin()
def registerMissingReq():
    status = "not-success"
    if request.files['image']:
        image = request.files['image']
        filename = secure_filename(image.filename)
        image.save('static/' + filename)
        data = applyFilters('./static/'+filename)
        fileNames = {
            "original": filename,
            "laplacian": data[0],
            "sobelx": data[1],
            "sobely": data[2],
            "edges": data[3],
            "gray": data[4],
            "binary": data[5]
        }
        return fileNames
    else:
        return status

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='3000')