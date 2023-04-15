# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import nltk
from gensim.models import Word2Vec
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
import seaborn as sns

# Perform K-means clustering for different number of clusters and compute the inertia
inertia = []
for n in range(5, 100):
    km = KMeans(n_clusters=n, random_state=42)
    km.fit(filtered_data_vec)
    inertia.append(km.inertia_)

# Plot the elbow curve
plt.plot(range(5, 100), inertia)
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.title('Elbow curve')
plt.show()

from sklearn.model_selection import GridSearchCV

# Define the parameter grid
param_grid = {
    'init': ['k-means++', 'random'],
    'n_clusters': range(5,100),
    'max_iter': [1000, 1500, 2000]
}

# Perform grid search with cross-validation
grid_search = GridSearchCV(KMeans(random_state=42), param_grid, cv=5)
grid_search.fit(filtered_data_vec)

# Print the best hyperparameters
print(grid_search.best_params_)

"""Finetune the Word2vec model"""

# Load the list of unlabeled course content information
corpus = data['5']

documents_tokenized = [nltk.word_tokenize(document) for document in corpus]

import requests

# Download the SimLex-999 dataset
url = 'https://www.cl.cam.ac.uk/~fh295/SimLex-999.zip'
r = requests.get(url)
with open('SimLex-999.zip', 'wb') as f:
    f.write(r.content)

# Extract the dataset file
import zipfile
with zipfile.ZipFile('SimLex-999.zip', 'r') as zip_ref:
    zip_ref.extractall('SimLex-999')

# Load the word similarity dataset
similarity_dataset = {}
with open('SimLex-999.txt', 'r') as f:
    next(f)  # Skip the header row
    for line in f:
        word1, word2, _, _, _, _, _, _, score, _ = line.strip().split('\t')
        similarity_dataset[(word1, word2)] = float(score)

# Use word similarity task to evaluate the performance of each model
def evaluate_similarity(model):
    gold_scores = []
    model_scores = []
    for (word1, word2), gold_score in similarity_dataset.items():
        if word1 in model.wv.index_to_key and word2 in model.wv.index_to_key:
            gold_scores.append(gold_score)
            model_scores.append(model.wv.similarity(word1, word2))
    spearman_correlation = spearmanr(gold_scores, model_scores).correlation
    return spearman_correlation

from gensim.models import Word2Vec
import numpy as np
from sklearn.model_selection import ParameterGrid
from scipy.stats import spearmanr


# Define the range of values for each hyperparameter
params = {
    'vector_size': [100],
    'window': [5, 10],
    'min_count': [3, 5],
    'epochs': [50],
    'alpha': [0.03, 0.05],
    'min_alpha': [0.001, 0.005]
}


# Train and evaluate the model for each combination of hyperparameters
best_score = float('-inf')
best_model = None
for params in ParameterGrid(params):
    model = Word2Vec(
        documents_tokenized,
        workers=4,
        seed=42,
        **params
    )
    # Train the model
    model.train(corpus, total_examples=model.corpus_count, epochs=model.epochs)
    # Evaluate the model using word similarity task
    score = evaluate_similarity(model)
    # Keep track of the best model so far
    if score > best_score:
        best_score = score
        best_model = model

# Print the best model and its score
print(f"Best model: {best_model}")
print(f"Best score: {best_score:.4f}")

# Fine-tune the hyperparameters of the Word2Vec algorithm
model = Word2Vec(
    documents_tokenized,
    vector_size=500, # Increase the vector size
    window=10, # Increase the window size
    min_count=3, # Increase the minimum word count
    sg=1, # Use the skip-gram model instead of the CBOW model
    workers=4,
    epochs=50, # Increase the number of training epochs
    alpha=0.03, # Decrease the learning rate
    min_alpha=0.001 # Set the minimum learning rate
)
model.train(corpus, total_examples=model.corpus_count, epochs=model.epochs)

from scipy.stats import spearmanr
#min_count=3
score = evaluate_similarity(model)
print(f"Best score: {score:.4f}")

from scipy.stats import spearmanr
#window=5
score = evaluate_similarity(model)
print(f"Best score: {score:.4f}")

from scipy.stats import spearmanr
500
score = evaluate_similarity(model)
print(f"Best score: {score:.4f}")

from scipy.stats import spearmanr
300
score = evaluate_similarity(model)
print(f"Best score: {score:.4f}")

from scipy.stats import spearmanr
100
score = evaluate_similarity(model)
print(f"Best score: {score:.4f}")

# Fine-tune the hyperparameters of the Word2Vec algorithm
model = Word2Vec(
    documents_tokenized,
    vector_size=500, # Fine-tune the vector size to match the pre-trained model
    window=10, # Fine-tune the window size
    min_count=5, # Fine-tune the minimum word count
    sg=1, # Use the skip-gram model instead of the CBOW model
    workers=4,
    epochs=50, # Fine-tune the number of training epochs
    alpha=0.03, # Fine-tune the learning rate
    min_alpha=0.001, # Set the minimum learning rate
    seed=42 # Set the random seed for reproducibility
)

import urllib.request

# URL of the file to download
url = "http://nlp.stanford.edu/data/glove.6B.zip"

# Path where the file will be saved
path = "glove.6B.zip"

# Download the file from the URL and save it to the specified path
urllib.request.urlretrieve(url, path)

import gensim.downloader as api

# load pre-trained embeddings
wv = api.load('glove-wiki-gigaword-300')

# set initial weights
model.wv.vectors = wv.vectors

model.train(corpus, total_examples=model.corpus_count, epochs=model.epochs)

from scipy.stats import spearmanr

score = evaluate_similarity(model)
print(f"Best score: {score:.4f}")

