import PyPDF2
import string
import math
from collections import Counter

def extract_text(FILE_PATH):
    pdfFileObject = open(FILE_PATH, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
    count = pdfReader.numPages
    for i in range(count):
        page = pdfReader.getPage(i)
        write_text(page.extractText())

def write_text(text):
    f = open("text.txt", "a+")
    text = text.rstrip("\n")
    f.write(text)
    f.close()

def get_words(FILE_PATH):
    words = []
    with open(FILE_PATH,'r') as f:
        for line in f:
            for word in line.split():
                word.rstrip("\n")

                for x in word.lower(): 
                    if x in string.punctuation: 
                        word = word.replace(x, "") 
                        
                if word not in string.punctuation:
                    words.append(word)
    words_counter = Counter(words)
    return words_counter


def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)

if __name__ == "__main__":
    PDF_FILE_PATH = 'lect5/lect5.pdf'
    TEXT_FILE_PATH = 'text.txt'
    NOTES_FILE_PATH = 'lect5/lect5_otp.txt'

    extract_text(PDF_FILE_PATH)

    words_counter1 = get_words(TEXT_FILE_PATH)
    words_counter2 = get_words(NOTES_FILE_PATH)

    sim_score = counter_cosine_similarity(words_counter1, words_counter2)
    print("Similarity score : ", sim_score )
    