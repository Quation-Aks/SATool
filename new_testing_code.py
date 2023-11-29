# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 16:01:28 2023

@author: Quation
"""

import requests
import json
import base64

# Replace these with the actual URLs of your API endpoints
data_url = "http://52.87.149.214/api/data/CTA_Meghana_Foods.csv"
images_url = "http://52.87.149.214/api/images"
list_files_url = "http://52.87.149.214/api/list_files"

# Example payload for the /api/images endpoint
images_payload = {
    "image_names": ["placeholder_graph_image2", "placeholder_graph_image"]
}

def test_data_endpoint():
    # Make a GET request to the /api/data endpoint
    response = requests.get(data_url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Process the response data (replace this with your processing logic)
        data = response.json()
        print("Data from /api/data endpoint:", data)
    else:
        print(f"Error: {response.status_code}\n{response.json()}")

def test_images_endpoint():
    # Make a POST request to the /api/images endpoint
    response = requests.post(images_url, json=images_payload)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Read the zip file and encode its content in base64
        base64_zip_data = base64.b64encode(response.content).decode('utf-8')

        # Save the base64-encoded zip content
        with open("received_images_base64.txt", "w") as base64_file:
            base64_file.write(base64_zip_data)
        print("Base64-encoded content saved successfully.")
    else:
        print(f"Error: {response.status_code}\n{response.json()}")

def test_list_files_endpoint():
    # Make a GET request to the /api/list_files endpoint
    response = requests.get(list_files_url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Process the response data (replace this with your processing logic)
        files = response.json()
        print("Files from /api/list_files endpoint:", files)
    else:
        print(f"Error: {response.status_code}\n{response.json()}")

if __name__ == "__main__":
    # Run the test functions
    test_data_endpoint()
    test_images_endpoint()
    test_list_files_endpoint()
