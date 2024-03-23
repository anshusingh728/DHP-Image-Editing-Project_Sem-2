from flask import Flask, render_template, request, redirect, url_for, send_file
import cv2
import numpy as np
import io

app = Flask(__name__)

def process_image(image, operations):
    # Apply operations to the image
    # Example operations:
    if 'blur' in operations:
        image = cv2.GaussianBlur(image, (5, 5), 0)
    if 'brightness' in operations:
        image = cv2.convertScaleAbs(image, alpha=1.5, beta=50)
    return image

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'image' in request.files:
        image_file = request.files['image']
        nparr = np.fromstring(image_file.read(), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Perform image processing
        operations = ['blur', 'brightness']
        processed_image = process_image(image, operations)

        # Convert processed image to bytes for download
        _, buffer = cv2.imencode('.jpg', processed_image)
        buffer_io = io.BytesIO(buffer)
        buffer_io.seek(0)

        # Convert original image to bytes for displaying in HTML
        _, original_buffer = cv2.imencode('.jpg', image)
        original_image_data = original_buffer.tobytes()

        return render_template('index.html', image_data=original_image_data, processed_image_data=buffer_io.getvalue())

    return render_template('index.html')

# Other routes and functions remain the same

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        whatsapp = request.form['whatsapp']
        message = request.form['message']

        # Process form submission here, for example, send email
        # Redirect to success page after processing the form
        return redirect(url_for('success'))

    return render_template('contact.html')

@app.route('/success', methods=['GET'])
def success():
    return render_template('success.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/brightness')
def brightness():
    return render_template('brightness.html')

@app.route('/blur')
def blur():
    return render_template('blur.html')


@app.route('/rotation')
def rotation():
    return render_template('rotation.html')

@app.route('/crop')
def crop():
    return render_template('crop.html')

@app.route('/vintage')
def vintage():
    return render_template('vintage.html')

@app.route('/saturation')
def saturation():
    return render_template('saturation.html')

@app.route('/edit_page')
def edit():
    return render_template('index.html')

@app.route('/More_Feature')
def More_Feature():
    return render_template('More_Features.html')


if __name__ == '__main__':
    app.run(debug=True)

