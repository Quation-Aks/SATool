import requests
import json

# Replace these with the actual URLs of your API endpoints
data_url = "http://localhost:5000/api/data/CTA_Meghana_Foods.csv"
images_url = "http://localhost:5000/api/images"
list_files_url = "http://localhost:5000/api/list_files"

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
        # Save the received zip file
        with open("received_images.zip", "wb") as f:
            f.write(response.content)
        print("Zip file saved successfully.")
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
