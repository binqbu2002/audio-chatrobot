from pydub import AudioSegment
# Set the input and output file paths
input_file = "audio.wav"
output_file = "answer/audio.wav"

# Read the input audio file
audio = AudioSegment.from_wav(input_file)

# Set the output format to signed 16-bit little-endian, 2 channels, 16000 Hz
output_format = "wav"
output_codec = "pcm_s16le"
output_channels = 2
output_rate = 16000

# Export the audio in the desired format
audio.export(output_file,
             format=output_format,
             codec=output_codec,
             channels=output_channels,
             rate=output_rate,
             byteorder="little",
             endian="little")