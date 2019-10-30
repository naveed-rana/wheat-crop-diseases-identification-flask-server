from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from filters import applyFilters
from PIL import Image
import random

#Flask App Structure
app = Flask(__name__)
app.config.from_object(__name__)


CORS(app)


#server route working
@app.route('/')
def index():
   return jsonify({"resp": "server is up and running!"})


@app.route('/test')
def test():
   return jsonify({"resp": "server is up and running Emb!"})

#@app.route('/assets/<path:path>')
#def serve_files(path):
#    return send_from_directory('assets/', path)


diseaseData = ["Leaf rust", "Yellow spot", "Eye Spot", "Narrow Spot", "Ring Spot"]

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
	    "status": "success",
            "original": filename,
            "sobelx": data[0],
            "sobely": data[1],
            "edges": data[2],
            "gray": data[3],
            "binary": data[4],
            "hsi" : data[5],
            "embosse" : data[6],
            "disease" : diseaseData[random.randint(0,4)]
        }
        return fileNames
    else:
        return {"status": status}

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80, debug=True)
