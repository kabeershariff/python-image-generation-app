import requests
import json
import os
import base64
import apikey
import argparse

# Fetch API key
api_key = apikey.key

url = "https://api.wizmodel.com/sdapi/v1/txt2img"

# Arguments for Generating Images
parser = argparse.ArgumentParser(description="Generate Images using Wizmodel's Stable Diffusion API.")

parser.add_argument('--prompt', help='the prompt is the description of the image to be generated, default="flowers"')
#parser.add_argument('--batch', help='the number of images to generate, default=1')
parser.add_argument('--steps', help='between 0 and 100, <20 low details, >20 and <25 image reaches high quality, >25 more detailed, default=25')
parser.add_argument('--remove', help='negative prompt i.e undesired characteristics to be removed')
parser.add_argument('--amount',help='amount of images to generate')

args = parser.parse_args()

prompt = args.prompt
batch_size = 1
steps = args.steps
negative_prompt = args.remove
amount = args.amount

# Check if Arguments are given and assign default if none
if not args.prompt:
    prompt = 'flowers'

#if not args.batch:
#    batch_size = 1

if not args.steps:
    steps = 25

if not args.remove:
    negative_prompt = ""

if not args.amount:
    amount = 4


payload = json.dumps({
    "prompt": prompt,
    "steps": steps,
    "batch_size": batch_size,
    "negative_prompt" : negative_prompt,
})

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + api_key
}

#Send requests for the number of images requested, since batch_size no longer works
for i in range(int(amount)):
    print(f'[-]Generating {i+1} image out of {amount} images')
    response = requests.request("POST", url, headers=headers, data=payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        try:     
            # Get the list of image data from the JSON response
            response_json = response.json()
            image_data_list = response_json.get('images')

            # Check if image data is present
            if image_data_list:
                # Decode the base64 image data
                image_data = base64.b64decode(image_data_list[0])

                # Save each image to a file
                image_filename = f"generated_image_{i + 1}.png"
                with open(image_filename, "wb") as image_file:
                    image_file.write(image_data)
                print(f"[-]Image {i + 1} saved as '{image_filename}'")
            else:
                print("Image data list not found in the response JSON.")
        except json.JSONDecodeError:
            print("Error decoding JSON response.")
    else:
        print("Error:", response.status_code, response.text)

