import requests
import json
import os
import base64
import apikey
import argparse

# Fetch Api Key
api_key = apikey.key

url = "https://api.wizmodel.com/sdapi/v1/img2img"

# Arguments for Generating Images
parser = argparse.ArgumentParser(description="Generate Images with inspiration drawn from a given image using Wizmodel's Stable Diffusion API.")

parser.add_argument('--prompt', help='the prompt is the description of the image to be generated, default="painting"')
parser.add_argument('--image', help='path to image, default="sample.jpg"')
parser.add_argument('--amount', help='amount of images to generate, default=4')
parser.add_argument('--steps', help='between 0 and 100, <20 low details, >20 and <25 image reaches high quality, >25 more detailed, default=25')
parser.add_argument('--cfg', help='between 1 and 30, 1 for maximum deviation/creativity from prompt, 30 for minimal deviation, default=7')
parser.add_argument('--remove', help='negative prompt i.e undesired characteristics to be removed, default=none')
parser.add_argument('--denoise', help='denoise is a value between 0 and 1, where 0 = exact image, where 1 = completly different, default = 0.40')

args = parser.parse_args()

prompt = args.prompt
image_file_path = args.image 
amount = args.amount
steps = args.steps
cfg_scale = args.cfg
negative_prompt = args.remove
denoising_strength = args.denoise

# Check if Arguments are given and assign default if none
if not args.prompt:
    prompt = 'painting'

if not args.image:
    image_file_path = "sample.jpg"

if not args.amount:
    amount = 4

if not args.steps:
    steps = 25

if not args.cfg:
    cfg_scale = 7

if not args.remove:
    negative_prompt = ""

if not args.denoise:
    denoising_strength = 0.40

# Read and encode the image files
with open(image_file_path, "rb") as image_file:
    image_data = image_file.read()
    base64_data = base64.b64encode(image_data).decode("utf-8")

# Create the payload with local image data
payload = json.dumps(
    {
        "prompt": prompt,
        "init_images": [base64_data],
				"steps": steps,
				"cfg_scale": cfg_scale,
				"negative_prompt": negative_prompt,
				"denoising_strength": denoising_strength,
    }
)

headers = {"Content-Type": "application/json", "Authorization": "Bearer " + api_key}

response = requests.request("POST", url, headers=headers, data=payload)

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

