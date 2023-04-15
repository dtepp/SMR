# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import string
import nltk
import re
import sklearn
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from gensim.models import LdaModel
from gensim.corpora import Dictionary
from gensim.models import Word2Vec
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, normalized_mutual_info_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.manifold import TSNE
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import metrics
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from gensim import corpora, models

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

data = pd.read_csv("data.csv",header=0)

data.head()

stop_words = set(stopwords.words('english')+ ['introduction', 'compulsory', 'course'])

# Define text preprocessing function
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove non-alphanumeric characters and extra whitespace
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove stop words
    tokens = [token for token in tokens if token not in stop_words]
    # Join the tokens back into a string
    text = ' '.join(tokens)
    return text

# Read data from CSV file
data = pd.read_csv("data.csv")

# Group data by 'cluster' column
grouped_data = data.groupby('cluster')

# Loop through each group and concatenate all  '5' column values
corpus = []
processed_labels = []
processed_text=[]
for name, group in grouped_data:
    # Preprocess text values in '5' column
    processed_text.append(' '.join(list(group['5'])))
    group['5'] = group['5'].apply(preprocess_text)
    corpus.append(' '.join(list(group['5'])))
    processed_labels.append(name)

# Apply LDA on the concatenated texts
vectorizer = CountVectorizer(max_df=0.95, min_df=3)
X = vectorizer.fit_transform(corpus)

lda = LatentDirichletAllocation(n_components=7, random_state=42,learning_decay=0.7)
lda.fit(X)

# Apply KMeans clustering on the LDA values
kmeans = KMeans(n_clusters=10, random_state=42,init='k-means++', max_iter=2500)
kmeans.fit(lda.transform(X))

# Evaluate the clustering result
score = silhouette_score(lda.transform(X), kmeans.labels_)
print("Silhouette score:", score)

cluster_result = pd.DataFrame({'group_labels': kmeans.labels_, 'cluster': processed_labels})

# merge the two dataframes based on the 'cluster' column
merged_df = pd.merge(data, cluster_result[['cluster', 'group_labels']], on='cluster', how='left')

# save the merged dataframe to a new CSV file
merged_df.to_csv("LDAGroup.csv", index=False)

merged_df.head()

"""Test"""

# import numpy as np
# import pandas as pd
# import re, nltk, spacy, gensim

# # Sklearn
# from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD
# from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
# from sklearn.model_selection import GridSearchCV
# from pprint import pprint

# import matplotlib.pyplot as plt
# %matplotlib inline

# # Define Search Param
# search_params = {'n_components': range(2,11), 'learning_decay': [ .7, .9]}

# # Init the Model
# lda = LatentDirichletAllocation(random_state=42)

# # Init Grid Search Class
# model = GridSearchCV(lda, param_grid=search_params)

# # Do the Grid Search
# model.fit(X)

# # Best Model
# best_lda_model = model.best_estimator_

# # Model Parameters
# print("Best Model's Params: ", model.best_params_)

# # Log Likelihood Score
# print("Best Log Likelihood Score: ", model.best_score_)

# # Perplexity
# print("Model Perplexity: ", best_lda_model.perplexity(X))