curl -X POST -F "file=@audio.wav" http://18.132.153.117:5000/upload
rm -rf ./audio.wav
cd answer & curl -OJ http://18.132.153.117:5000/download/audio.wav