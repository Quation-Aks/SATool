import os
import boto3
from flask import Flask, jsonify, request, send_file
import botocore
import csv
import io
import zipfile

app = Flask(__name__)

# Retrieve environment variables with default values
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID', 'AKIASDT5BINYALJ5M76J')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY', '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')
aws_region = os.environ.get('AWS_REGION', 'us-east-1')
aws_s3_bucket = os.environ.get('AWS_S3_BUCKET', 'twixorapi-bucket')

# Initialize the S3 client
s3 = boto3.client('s3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

# CSV Processor
def process_csv_data(csv_text, start_row, end_row):
    processed_data = []
    try:
        # Process CSV data
        csv_reader = csv.DictReader(io.StringIO(csv_text))
        for i, row in enumerate(csv_reader):
            if start_row <= i < end_row:
                processed_data.append(row)
            elif i >= end_row:
                break

        return processed_data

    except Exception as e:
        return None

# Data Endpoint for CSV files
@app.route('/api/data/<file_name>', methods=['GET'])
def get_data(file_name):
    try:
        # Retrieve start and end row parameters from the query string
        start_row = int(request.args.get('start_row', 0))
        end_row = int(request.args.get('end_row', 100))  # Default end_row value

        try:
            # Check if the file exists in the bucket
            s3_object = s3.get_object(Bucket=aws_s3_bucket, Key=f'data/{file_name}')
            file_extension = file_name.split('.')[-1]

            if file_extension == 'csv':
                # Process CSV data
                data_body = s3_object['Body'].read().decode('utf-8')
                processed_data = process_csv_data(data_body, start_row, end_row)

                if processed_data is not None:
                    return jsonify({"data": processed_data})
                else:
                    return jsonify({"error": "Failed to process data from the file"}), 500  # Return a 500 Internal Server Error status code

        except botocore.exceptions.ClientError as e:
            return jsonify({"error": "S3 operation failed", "details": str(e)}), 500  # Handle S3-related errors

        return jsonify({"error": "Unsupported file type"}), 400  # Return a 400 Bad Request for unsupported file types

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500  # Handle other unexpected errors

# Image Endpoint
@app.route('/api/images', methods=['POST'])
def get_images():
    # Parse JSON data from the request
    data = request.get_json()
    image_names = data.get('image_names', [])

    # Check if image names are provided
    if not image_names or len(image_names) != 2:
        return jsonify({"error": "Provide exactly 2 image names"})

    try:
        s3_resource = boto3.resource('s3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )

        # Create an in-memory zip file to store images
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            for image_name in image_names:
                # Download the image file from S3
                s3_key = f'images/{image_name}.jpg'
                s3_resource.meta.client.download_file(aws_s3_bucket, s3_key, image_name)
                zf.write(image_name)

        # Prepare the zip file for sending
        memory_file.seek(0)

        # Determine the appropriate file name for the zip
        zip_file_name = f'images.zip'

        # Return the zip file as an attachment
        return send_file(memory_file, as_attachment=True, download_name=zip_file_name)
    except botocore.exceptions.ClientError as e:
        # Handle S3-related errors
        return jsonify({"error": "S3 operation failed", "details": str(e)}), 500
    except Exception as e:
        # Handle other unexpected errors
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

# List Files Endpoint
@app.route('/api/list_files', methods=['GET'])
def list_files():
    try:
        s3 = boto3.client('s3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )

        # List files in the specified S3 bucket
        s3_objects = s3.list_objects(Bucket=aws_s3_bucket)

        # Extract file names from S3 objects
        file_list = [obj['Key'] for obj in s3_objects['Contents']]

        return jsonify({"files": file_list})
    except botocore.exceptions.ClientError as e:
        return jsonify({"error": "S3 operation failed", "details": str(e)}), 500  # Handle S3-related errors
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500  # Handle other unexpected errors

if __name__ == '__main__':
    app.run(debug=True)
