from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)

USERS = [
    {'id': '1111', 'name': 'Brayan', 'phone': '+573144777544'},
    {'id': '2222', 'name': 'Pedro', 'phone': '+573003333333'},
    {'id': '3333', 'name': 'María', 'phone': '+573004444444'}
]
CONVERSATIONS = {}

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
        # Back Button
        if incoming_message == '0':
            return self.get_menu()
        
        # Process image
        num_media = int(request.values.get("NumMedia"))
        if num_media == 0:
            return "Por favor envía una imagen."
        
        # Procesar la imagen recibida
        media_url = request.values.get("MediaUrl0")
        media_type = request.values.get("MediaContentType0")
        
        # Descarga la imagen
        img_data = requests.get(media_url).content
        img_filename = f"image_received.{media_type.split('/')[1]}"
        
        # Guardar temporalmente la imagén
        with open(img_filename, 'wb') as handler:
            handler.write(img_data) 

        # Respuesta a la imagen recibida
        return "Tus resultados son:"


@app.route('/test', methods=['GET'])
def test_route():
    return "GET request received! The server is working."

if __name__ == '__main__':
    app.run(debug=True, port=8000)
