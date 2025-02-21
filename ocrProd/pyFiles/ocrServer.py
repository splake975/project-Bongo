import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs
import easyocr
import cv2
import numpy as np
from io import BytesIO
import requests
import os
from PIL import Image
import base64

# Initialize EasyOCR reader
reader = easyocr.Reader(["en"])

def remove_transparency(image):
    """
    Remove transparency from an image by compositing it onto a white background.
    """
    if image.mode in ("RGBA", "LA"):
        background = Image.new("RGB", image.size, (255, 255, 255))  # White background
        background.paste(image, mask=image.split()[-1])  # Paste image using alpha channel as mask
        return background
    else:
        return image

# def load_image_from_data_uri(data_uri):
#     """
#     Load an image from a data URI.
#     """
#     # Extract the base64-encoded image data
#     header, encoded = data_uri.split(",", 1)
#     image_data = base64.b64decode(encoded)

#     # Load the image using PIL
#     image = Image.open(BytesIO(image_data))
#     return image

def load_image_from_data_uri(data_uri):
    """
    Load an image from a data URI.
    """
    if "," not in data_uri:
        raise ValueError("Invalid data URI format")

    header, encoded = data_uri.split(",", 1)
    image_data = base64.b64decode(encoded)

    image = Image.open(BytesIO(image_data))
    return image

def get_bounding_box(results):
    """
    Calculate the bounding box of all detected text.
    """
    if not results:
        return None

    # Initialize min and max coordinates
    min_x = min_y = float("inf")
    max_x = max_y = float("-inf")

    for result in results:
        # Extract the bounding box coordinates
        (top_left, top_right, bottom_right, bottom_left) = result[0]
        # Update min and max coordinates
        min_x = min(min_x, top_left[0], bottom_left[0])
        min_y = min(min_y, top_left[1], top_right[1])
        max_x = max(max_x, top_right[0], bottom_right[0])
        max_y = max(max_y, bottom_left[1], bottom_right[1])

    return {
        "min_x": int(min_x),
        "min_y": int(min_y),
        "max_x": int(max_x),
        "max_y": int(max_y)
    }

class OCRRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the request path and query parameters
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        # Check if the 'image_uri' parameter is provided
        if "image_uri" not in query_params:
            self.send_json_error(400, json.dumps({"status": "error", "message": "Missing 'image_uri' parameter"}))
            return

        # Get the image URI from the query parameters
        image_uri = query_params["image_uri"][0]

        # Check if the 'bounding_box' parameter is provided
        bounding_box = query_params.get("bounding_box", [""])[0].lower() == "true"

        try:
            # Load the image based on the URI type
            if image_uri.startswith("data:"):
                # Handle data URI
                image = load_image_from_data_uri(image_uri)
            elif image_uri.startswith(("http://", "https://")):
                # Handle URL
                response = requests.get(image_uri)
                response.raise_for_status()
                image_data = BytesIO(response.content).read()
                image = Image.open(BytesIO(image_data))
            else:
                # Handle local file path (relative or absolute)
                if not os.path.isabs(image_uri):
                    # Convert relative path to absolute path
                    image_uri = os.path.abspath(image_uri)
                # Read the image
                with open(image_uri, "rb") as f:
                    image_data = f.read()
                image = Image.open(BytesIO(image_data))

            # Remove transparency by compositing onto a white background
            image = remove_transparency(image)

            # Convert the image to a NumPy array for OpenCV
            image = np.array(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR for OpenCV

            # Perform OCR on the image
            results = reader.readtext(image)

            # Prepare the response
            response = {"status": "success"}

            if bounding_box:
                # Calculate the bounding box of all text
                bounding_box_coords = get_bounding_box(results)
                if bounding_box_coords:
                    response["bounding_box"] = bounding_box_coords
                else:
                    response["bounding_box"] = None
            else:
                # Extract the OCR text
                ocr_text = " ".join([result[1] for result in results])
                response["ocr_text"] = ocr_text

            # Send the response as JSON
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))

        except FileNotFoundError:
            self.send_json_error(404, json.dumps({"status": "error", "message": "Image file not found"}))
        except Exception as e:
            # Handle other errors
            self.send_json_error(500, json.dumps({"status": "error", "message": f"Error processing image: {str(e)}"}))

    def send_json_error(self, status_code, message):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "error", "message": message}).encode("utf-8"))



def run_server(port=8000):
    # Start the HTTP server
    with socketserver.TCPServer(("", port), OCRRequestHandler) as httpd:
        print(f"Serving on port {port}...")
        httpd.serve_forever()

if __name__ == "__main__":
    # Run the server on port 8000
    run_server()

    # curl "http://localhost:8000/?image_uri=cache/globalpokercode.png&bounding_box=true"

    # curl "http://localhost:8000/?image_uri=cache/globalpokercode.png"

    # doesnt really work with base64 rn
        # untested base64 fix 2/19
    