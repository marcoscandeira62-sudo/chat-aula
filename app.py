import os
from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_123'
# permitimos conexiones desde cualquier origen para que funcione online
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    # 'data' contiene el nombre y el texto enviado desde el navegador
    print(f"Mensaje: {data}")
    send(data, broadcast=True)

if __name__ == '__main__':
    # Usamos el puerto que asigne Render o el 5000 por defecto localmente
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
