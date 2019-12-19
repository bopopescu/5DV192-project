from flask import request
from werkzeug.utils import secure_filename

from . import app_google
from .views import GoogleBucket
from app_main.utils import json_response



@app_google.route('/upload', methods=['POST'])
def form_example():

    google_storage = GoogleBucket('umu-5dv192-project-eka')
    print(google_storage.list_buckets_names())


    if request.method == 'POST':

        file = request.files['file']
        form = request.form

        form_data = form.to_dict(flat=True)
        form_data.get("input-filename")

        print(file)
        print(form)

        if 'file' not in request.files:
            print('Error: no file found')
            return json_response({"error": "invalid file"}, 201)

        file = request.files['file']

        if file.filename == '':
            return json_response({"error": "invalid file name"}, 201)

        file.filename = secure_filename(file.filename)

        url = google_storage.upload_file(
            file.read(),
            file.filename,
            file.content_type
        )

        print(url)

        return json_response({"status": "success"}, 200)

    else:

        return json_response({"error": "invalid method"}, 201)
