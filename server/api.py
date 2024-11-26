from flask import Blueprint, request, jsonify
from funcs.play_audio import AudioPlayer
from funcs.mic_interface import MicInterface
from models import db, Usercfg, Tracks
import os
import signal
import time

bp = Blueprint('api', __name__)

player = AudioPlayer()
def play(device, url, volume):
    player.initialize_mixer(device)
    player.load_audio(url)
    player.set_volume(volume)
    player.play_in_thread()

mi = MicInterface()

# "CABLE Input (VB-Audio Virtual Cable)"
@bp.route('/play-audio', methods=['POST'])
def api_play_audio():
    cfg = db.session.execute(db.select(Usercfg)).scalar_one_or_none()
    data = request.get_json()
    url = data.get('url')
    device_in_or_out = data.get('device')
    device = None
    volume = None
    if device_in_or_out == 'in':
        device = cfg.in_device
        volume = cfg.vol_in / 100
    elif device_in_or_out == 'out':
        device = cfg.out_device
        volume = cfg.vol_out / 100
    play(device, url, volume)
    return 'played'

@bp.route('/start-audio-stream', methods=['POST'])
def start_audio_stream():
    cfg = db.session.execute(db.select(Usercfg)).scalar_one_or_none()
    if not cfg:
        cfg = Usercfg(mic_on=True)
        db.session.add(cfg)
    else:
        cfg.mic_on = not cfg.mic_on

    aud_err = None
    if cfg.mic_on:
        aud_err = mi.set_device(cfg.in_device)
        mi.start_audio_stream()

    else:
        mi.stop_audio_streaming()

    db.session.commit()
 
    return jsonify({"mic": cfg.mic_on, "audio_stream": aud_err})

@bp.route('/get-config', methods=['POST'])
def get_config():
    cfg = db.session.execute(db.select(Usercfg)).scalar_one_or_none()
    if not cfg:
        cfg = Usercfg()
        db.session.add(cfg)
        db.session.commit()

    return jsonify({
        "in_device": cfg.in_device,
        "out_device": cfg.out_device,
        "show_img": cfg.show_img,
        "show_track_details": cfg.show_track_details,
        "mic_on": cfg.mic_on,
        "vol_in": cfg.vol_in,
        "vol_out": cfg.vol_out
    })

@bp.route('/set-volume', methods=['POST'])
def set_volume():
    data = request.get_json()
    vol_inr = data.get('vol_in')
    vol_outr = data.get('vol_out')
    cfg = db.session.execute(db.select(Usercfg)).scalar_one_or_none()
    cfg.vol_in = vol_inr
    cfg.vol_out = vol_outr
    db.session.commit()
    return 'v'

@bp.route('/set-inputdev', methods=['POST'])
def set_indev():
    data = request.get_json()
    device = data.get('device')
    cfg = db.session.execute(db.select(Usercfg)).scalar_one_or_none()
    cfg.in_device = device
    db.session.commit()
    return 'input set'
@bp.route('/set-outputdev', methods=['POST'])
def set_outdev():
    data = request.get_json()
    device = data.get('device')
    cfg = db.session.execute(db.select(Usercfg)).scalar_one_or_none()
    cfg.out_device = device
    db.session.commit()
    return 'output set'

@bp.route('/delete-track', methods=['DELETE'])
def delete_track():
    data = request.get_json()
    track_id = data.get('track_id')
    track = db.session.execute(db.select(Tracks).filter_by(id=track_id)).scalar_one_or_none()
    if track:
        db.session.delete(track)
        db.session.commit()
    return 'deleted'

@bp.route('/close-server', methods=['POST'])
def close_server():
    cfg = db.session.execute(db.select(Usercfg)).scalar_one_or_none()
    cfg.mic_on = False
    db.session.commit()
    os.kill(os.getpid(), signal.SIGINT)
    return '.'
