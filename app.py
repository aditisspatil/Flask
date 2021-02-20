from flask import Flask, render_template, request, redirect
from flask_uploads import configure_uploads, IMAGES, UploadSet
from PIL import Image

UPLOADER_PATH = 'static/img'
SIZE = (200, 200)

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = UPLOADER_PATH
configure_uploads(app, photos)


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

#
# def predict(files):
#     if 'image' not in files or files['image'].filename == '':
#         return render_template('index.html', warn='Please add an image')
#
#     else:
#         try:
#             sfname = photos.save(files['image'])
#             path = UPLOADER_PATH + '/' + sfname
#             return render_template('index.html', pred='XXX', fname=path)
#         except:
#             return render_template('index.html', warn='Unknown Error')


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method != 'POST' or 'image' not in request.files:
        return render_template('index.html', warn='Please add an image')

    else:
        if request.files['image'].filename != '':
            try:
                fname = photos.save(request.files['image'])
                path = UPLOADER_PATH + '/' + fname
                resize(path)
                return render_template('index.html', pred='XXX', fname=path)
            except:
                return render_template('index.html', warn='Unknown Error')

        return render_template('index.html', warn='Please add an image')


def resize(path):
    try:
        im = Image.open(path)
        im.thumbnail(SIZE, Image.ANTIALIAS)
        im.save(path)
    except IOError:
        print("cannot create thumbnail for %s" % path)


@app.route('/reset', methods=['POST', 'GET'])
def reset():
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
