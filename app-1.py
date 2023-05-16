from flask import Flask, render_template, jsonify, request, send_file, send_from_directory
from pydub import AudioSegment
import os
import requests
import time


def post_wav(wav_path):
    # files = {
    #     '"filename': open('audio.wav"', 'rb'),
    # }

    files = {'file': (wav_path, open('audio.mp3', 'rb'))}

    response = requests.post('http://18.132.153.117:5000/upload', files=files)

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
    # ... your code here to select the music file ...
    # return the URL of the music file
    print("ask GPT")
    # os.system('curl -X POST -F \"file=@audio.wav\" http://18.132.153.117:5000/upload')
    post_wav('audio.mp3')
    if os.path.exists('audio.mp3'):
        os.remove('audio.mp3')
    # os.system('rm -rf ./audio.wav')
    # os.system('curl -OJ http://18.132.153.117:5000/download/audio.wav')

    response = requests.get('http://18.132.153.117:5000/download/audio.mp3')

    music = response.content

    with open(r'audio.mp3', 'ab') as file:  # 保存到本地的文件名
        file.write(response.content)
        file.flush()

    # music_file_path = './audio.wav'
    # output_path = './audio.wav'
    #
    music_file_path = './audio.mp3'
    output_path = './audio.mp3'
    #
    # Convert the audio file to 16kHz
    audio = AudioSegment.from_file(music_file_path)
    converted_audio = audio.set_frame_rate(16000)
    converted_audio.export(output_path, format='mp3')
    url = "./audio.mp3"
    return jsonify({'url': url})

@app.route('/record', methods=['POST'])
def record():
    # os.system('rm -rf ./audio.wav')
    if os.path.exists('audio.mp3'):
        os.remove('audio.mp3')
    start = time.time()
    audio_file = request.files['audio_data']
    file_path = 'recorded_audio.webm'
    audio_file.save(file_path)

    # Convert the webm file to a wav file using pydub
    webm_audio = AudioSegment.from_file(file_path, format='webm')
    wav_file_path = 'audio.mp3'
    webm_audio = webm_audio.set_frame_rate(16000)
    webm_audio.export(wav_file_path, format='mp3')

    # Clean up temporary files
    os.remove(file_path)

    # audio_data = request.files['audio_data']
    # audio_path = os.path.join('./', 'audio.wav')
    # audio_data.save(audio_path)
    #
    # # Convert audio to WAV format with a sample rate of 16000 Hz
    # audio = AudioSegment.from_file(audio_path)
    # audio = audio.set_frame_rate(16000)
    # audio.export('audio.wav', format='wav')
    #
    end = time.time()
    print("the converting time is:")
    print(end - start)

    return send_file(wav_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 8200, debug=True)
