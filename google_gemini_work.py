from PIL import Image
import google.generativeai as genai
import json

genai.configure(api_key="AIzaSyCLPRDy8yXvcbpBu0LoMssojeO9yJaq3DI")


def parse_json_string_manual(json_string):
    try:
        # Remove triple quotes and 'json\n', then split by lines
        lines = json_string.strip("'''").split('json\n')[1].strip().split('\n')

        # Initialize an empty dictionary to hold the extracted values
        json_data = {}

        # Iterate through each line and extract key-value pairs
        for line in lines:
            # Strip whitespace and remove commas and quotes
            cleaned_line = line.strip().rstrip(',').replace("\"", "")

            # Split the line into key and value
            if ':' in cleaned_line:
                key, value = cleaned_line.split(':', 1)
                key = key.strip()
                value = value.strip()

                # Add to the dictionary
                json_data[key] = value

        # Return only the specific fields
        return { 
            "coupon_code": json_data.get("coupon_code")
        }
    except IndexError:
        return "Error: Incorrectly formatted string."


def parse_json_string(json_string):
    try:
        # Remove triple quotes and strip any whitespace
        cleaned_string = json_string.replace("```","").strip()

        # Extract the JSON part (after the word 'json')
        json_part = cleaned_string.split('json\n', 1)[1].strip()
        print(json_part)
        # Parse the JSON part
        json_data = json.loads(json_part)
        return json_data
    except IndexError:
        return parse_json_string_manual(json_string)
    except json.JSONDecodeError as e:
        return parse_json_string_manual(json_string)
# Configure the Google API


# Function to get a response from Gemini model
def get_gemini_response(input_text, image_path):
    model = genai.GenerativeModel('gemini-pro-vision')

    # Open the image file
    image_file = open(image_path, 'rb')
    image = Image.open(image_file)

    try:
        if input_text != "":
            response = model.generate_content([input_text, image])
        else:
            response = model.generate_content(image)
    finally:
        # Close the image file after processing
        image_file.close()
    print(response.text)
    print(type(response.text))
    return parse_json_string(response.text)

# Example usage
# input_text = "The picture is a parking ticket picture taken by a police person. I want the color,brand_name and license_number of the car in a json format. The american number plate will have american_state and license_number so add it in the response also ."
# image_path = "sample.jpg"

# response = get_gemini_response(input_text, image_path)
# print("The Response is:")
# print(response)
