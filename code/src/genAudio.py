import subprocess

def generate_audio(file_path):
    print("Extracting audio...")
    command = "ffmpeg -i " + file_path + " audio.wav"
    subprocess.call(command, shell=True)

'''
command extracts only the audio from the input, and saves it into audio.wav
'''