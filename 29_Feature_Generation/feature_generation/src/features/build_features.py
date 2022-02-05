from re import X
import nltk
import os
nltk.download('stopwords')
nltk.download('wordnet')

import pandas as pd
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from tqdm import tqdm

from gensim.models.wrappers import FastText

## For Index Based

def create_corpuses(X_train):
    document_corpus = X_train['text'].list()
    data_corpus = set()
    for row in document_corpus:
        for word in row.split(" "):
            if word not in data_corpus:
                data_corpus.add(word)

    data_corpus=sorted(data_corpus)
    return document_corpus, data_corpus

def create_binary_bow(X_train):
    document_corpus, data_corpus = create_corpuses(X_train)
    res = len(max(document_corpus, key = len).split(" "))
    index_based_encoding=[]
    for row in document_corpus:
        row_encoding = []
        split = row.split(" ")
        for i in range(res):
            if i <= len(split)-1:
                row_encoding.append(data_corpus.index(split[i])+1)
            else:
                row_encoding.append(0)
        index_based_encoding.append(row_encoding)
    return index_based_encoding



## For BOWs

def get_binary_bow(X_train):
    document_corpus, data_corpus = create_corpuses(X_train)
    #BINARY BOW
    one_hot_encoding = []
    for row in document_corpus:
        row_encoding = []
        split = row.split(" ")
        for word in data_corpus:
            if word in split:
                row_encoding.append(1)
            else:
                row_encoding.append(0)
        one_hot_encoding.append(row_encoding)
    return one_hot_encoding

def get_count_bow(X_train):
    document_corpus, data_corpus = create_corpuses(X_train)
    one_hot_encoding = []
    for row in document_corpus:
        row_encoding = []
        split = row.split(" ")
        for word in data_corpus:
            count = split.count(word)
            if word in split:
                row_encoding.append(count)
            else:
                row_encoding.append(count)
        one_hot_encoding.append(row_encoding)
    return one_hot_encoding



## For TF-IDF

def preprocess_text(text):
    # Tokenise words while ignoring punctuation
    tokeniser = RegexpTokenizer(r'\w+')
    tokens = tokeniser.tokenize(text)
    
    # Lowercase and lemmatise 
    lemmatiser = WordNetLemmatizer()
    lemmas = [lemmatiser.lemmatize(token.lower(), pos='v') for token in tokens]
    
    # Remove stopwords
    keywords= [lemma for lemma in lemmas if lemma not in stopwords.words('english')]
    return keywords

def get_tfidf_features(X_train):
    # Create an instance of TfidfVectorizer
    vectoriser = TfidfVectorizer(analyzer=preprocess_text)
    # Fit to the data and transform to feature matrix
    X_train = vectoriser.fit_transform(X_train['text'])
    # Convert sparse matrix to dataframe
    X_train = pd.DataFrame.sparse.from_spmatrix(X_train)
    # Save mapping on which index refers to which words
    col_map = {v:k for k, v in vectoriser.vocabulary_.items()}
    # Rename each column using the mapping
    for col in X_train.columns:
        X_train.rename(columns={col: col_map[col]}, inplace=True)
    return X_train


## For Glove Embedding

def get_glove_embedding(text):
    token = Tokenizer()
    token.fit_on_texts(text)
    seq = token.texts_to_sequences(text)
    pad_seq = pad_sequences(seq,maxlen=300)
    vocab_size = len(token.word_index)+1
    embedding_vector = {}
    f = open('../input/embeddings/glove.840B.300d/glove.840B.300d.txt')     ### To Do: Change this so that it takes from environment variable
    for line in tqdm(f):
        value = line.split(' ')
        word = value[0]
        coef = np.array(value[1:],dtype = 'float32')
        embedding_vector[word] = coef



## For FastText

def get_fasttext_embeddding(text):
    model = FastText.load_fasttext_format('wiki.simple')
    # This seems like the code to train fastext (rather than using pretrained?)
    ## Will have to see if the embedding layer needs to be added directly onto the model, or is their a way to do this cleanly.

