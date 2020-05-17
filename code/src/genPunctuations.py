from punctuator import Punctuator

def addPunctuation(text_file):
    #load the pre-trained model
    p = Punctuator('model.pcl')

    #read unstructured text from the file
    fp = open(text_file, "r")
    text = fp.read()
    
    #punctuate the read text
    sentences = p.punctuate(text)
    fp.close()

    #write punctuated text into the file
    otp_file = open("notes.txt", "w")
    otp_file.write(sentences)
    otp_file.close()

