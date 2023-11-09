import requests
import json
import os
import base64
import apikey
import argparse

# Fetch Api Key
api_key = apikey.key

url = "https://api.wizmodel.com/sdapi/v1/img2img"

# Local image file paths
image_file_path = "sample.jpg"

# Read and encode the image files
with open(image_file_path, "rb") as image_file:
    image_data = image_file.read()
    base64_data = base64.b64encode(image_data).decode("utf-8")

# Create the payload with local image data
payload = json.dumps(
    {
        "prompt": "painting",
        "init_images": [base64_data],
    }
)

headers = {"Content-Type": "application/json", "Authorization": "Bearer " + api_key}

response = requests.request("POST", url, headers=headers, data=payload)

amount = 4
# Send requests for the number of images requested
for i in range(int(amount)):
    print(f"[-] Generating {i+1} image out of {amount} images")
    response = requests.request("POST", url, headers=headers, data=payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        try:
            # Get the list of image data from the JSON response
            response_json = response.json()
            image_data_list = response_json.get("images")

            # Check if image data is present
            if image_data_list:
                # Decode the base64 image data
                image_data = base64.b64decode(image_data_list[0])

                # Save each image to a file
                image_filename = f"generated_image_{i + 1}.png"
                with open(image_filename, "wb") as image_file:
                    image_file.write(image_data)
                print(f"[-] Image {i + 1} saved as '{image_filename}'")
            else:
                print("Image data list not found in the response JSON.")
        except json.JSONDecodeError:
            print("Error decoding JSON response.")
    else:
        print("Error:", response.status_code, response.text)

