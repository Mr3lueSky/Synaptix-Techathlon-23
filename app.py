import numpy as np
from flask import Flask, request, render_template, jsonify, redirect, session, url_for
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'
model = load_model('model.h5')

def preprocess_image(image_file):
    img = load_img(image_file, target_size=(300, 300))
    x = img_to_array(img)
    x /= 255
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    return images

@app.route('/')
def home():
    return render_template('Index.html')

@app.route('/upload',methods=['POST'])
def predict():
    if 'file' not in request.files:
        print('No image part')
    file = request.files['file']
    if file.filename == '':
        print('No selected file')
    if file:
        try:
            print("Hello world")
            img_path = secure_filename(file.filename)  # Secure the filename
            file.save(img_path)  # Save the file to the server
            img = preprocess_image(img_path)
            predictions = model.predict(img)
            if predictions[0] > 0.5:
                result_message = "The patient does have pneumonia"
                print("before redirect")
                return jsonify({'message': result_message})
            else:
                result_message = "The patient does not have pneumonia"
                return jsonify({'message': result_message})
        except Exception as e:
            return str(e)

@app.route('/result', methods=['GET', 'POST'])
def result():
    print("inside result")
    result_message = request.args.get('message', 'No result message')
    return render_template('Result.html', message=result_message)


if __name__ == "__main__":
    app.run(debug=True)
