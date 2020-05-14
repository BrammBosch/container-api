from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder="static", static_url_path="")



@app.route('/')
def upload_file():
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def upload_file_test():
    if request.method == 'POST':
        f = request.files['file']
        print(f.read())
        f.save(secure_filename(f.filename))
        print(f.read())

        return render_template('index.html',result='Succes')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

