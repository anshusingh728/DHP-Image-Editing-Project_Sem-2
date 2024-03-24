from flask import Flask, render_template, request, redirect, url_for, send_file
from PIL import Image, ImageEnhance, ImageFilter  # Import necessary modules
import io
import numpy as np
import cv2

app = Flask(__name__)

# Define image processing function using PIL
def process_image(image, operations):
    pil_image = Image.fromarray(image)  # Convert numpy array to PIL Image

    # Apply operations based on the selected features
    if 'blur' in operations:
        pil_image = pil_image.filter(ImageFilter.BLUR)
    if 'brightness' in operations:
        enhancer = ImageEnhance.Brightness(pil_image)
        pil_image = enhancer.enhance(1.5)  # Adjust brightness factor as needed
    if 'rotation' in operations:
        pil_image = pil_image.rotate(45)  # Adjust rotation angle as needed
    if 'crop' in operations:
        pil_image = pil_image.crop((100, 100, 300, 300))  # Adjust crop coordinates as needed
    if 'saturation' in operations:
        enhancer = ImageEnhance.Color(pil_image)
        pil_image = enhancer.enhance(1.5)  # Adjust saturation factor as needed
    if 'vintage' in operations:
        # Apply vintage effect 
        pass

    # Convert PIL Image back to numpy array for OpenCV compatibility
    image = np.array(pil_image)

    return image

# Flask route for the index page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'image' in request.files:
        image_file = request.files['image']
        nparr = np.fromstring(image_file.read(), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Perform image processing based on selected features
        operations = ['blur', 'brightness', 'rotation', 'crop', 'saturation', 'vintage']
        processed_image = process_image(image, operations)

        # Convert processed image to bytes for display and download
        _, buffer = cv2.imencode('.jpg', processed_image)
        buffer_io = io.BytesIO(buffer)
        buffer_io.seek(0)

        return render_template('index.html', processed_image_data=buffer_io.getvalue())

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




        
        

    

