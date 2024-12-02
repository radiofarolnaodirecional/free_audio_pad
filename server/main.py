from flask import Flask, render_template, request
from extensions import init_exetensions, db
from models import Tracks
from api import bp
from funcs.audio_devices import get_audio_devices
from sqlalchemy import func
import os
import shutil
import uuid
from pathlib import Path
from utils.find_free_port import find_free_port

server = Flask(__name__, template_folder='../ui/templates', static_folder='../ui/static')
server.config.from_pyfile('config.py')
init_exetensions(server)
server.register_blueprint(bp)

@server.route('/')
def home():
    return render_template('index.html')

@server.route('/index-content', methods=['POST'])
def home_content():
    devices = get_audio_devices()
    inputs = devices['inputs']
    if 'CABLE Output (VB-Audio Virtual Cable)' in inputs:
        inputs.append('CABLE Input (VB-Audio Virtual Cable)')
    outputs = devices['outputs']
    return render_template('index_content.html', inputs=inputs, outputs=outputs)

@server.route('/track-list', methods=['POST'])
def track_list():
    tracks = db.session.execute(db.select(Tracks)).scalars()
    track_count = db.session.execute(db.select(func.count(Tracks.id))).scalar()
    return render_template('index_tracklist.html', tracks=tracks, track_count=track_count)


def save_img(url: str) -> str:
    # Diretório base para salvar as imagens
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ui", "static", "img", "client"))

    # Garante que o diretório existe
    os.makedirs(base_dir, exist_ok=True)

    # Gera um nome único para o arquivo de destino
    file_name = f"{uuid.uuid4()}{Path(url).suffix}"  # Mantém a extensão original do arquivo
    destination_path = os.path.join(base_dir, file_name)

    # Copia o arquivo para o destino
    shutil.copyfile(url, destination_path)

    destination_path_static = destination_path.replace("\\", "/").split('img/')[1]
    return destination_path_static  # Retorna o caminho completo da imagem salva

@server.route('/add-track', methods=['POST'])
def add_track():
    data = request.get_json()
    track_name, track_tag, track_url, track_img = data.get('track_name') if data.get('track_name') != '' or None else 'unnamed', data.get('track_tag') if data.get('track_tag') != '' or None else 'untagged', data.get('track_url').replace("\\", "/"), save_img(data.get('track_img').replace("\\", "/")) if data.get('track_img') != 'no file selected (optional)' else None
    track = Tracks(name=track_name, tag=track_tag, url=track_url, img_url=track_img)
    db.session.add(track)
    db.session.commit()
    return 'add'

if __name__ == "__main__":
    with server.app_context():
        db.create_all()
    port = find_free_port()
    print(f'PORT={port}')
    server.run(port=port)
