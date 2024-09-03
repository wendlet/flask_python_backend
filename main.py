from flask import Flask, request, send_from_directory, abort
import os
import cv2
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit the file size to 16MB
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    #if 'file' not in request.files:
        #return 'No file part', 400

    file1 = request.files['file1']
    file2 = request.files['file2']


    # If the user does not select a file, the browser may submit an empty part without a filename
    if file1.filename == '':
        return 'No selected file', 400

    # Check if the file is allowed (by extension)
    #if file1 and allowed_file(file1.filename):
        #filename = 'image.' + file.filename.rsplit('.', 1)[1].lower()
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
    file_path2 = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)
    file1.save(file_path)
    file2.save(file_path2)

    def template_matching(path1, path2):

        # Check if the paths exist
        if os.path.exists(path1):
            print(f"Path 1 exists: {path1}")
        else:
            print(f"Path 1 does not exist: {path1}")

        if os.path.exists(path2):
            print(f"Path 2 exists: {path2}")
        else:
            print(f"Path 2 does not exist: {path2}")

        # Load the source image and template image
        template_image = cv2.imread(path1)
        source_image = cv2.imread(path2)

        # Convert images to grayscale
        gray_source = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)
        gray_template = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

        # Get the width and height of the template
        w, h = gray_template.shape[::-1]

        # Perform template matching using cv2.matchTemplate
        res = cv2.matchTemplate(gray_source, gray_template, cv2.TM_CCOEFF_NORMED)

        # Set a threshold for matching
        threshold = 0.6
        loc = np.where(res >= threshold)

        # Draw rectangles around matched regions
        for pt in zip(*loc[::-1]):
            cv2.rectangle(source_image, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

        # Save the result
        cv2.imwrite("results/result.jpg", source_image)

    template_matching(file_path, file_path2)

    return f'File successfully uploaded and saved as {file1.filename}', 200

@app.route('/upload', methods=['GET'])
def download_file():
    try:
        # Sende die Datei aus dem Verzeichnis zurück
        return send_from_directory("results", "result.jpg", as_attachment=True)
    except FileNotFoundError:
        abort(404, description=f"Datei nicht gefunden.")



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)





