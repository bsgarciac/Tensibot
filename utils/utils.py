import os
import gdown
from PIL import Image
import requests

# Access variables
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

MODELS = [
   {'name': 'detector.h5', 'url': 'https://drive.google.com/uc?id=1v4t-YZUhspSY48PMibRnlzjNVYuAPAPT'},
   {'name': 'recognizer.h5', 'url': 'https://drive.google.com/uc?id=1HglRWLUaSc5i2bDsAMY8MiKKJtHmG6y6'}
] 

def download_models():
    # Ensure the "models" folder exists
    models_folder = "models"
    if not os.path.exists(models_folder):
        os.makedirs(models_folder)
        print(f"Created folder: {models_folder}")

    # Download the models
    for model in MODELS:
        model_path = f"models/{model['name']}"
        if not os.path.exists(model_path):
            print("Downloading model...")
            gdown.download(model['url'], model_path, quiet=False)

def resize_image(image_path, max_width=833, max_height=800):
    # Abre la imagen
    image = Image.open(image_path)
    original_width, original_height = image.size

    # Calcula la relación de escalado necesaria
    width_ratio = max_width / original_width
    height_ratio = max_height / original_height
    scale_ratio = min(width_ratio, height_ratio)

    if scale_ratio < 1:
      # Calcula el nuevo tamaño basado en la escala
      new_width = int(original_width * scale_ratio)
      new_height = int(original_height * scale_ratio)

      # Redimensiona la imagen
      resized_image = image.resize((new_width, new_height), Image.LANCZOS)

      return resized_image
    else:
      print('Imagen se mantiene')

      return image
    

def save_file(media_url, content_type):
    from base64 import b64encode

    # Prepare the basic authentication header
    auth_str = f"{ACCOUNT_SID}:{AUTH_TOKEN}"
    auth_bytes = auth_str.encode('utf-8')
    auth_b64 = b64encode(auth_bytes).decode('utf-8')
    headers = {'Authorization': 'Basic ' + auth_b64}

    # Make the request
    r = requests.get(media_url, headers=headers)
    filename = None

    if content_type == 'image/jpeg':
        filename = f'image.jpg'
    elif content_type == 'image/png':
        filename = f'image.png'

    if filename:
      with open(filename, 'wb') as f:
        f.write(r.content)
    return filename

def remove_file(file_path):
    if os.path.exists(file_path):
      os.remove(file_path)
      print(f"{file_path} has been deleted.")
    else:
        print(f"{file_path} does not exist.")