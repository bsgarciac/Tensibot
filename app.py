from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os
app = Flask(__name__)

# admin
# wrHS2aThDoAzKbZD

conversations = {}
messages = {
    'initial_data': "¡Hola! Para empezar, ¿cuál es tu documento de identidad?",
    'menu': """
Bienvenido! ¿En qué puedo ayudarte hoy?
1. Enviar imágenes para procesar
2. Consultar información
3. Actualizar mis datos
"""
}
users = [
    {'id': '1014302274', 'name': 'Brayan', 'phone': '+573144777544'},
    {'id': '2', 'name': 'Pedro', 'phone': '+573003333333'},
    {'id': '3', 'name': 'María', 'phone': '+573004444444'}
]
@app.route('/bot', methods=['POST'])
def bot():
    # Incoming Data
    incoming_msg = request.values.get('Body', '').lower()
    phone_number = request.values.get('From')
    resp = MessagingResponse()

    if phone_number not in conversations:
        conversations[phone_number] = 'initial_data'
        resp.message(messages['initial_data'])
        return str(resp)
    
    # Handle user data


    # Handle incoming messages
    if conversations[phone_number] == 'initial_data':
        message = process_initial_data(incoming_msg, phone_number)
    elif conversations[phone_number] == 'menu':
        message = process_menu(incoming_msg, phone_number)
    elif conversations[phone_number] == 'send_image':
        message = image_sent(request)

    # Response
    resp.message(message)
    return str(resp)

def process_initial_data(incoming_message, phone_number):
    if incoming_message not in [user['id'] for user in users]:
        message = "Documento no encontrado. Ingresalo nuevamente"
    else:
        conversations[phone_number] = 'menu'
        message = messages['menu']
    return message

def process_menu(incoming_message, phone_number):
    if incoming_message == '1':
        conversations[phone_number] = 'send_image'
        message = "Por favor envía la imagen que deseas procesar."
    elif incoming_message == '2':
        message = "'Consulta de información' aún no implementada."
    elif incoming_message == '3':
        message = "'Actualización de datos' aún no implementada."
    else:
        message = "Opción no válida." 
    return message

def image_sent(request):
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
    # Guardar la imagen temporalmente
    with open(img_filename, 'wb') as handler:
        handler.write(img_data) 

    # Respuesta a la imagen recibida
    return "Tus resultados son:"        


@app.route('/test', methods=['GET'])
def test_route():
    return "GET request received! The server is working."

if __name__ == '__main__':
    app.run(debug=True, port=8000)
