from flask import Flask, render_template, jsonify, request, send_file, send_from_directory
from pydub import AudioSegment
import os
import aiohttp
import asyncio
import time
import requests

async def post_wav(wav_path):
    url = 'http://18.132.153.117:5000/upload'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data={'file': open(wav_path, 'rb')}) as response:
            print(response.status)
            print(await response.text())


app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/audio.mp3', methods=['GET', 'POST'])
def serve_audio():
    return send_from_directory(directory='.', path='audio.mp3')

@app.route('/music_play', methods=['GET'])
def music_play():
    print("ask GPT")
    asyncio.run(post_wav('audio.mp3'))

    if os.path.exists('audio.mp3'):
        os.remove('audio.mp3')

    response = requests.get('http://18.132.153.117:5000/download/audio.mp3')
    music = response.content

    with open(r'audio.mp3', 'ab') as file:
        file.write(response.content)
        file.flush()

    music_file_path = './audio.mp3'
    output_path = './audio.mp3'

    audio = AudioSegment.from_file(music_file_path)
    converted_audio = audio.set_frame_rate(16000)
    converted_audio.export(output_path, format='mp3')

    url = "./audio.mp3"
    return jsonify({'url': url})

@app.route('/record', methods=['POST'])
def record():
    if os.path.exists('audio.mp3'):
        os.remove('audio.mp3')
    start = time.time()
    audio_file = request.files['audio_data']
    file_path = 'recorded_audio.webm'
    audio_file.save(file_path)

    webm_audio = AudioSegment.from_file(file_path, format='webm')
    wav_file_path = 'audio.mp3'
    webm_audio = webm_audio.set_frame_rate(16000)
    webm_audio.export(wav_file_path, format='mp3')

    os.remove(file_path)

    end = time.time()
    print("the converting time is:")
    print(end - start)

    return send_file(wav_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8200, debug=True)
