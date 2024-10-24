# TensiBot

**TensiBot** es una aplicación desarrollada para la **Fundación Santafé** que permite a las personas mayores enviar fotos de sus lecturas de tensiómetro a un chatbot de **WhatsApp**. Utiliza inteligencia artificial para reconocer los números en las imágenes y almacenarlos automáticamente, facilitando el monitoreo de la presión arterial y promoviendo la autonomía de los usuarios.

## Tecnologías utilizadas

- **Flask**: Framework para construir aplicaciones web en Python.
- **Twilio**: API para enviar y recibir mensajes a través de WhatsApp.
- **TensorFlow**: Biblioteca de código abierto para el aprendizaje automático.
- **Keras OCR**: Herramienta para el reconocimiento óptico de caracteres en imágenes.
- **Heroku**: Plataforma como servicio para implementar aplicaciones en la nube.

## Instalación

1. Clona este repositorio:

   ```bash
   git clone https://github.com/tu_usuario/tensibot.git
   ```

2. Navega al directorio del proyecto:

   ```bash
   cd tensibot
   ```

3. Crea un entorno virtual y actívalo:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   ```

4. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```


   ```

## Uso

1. Inicia el servidor Flask localmente:

   ```bash
   python app.py
   ```

2. Envía una imagen de tu lectura de tensiómetro al chatbot de WhatsApp y espera la respuesta.

3. Si has desplegado en Heroku, simplemente envía un mensaje al número configurado.

## Licencia

Este proyecto está bajo la licencia MIT.