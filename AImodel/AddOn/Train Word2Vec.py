# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import nltk
from gensim.models import Word2Vec
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Load the unlabeled course content data
data = pd.read_csv('data.csv',header=0)


# Preprocess the text data
stop_words = set(stopwords.words('english')+['introduction', 'compulsory', 'course','student'])
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = text.lower() # Convert to lowercase
    tokens = nltk.word_tokenize(text)
    # remove stop words
    tokens = [token for token in tokens if token not in stop_words]
    # lemmatize the tokens
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    text = ' '.join(tokens)
    return text

data['5'] = data['5'].apply(preprocess_text)

corpus = data['5']

# Train a Word2Vec model
sentences = [nltk.word_tokenize(sent) for sent in data['5']]
model = Word2Vec(
    sentences,
    vector_size=500, # Increase the vector size
    window=10, # Increase the window size
    min_count=5, # Increase the minimum word count
    sg=1, # Use the skip-gram model instead of the CBOW model
    workers=4,
    epochs=50, # Increase the number of training epochs
    alpha=0.03, # Decrease the learning rate
    min_alpha=0.001 # Set the minimum learning rate
)

model.train(corpus, total_examples=model.corpus_count, epochs=model.epochs)

# Save the Word2Vec model
model.save('word2vec.model')
