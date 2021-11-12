import sys
import os
import contourSyntaxValidator as con

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_caching import Cache

UPLOAD_FOLDER = './Uploads'
ALLOWED_EXTENSIONS = ('txt',)
cache = Cache()

app = Flask(__name__, template_folder='./templates')
app.secret_key = 'e0e84c58cd32c2e30368677f520d5cc2'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def from_file_checking():
    filename = os.path.join(app.config['UPLOAD_FOLDER'],
                            "".join(os.listdir(app.config['UPLOAD_FOLDER'])))
    contours = con.reader(filename)
    return len(contours), *con.getInvalidContour(contours)

def from_input_checking(contour):
    valid, syntaxError, modelError = con.syntaxValidator(contour)
    if not valid:
        return 1, "1", contour, syntaxError, modelError
    return 1, "0", "", "", ""

@app.before_first_request
def clear_uploads():
    for files in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], files))

@app.before_first_request
def clear_cache():
    cache.init_app(app)
    with app.app_context():
        cache.clear()

@app.route('/')
def index():
    return render_template('index.html', countError=None, allCount=None,
                           contour=None, syntaxError=None, modelError=None, message=None)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        clear_uploads()
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template("index.html", countError=None, allCount=None, contour=None, syntaxError=None,
                                   modelError=None, message="Plik został dodany!")

@app.route('/check', methods=['GET', 'POST'])
def check():
    contour = request.form['contour']
    if contour:
        allCount, *param = from_input_checking(contour)
    else:
        allCount, *param = from_file_checking()
    return render_template("index.html", countError=param[0],
                           allCount=allCount, contour=param[1],
                           syntaxError=param[2], modelError=param[3])

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port, debug=True)
    else:
        app.run(debug=True)
