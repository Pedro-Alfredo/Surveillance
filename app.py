from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio
from queue import Queue
from modules.risk_module import calcular_risco
from modules.video_module import iniciar_video_thread

app = FastAPI()
event_queue = Queue()
connected_clients = []

# Inicia thread de vídeo
iniciar_video_thread(0)  # 0 = webcam local

@app.get("/")
async def dashboard():
    with open("static/dashboard.html") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except:
        connected_clients.remove(websocket)

async def enviar_alerta_web(alerta):
    for client in connected_clients:
        try:
            await client.send_text(alerta)
        except:
            connected_clients.remove(client)

async def processar_eventos():
    while True:
        if not event_queue.empty():
            evento = event_queue.get()
            score = calcular_risco(evento)
            alerta = f"ALERTA: Evento crítico! Score {score:.2f}" if score > 0.5 else f"Evento baixo risco {score:.2f}"
            print(alerta)
            await enviar_alerta_web(alerta)
        await asyncio.sleep(0.5)

# Exemplo de adicionar eventos manualmente
def simular_eventos():
    import time, random
    while True:
        event_queue.put({'tempo': random.randint(1,10), 'local_cameras': random.randint(0,5),
                         'online_posts': random.randint(0,5), 'texto': 'Post de teste'})
        time.sleep(2)

import threading
threading.Thread(target=simular_eventos, daemon=True).start()
asyncio.create_task(processar_eventos())
