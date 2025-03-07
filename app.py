"""
Flask Serving

This file is a sample flask app that can be used to test your model with an API.

This app does the following:
    - Handles uploads and looks for an image file send as "file" parameter
    - Stores the image at ./images dir
    - Invokes ffwd_to_img function from evaluate.py with this image
    - Returns the output file generated at /output

Additional configuration:
    - You can also choose the checkpoint file name to use as a request parameter
    - Parameter name: checkpoint
    - It is loaded from /input
"""
import os
from flask import Flask, send_file, request
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename
import sys

from evaluate import ffwd_to_img

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
app = Flask(__name__)


@app.route('/styletransfer', methods=["GET", "POST"])
def style_transfer():
    """
    Take the input image and style transfer it
    """
    # check if the post request has the file part
    input_file = request.files.get('file')
    if not input_file:
        return BadRequest("File not present in request")

    filename = secure_filename(input_file.filename)
    if filename == '':
        return BadRequest("File name is not present in request")
    if not allowed_file(filename):
        return BadRequest("Invalid file type")

    input_filepath = os.path.join('./images/', filename)
    output_filepath = os.path.join('./output/', filename)
    input_file.save(input_filepath)

    # Get checkpoint filename from la_muse
    checkpoint = request.values.get("style", "udnie.ckpt")
    print("Use style model: {}".format(checkpoint), file=sys.stderr)
    ffwd_to_img(input_filepath, output_filepath, './data/models/' + checkpoint, '/gpu:0')
    return send_file(output_filepath, mimetype='image/jpg')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(host='0.0.0.0')
