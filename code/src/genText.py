from pydub import AudioSegment
import os
import speech_recognition as sr

#function to generate text given the audio file as input in .wav format
def generate_text(WAV_FILE):
    #file to which the transcribed text will be written
    fp = open("notes.txt","a+")
    r = sr.Recognizer()
    with sr.WavFile(WAV_FILE) as source:
        audio = r.record(source) 

    try:
        txt = r.recognize_google(audio)
        fp.write(txt)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    fp.close() 

#function that segments a big audio file into 3mintues audio files
#calls generate_text function on each of those segments
def transcribe(audio_file_path):
    #main sudio file
    audio_file = AudioSegment.from_wav(audio_file_path)
    audio_length = len(audio_file)

    time_seg = 180 * 1000     
    quotient, remainder = divmod(audio_length, time_seg)
    #decide the number of segements of length time_seg that could be made from audio_file 
    num_segments = quotient + int(bool(remainder)) 

    #iterate through each 3minutes segment
    for seg_no in range(num_segments):
        #decide the start and end timing of audio segment
        firstPart = (time_seg * seg_no)
        secondPart =  (time_seg * (seg_no + 1))

        #extract the required audi segment from big audio file
        audio_segment = audio_file[firstPart:secondPart]
        #create a new .wav file from extracted audio segment
        audio_segment_file = "audio_segment.wav"
        audio_segment.export(audio_segment_file , format="wav")
        #generate text for the audio segment
        generate_text(audio_segment_file)