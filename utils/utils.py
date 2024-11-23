import os
import gdown
from PIL import Image

MODELS = [
   {'name': 'detector.h5', 'url': 'https://drive.google.com/uc?id=1v4t-YZUhspSY48PMibRnlzjNVYuAPAPT'},
   {'name': 'recognizer.h5', 'url': 'https://drive.google.com/uc?id=1HglRWLUaSc5i2bDsAMY8MiKKJtHmG6y6'}
] 

def download_models():
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