from flask import Flask, render_template, redirect, url_for, flash, session, request
import gmplot
import googlemaps
import re
import os
from models import Conductor, RegisterForm
import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
apikey = os.getenv('API_KEY')
gmap = gmplot.GoogleMapPlotter(lat=6.2442, lng=-75.5814, zoom=10, apikey=apikey)
gmaps = googlemaps.Client(key=apikey)

def obtener_coordenadas(direccion):
    try:
        # Llama a la API de geocodificación para obtener las coordenadas
        geocode_result = gmaps.geocode(direccion)
        
        # Extrae las coordenadas desde el resultado de geocodificación
        location = geocode_result[0]['geometry']['location']
        latitud = location['lat']
        longitud = location['lng']
        
        return latitud, longitud
    except Exception as e:
        print(f"Error al obtener coordenadas para '{direccion}': {e}")
        return None

@app.route("/", methods=['GET', 'POST'])
def home_page():
    form = RegisterForm()
    if form.validate_on_submit:
        origen_direccion = form.origen.data 
        destino_direccion = form.destino.data
        if origen_direccion != destino_direccion:
            # Almacenar datos en la sesión
            session['origen'] = origen_direccion
            session['destino'] = destino_direccion
            return redirect(url_for('conductor_page'))
        else:
            flash('El origen y el destino no pueden ser iguales', category='danger')

    return render_template('home.html', form=form)

@app.route("/conductor", methods=['GET', 'POST'])
def conductor_page():

    origen_direccion = session.get('origen', None)
    destino_direccion = session.get('destino', None)

    distancia = gmaps.directions(origen_direccion,destino_direccion)

    km_distance = (distancia[0]['legs'][0]['distance']['text'])
    horas_minutos_duracion = (distancia[0]['legs'][0]['duration']['text'])
    
    numero_km = float(re.search(r'\d+\.\d+', km_distance).group())

    conductor1 = Conductor('Gustavo Montoya',1.25)
    conductor2 = Conductor('Jairo Restrepo', 2)
    conductor3 = Conductor('Elkin Soto', 1)

    conductores = [conductor1,conductor2,conductor3]
  
    return render_template('conductor.html', 
                           origen=origen_direccion, 
                           destino=destino_direccion,
                           km_distance=km_distance,
                           horas_minutos_duracion=horas_minutos_duracion,
                           numero_km = numero_km,
                           conductores = conductores)

@app.route("/mapa", methods=['GET', 'POST'])
def mapa_page():
    origen_direccion = session.get('origen', None)
    destino_direccion = session.get('destino', None)
    
    origen = obtener_coordenadas(origen_direccion)
    destino = obtener_coordenadas(destino_direccion)

    gmap.marker(origen[0], origen[1], color='blue', title='Origen')
    gmap.marker(destino[0], destino[1], color='red', title='Destino')

    ruta_coords = gmap.directions(origen, destino)

    ruta_archivo = 'templates/mapa_ruta.html'

    load_dotenv()

    remitente = os.getenv('REMITENTE')
    contraseña = os.getenv('CONTRASENA')
    destinatario = request.form.get('correo')
    asunto = 'Factura UberUdem'
    boton_aceptar = request.form.get('aceptar')

    if boton_aceptar and destinatario:
        conductor_name, conductor_tarifa = boton_aceptar.split('|')

        mensaje_texto = f'''Hola estimado usuario, esta es tu factura de viaje. 🚗✨

        Detalles del viaje:
        - Origen: {origen_direccion}
        - Destino: {destino_direccion}
                        

        Tu conductor fue: 🚖 {conductor_name}
        Costo del viaje: 💲 {conductor_tarifa}

        ¡Gracias por elegir nuestro servicio! 🌟
        '''

        msg = MIMEText(mensaje_texto)
        msg['From'] = remitente
        msg['Subject'] = asunto
        msg['To'] = destinatario

        # Configurar el servidor SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, contraseña)

        # Enviar el mensaje
        server.sendmail(remitente, destinatario, msg.as_string())

        # Cerrar la conexión con el servidor
        server.quit()
    
    # Borra el archivo HTML existente
    if os.path.exists(ruta_archivo):
        os.remove(ruta_archivo)

    # Dibuja las rutas en el nuevo archivo HTML
    gmap.draw(ruta_archivo)   
    return render_template('mapa_ruta.html')


if __name__ == '__main__':
    app.run(debug=True)
