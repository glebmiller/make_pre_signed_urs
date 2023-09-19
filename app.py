from flask import Flask, request, jsonify
import uuid
import datetime

app = Flask(__name__)

UPLOAD_DIRECTORY = "/var/www/tutorial/upload"  # Replace with your desired storage location


def generate_presigned_url(file_name, expiration_minutes):
    unique_id = str(uuid.uuid4())
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)
    presigned_url = f"/upload/{unique_id}/{file_name}?expires={expiration.isoformat()}"
    return presigned_url


@app.route("/generate_presigned_url", methods=["POST"])
def generate_url():
    data = request.get_json()
    if "file_name" not in data or "expiration_minutes" not in data:
        return jsonify({"error": "Invalid request"}), 400

    file_name = data["file_name"]
    expiration_minutes = int(data["expiration_minutes"])

    presigned_url = generate_presigned_url(file_name, expiration_minutes)

    return jsonify({"presigned_url": presigned_url})


@app.route("/upload/<unique_id>/<file_name>", methods=["PUT"])
def upload_file(unique_id, file_name):
    # Handle the PUT request and file upload logic here
    # You can access the uploaded file data using request.data
    # Validate the pre-signed URL and expiration time before processing the upload
    # You should also save the uploaded file to the specified directory
    # Return an appropriate response

    # Example: Save the uploaded data to a file
    with open(f"{UPLOAD_DIRECTORY}/{file_name}", "wb") as f:
        f.write(request.data)

    return jsonify({"message": "File uploaded successfully"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

