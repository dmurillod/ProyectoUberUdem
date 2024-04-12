# Proyecto Simulador de Uber 🚗💨
Este proyecto simula una aplicación similar a Uber, donde los usuarios pueden ingresar un origen y destino, ver detalles del viaje como tiempo estimado y distancia, y seleccionar entre varios conductores disponibles para realizar el viaje. La aplicación utiliza la API de Google Maps 🗺️ para mostrar la ruta del viaje y enviar la factura del viaje al correo electrónico del usuario.

# Requisitos 📋
Antes de ejecutar este proyecto, necesitarás generar una API Key de Google Maps y agregarla al archivo de configuración correspondiente. Sigue los pasos a continuación para obtener una API Key:

1. Crea un proyecto en Google Cloud Platform:
   -Ve a Google Cloud Platform.
   -Crea un nuevo proyecto.

2. Habilita la API de Google Maps:

En el panel de control del proyecto, selecciona "API y servicios" y luego "Biblioteca".
Busca y selecciona "Google Maps JavaScript API".
Haz clic en "Habilitar".

# Genera una API Key:

En el panel de control del proyecto, selecciona "API y servicios" y luego "Credenciales".
Haz clic en "Crear credenciales" y selecciona "Clave de API".
Copia la API Key generada y asegúrate de restringirla solo para el uso con la API de Google Maps.
Agrega la API Key al proyecto:

Copia la API Key generada y agrégala al archivo de configuración config.py del proyecto.
