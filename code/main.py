from flask import Flask, render_template
from flask import request, redirect

from src.genAudio import generate_audio
from src.genText import transcribe
from src.genPunctuations import addPunctuation
from src.genPDF import createPDF
from src.genPPT import createPPT
from src.genParagraphs import genParagraphs

import os
app = Flask(__name__)

filename = ''
@app.route('/')
@app.route('/homePage')
def homePage():
    return render_template('homePage.html')

@app.route('/notes', methods=["POST"])
def notes():
    if request.method == 'POST': 
        global filename 
        f = request.files['file'] 

        #save the uploaded file in current directory
        f.save(f.filename)
        filename = f.filename

        video_path = f.filename + ".mp4"
        audio_path =  'audio.wav'
        audio_seg_path = 'audio_segment.wav'

        #extract audio from video
        try:
            generate_audio(f.filename)
            print("EXTRACTED AUDIO")
            os.remove(f.filename)
        except:
            print("Couldn't generate audio")
            return render_template('homePage.html')
       
        # generate transcipt from generated audio
        try:
            transcribe(audio_path)
            print("GENERATED TEXT")
            os.remove(audio_path)
            os.remove(audio_seg_path)
        except:
            print("Couldn't generate text")
            return render_template('homePage.html')
            
        # add punctuation to generated text doucment
        try:
            text_file_path = "notes.txt"
            addPunctuation(text_file_path)
            print("PUNCTUATED TEXT GENERATED")
        except:
            print("Couldn't add punctuation")
            return render_template('homePage.html')

        #segment the punctuated document into paragraphs
        try:
            genParagraphs()
            print("Segmented the text")
        except:
            print("Couldn't segment the text document")
            return render_template('homePage.html')
            
        # Todo: remove irrelevant contents
        f = open('notes.txt')
        text = f.read()
        f.close()
        return render_template('notes.html', text = text)

    # if request method is anything other than POST
    else:
        return render_template('homePage.html')


@app.route('/download', methods=['POST'])
def download():
    #write edited form contents into the file
    text = request.form['notes']
    f = open('notes.txt', 'w')
    f.write(text)
    f.close()

    if request.method == 'POST':  
        global filename
        # generate PDF from formatted text and save document
        try:
            createPDF(filename, 'notes.txt')
            print("PDF GENERATED")
        except:
            print("Couldn't generate PDF")

        
        #generte PPT from formatted text document
        try:
            createPPT(filename, 'notes.txt', 'title')
            print("PPT GENERATED")
        except:
            print("Couldn't generate PPT")
        
        #os.remove('notes.txt')
    return redirect('/')

if __name__=="__main__":
    app.run()