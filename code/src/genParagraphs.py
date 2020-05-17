import collections
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from pprint import pprint


def word_tokenizer(text):
    #tokenizes and stems the text
    tokens = word_tokenize(text)
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(t) for t in tokens if t not in stopwords.words('english')]
    return tokens


def cluster_sentences(sentences, nb_of_clusters=5):
    tfidf_vectorizer = TfidfVectorizer(tokenizer=word_tokenizer, stop_words=stopwords.words('english'), max_df=0.9, min_df=0.1, lowercase=True)
    
    tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)
    kmeans = KMeans(n_clusters=nb_of_clusters)
    kmeans.fit(tfidf_matrix)
    clusters = collections.defaultdict(list)

    for i, label in enumerate(kmeans.labels_):
            clusters[label].append(i)
    return dict(clusters)


def genParagraphs():
    f = open("notes.txt")
    text = f.read()
    sentences = nltk.sent_tokenize(text)
    nclusters= 10
    clusters = cluster_sentences(sentences, nclusters)

    f.close()
    f = open("notes.txt", "w")
    for cluster in range(nclusters):
            print("cluster ",cluster,":")
            for i, sentence in enumerate(clusters[cluster]):
                    f.write(sentences[sentence])
            f.write("\n\n")
    f.close()
    
    #replacing '.' with '. '
    fin = open("notes.txt", "rt")
    data = fin.read()
    data = data.replace('.', '. ')
    fin.close()
    
    fin = open("notes.txt", "wt")
    fin.write(data)
    fin.close()