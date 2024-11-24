from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import keras_ocr
from utils.utils import download_models, resize_image, save_file, remove_file
    
download_models()

detector = keras_ocr.detection.Detector(weights='clovaai_general')
recognizer = keras_ocr.recognition.Recognizer(
    weights='kurapan'
)
#cargar los modelos entrenados para reconocer los dígitos
detector.model.load_weights('./models/detector.h5')
recognizer.model.load_weights('./models/recognizer.h5')

pipeline = keras_ocr.pipeline.Pipeline(detector=detector, recognizer=recognizer)

USERS = [
    {'id': '1111', 'name': 'Brayan', 'phone': '+573144777544'},
    {'id': '2222', 'name': 'Juan', 'phone': '+573003333333'},
    {'id': '3333', 'name': 'Profe', 'phone': '+573004444444'}
]
CONVERSATIONS = {}

app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def bot():
    # Incoming Data
    incoming_msg = request.values.get('Body', '').lower()
    phone_number = request.values.get('From')
    resp = MessagingResponse()
    bot = BotProcessor(phone_number)

    if phone_number not in CONVERSATIONS:
        bot.user_status = 'initial_data'
        resp.message(bot.messages['initial_data'])
        return str(resp)
    
    # Handle incoming messages
    message = ''
    match bot.user_status:
        case 'initial_data':
            message = bot.process_initial_data(incoming_msg)
        case 'menu':
            message = bot.process_menu(incoming_msg)
        case 'send_image':
            message = bot.image_sent(incoming_msg, request)
        case 'back':
            message = bot.process_back(incoming_msg)

    # Back Button
    if bot.user_status not in ['initial_data', 'menu']:
        message += '\n\n' + bot.messages['back']

    # Response
    resp.message(message)
    return str(resp)

class BotProcessor:

    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.current_user = self.set_current_user()
        self.messages = {
            'initial_data': "¡Hola! Para empezar, ¿cuál es tu documento de identidad?",
            'back': '0. Volver al menú principal'
        }

    def set_current_user(self):
        return next((user for user in USERS if user['phone'] == self.phone_number), {})

    @property
    def user_status(self):
        return CONVERSATIONS.get(self.phone_number, 'initial_data')

    @user_status.setter
    def user_status(self, status):
        CONVERSATIONS[self.phone_number] = status

    def get_menu(self):
        self.user_status = 'menu'
        return f'¡Hola {self.current_user.get("name", "")}! ¿Qué deseas hacer?\n1. Procesar imagen\n2. Consultar información\n3. Actualizar datos'

    def process_initial_data(self, incoming_message):
        if incoming_message not in [user['id'] for user in USERS]:
            message = "Documento no encontrado. Ingresalo nuevamente"
        else:
            self.current_user = next(user for user in USERS if user['id'] == incoming_message)
            message = self.get_menu()
        return message

    def process_menu(self, incoming_message):
        match incoming_message:
            case '1':
                self.user_status = 'send_image'
                message = "Por favor envía la imagen que deseas procesar."
            case '2':
                self.user_status = 'back'
                message = "'Consulta de información' aún no implementada."
            case '3':
                self.user_status = 'back'
                message = "'Actualización de datos' aún no implementada."
            case _:
                message = "Opción no válida."
        return message

    def process_back(self, incoming_message):
        if incoming_message == '0':
            message = self.get_menu()
        else:
            message = "Opción no válida."
        return message

    def image_sent(self, incoming_message, request):
        print("procesando imagen")
        # Back Button
        if incoming_message == '0':
            return self.get_menu()

        # Process image
        num_media = int(request.values.get("NumMedia"))
        if num_media == 0:
            return "Por favor envía una imagen."

        # Process the received image
        media_url = request.form.get('MediaUrl0')
        media_type = request.form.get('MediaContentType0')

        img_filename = save_file(media_url, media_type)

        if not img_filename:
             return "Por favor envía una imagen valida!." 

        # Resize image (optional, based on your model's needs)
        resized_image = resize_image(img_filename)
        resized_image.save(img_filename)

        # Perform OCR
        images = [keras_ocr.tools.read(img_filename)]
        prediction_groups = pipeline.recognize(images)

        words = []
        for prediction in prediction_groups:
            for value, _ in prediction:
                words.append(value)

        remove_file(img_filename)
        print(words)
        data = [
            {'name': 'Diastolica', 'value': 'No se encontró'},
            {'name': 'Sistolica', 'value': 'No se encontró'},
            {'name': 'Pulso', 'value': 'No se encontró'}
        ]
        index = 0
        for string in words:
            # Break if we have found all the values
            if index > len(data):
                break

            # Check if the string is a number
            try:
                data[index]['value'] = int(string)
                index += 1
            except ValueError:
                continue
        
        # Prepare the response
        response = "Gracias por reportar tu información!\n"
        for item in data:
            response += f"\n{item['name']}: {item['value']}"

        response += "\n\nRecuerda volver mañana para reportar tus valores nuevamente."
        response += "Ten un buen día!"
        # Return the results
        return  response

if __name__ == '__main__':
    app.run(debug=True, port=8000)
