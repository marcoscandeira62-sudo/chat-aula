import os
import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template
from flask_socketio import SocketIO, send
from datetime import datetime
import random

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# Colores para usuarios
colors = ["#e6194b","#3cb44b","#ffe119","#4363d8","#f58231","#911eb4","#46f0f0","#f032e6"]

user_colors = {}  # nombre -> color

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("message")
def recibir_mensaje(msg):
    try:
        nombre, texto = msg.split(":",1)
    except ValueError:
        nombre = "Anonimo"
        texto = msg
    if nombre not in user_colors:
        user_colors[nombre] = random.choice(colors)
    hora = datetime.now().strftime("%H:%M")
    # Enviar diccionario a todos
    socketio.emit("message", {"nombre": nombre, "texto": texto, "hora": hora, "color": user_colors[nombre]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)

