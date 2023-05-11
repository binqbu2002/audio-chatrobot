from flask import Flask, render_template, jsonify, request, send_file, send_from_directory
from pydub import AudioSegment
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/audio.wav')
def serve_audio():
    print("ask GPT")
    os.system('curl -X POST -F \"file=@audio.wav\" http://18.132.153.117:5000/upload')
    os.system('rm -rf ./audio.wav')
    os.system('curl -OJ http://18.132.153.117:5000/download/audio.wav')

    # music_file_path = './audio.wav'
    # output_path = './audio.wav'
    #
    music_file_path = './audio.wav'
    output_path = './audio.wav'
    #
    # Convert the audio file to 16kHz
    audio = AudioSegment.from_file(music_file_path)
    converted_audio = audio.set_frame_rate(16000)
    converted_audio.export(output_path, format='wav')


    return send_from_directory(directory='.', path='audio.wav')

@app.route('/music_play', methods=['GET'])
def music_play():
    # ... your code here to select the music file ...
    # return the URL of the music file
    url = "./audio.wav"
    return jsonify({'url': url})

@app.route('/record', methods=['POST'])
def record():
    audio_file = request.files['audio_data']
    file_path = 'recorded_audio.webm'
    audio_file.save(file_path)

    # Convert the webm file to a wav file using pydub
    webm_audio = AudioSegment.from_file(file_path, format='webm')
    wav_file_path = 'audio.wav'
    webm_audio = webm_audio.set_frame_rate(16000)
    webm_audio.export(wav_file_path, format='wav')

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

    return send_file(wav_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
