from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

from db import db_init, db
from models import Img

import base64

app = app = Flask( 
  __name__,
  template_folder='templates',
  static_folder='static'
)

# SQLAlchemy config. Read more: https://flask-sqlalchemy.palletsprojects.com/en/2.x/
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    pic = request.files['pic']
    if not pic:
        return 'No pic uploaded!', 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400

    img = Img(img=pic.read(), name=filename, mimetype=mimetype)
    db.session.add(img)
    db.session.commit()

    return render_template('upload.html')

@app.route('/display', methods=['POST'])
def display_img():
    img_list = Img.query.all()

    for i in range(len(img_list)):
        encoded_string = base64.b64encode(img_list[i].img)
        encoded_string = encoded_string.decode('utf-8')
        img_list[i].img = encoded_string

    return render_template('image.html', user_images = img_list)