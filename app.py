from flask import Flask, render_template, request, send_from_directory, url_for
import os
import time
from pydub import AudioSegment, silence

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    audio_data = request.files['audio_data']
    audio_data.save('audio.wav')
    return 'OK'



# @app.route('/upload', methods=['POST'])
# def upload():
#     audio_data = request.files['audio_data']
#     audio_path = os.path.join('.', 'audio.wav')
#     audio_data.save(audio_path)
#
#     # Load the audio file
#     audio = AudioSegment.from_wav(audio_path)
#
#     # Detect silence and split the audio
#     silent_ranges = silence.detect_silence(audio, min_silence_len=2000, silence_thresh=-40)
#     silent_ranges = [(start, end) for start, end in silent_ranges if end - start > 2000]
#
#     if silent_ranges:
#         start, end = silent_ranges[0]
#         split_audio = audio[:start]
#         split_audio.export(audio_path, format='wav')
#
#     return ('', 204)



@app.route('/audio/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory='.', path=filename)

@app.route('/fetch_music', methods=['GET'])
def fetch_music():
    # Replace 'path/to/music/file.mp3' with the actual path to your music file
    print("ask GPT")
    os.system('curl -X POST -F \"file=@audio.wav\" http://18.132.153.117:5000/upload')
    os.system('rm -rf ./audio.wav')
    os.system('curl -OJ http://18.132.153.117:5000/download/audio.wav')

    music_file_path = './audio.wav'
    output_path = './audio.wav'

    # Convert the audio file to 16kHz
    audio = AudioSegment.from_file(music_file_path)
    converted_audio = audio.set_frame_rate(16000)
    converted_audio.export(output_path, format='wav')

    return send_from_directory(directory='.', path='audio.wav')


if __name__ == '__main__':
    app.run(debug=True)
