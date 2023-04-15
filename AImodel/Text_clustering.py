# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import string
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering, MiniBatchKMeans
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, normalized_mutual_info_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.manifold import TSNE
from sklearn import metrics
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import TruncatedSVD

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

# import data
data = pd.read_excel("data.xlsx")
texts = data.iloc[:, 5]
texts.head()

# data preprocessing 
processed_data = []
processed_texts = []
for text in texts:

    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = nltk.word_tokenize(text)
    lemmatizer = nltk.WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    stopwords = nltk.corpus.stopwords.words("english")+ ['introduction', 'compulsory', 'course']
    tokens = [token for token in tokens if token not in stopwords]
    processed_texts.append(" ".join(tokens))
    processed_data.append(tokens)

# Vectorize text data using TF-IDF
tfidf_vectorizer  = TfidfVectorizer(max_df=0.7, max_features=2500,
                             min_df=3, stop_words=stopwords,
                             use_idf=True)
tfidf = tfidf_vectorizer.fit_transform(processed_texts)
tfidf.shape
svd = TruncatedSVD(200)
normalizer = Normalizer(copy=False)
lsa = make_pipeline(svd, normalizer)
X_lsa = lsa.fit_transform(tfidf)




def evaluate_clustering(models, X):
    best_model = None 
    best_score = -1 
    best_name = "" 
    
    for name, model in models.items():
        model.fit(X) 
        labels = model.fit_predict(X)   
        score = silhouette_score(X, labels) 
            
        if score > best_score:
                
                best_model = model 
                best_score = score 
                best_name = name
                
        print(f"{name}: {score}") 
        print("Coefficient for 16 clusters: %0.3f"
  % metrics.silhouette_score(X, model.labels_))
        labels, counts = np.unique(model.labels_[model.labels_>=0], return_counts=True)
        print (labels)
        print (counts)
            
    print(f"Best model: {best_name}") 
    
    return best_model



models = {
    "KMeans": KMeans(n_clusters=128, init='k-means++', max_iter=2500,random_state=42), 
    "GMM":GaussianMixture(n_components=17, random_state=42),  
    "Agglomerative": AgglomerativeClustering(n_clusters=16),
    "MiniKmeans":MiniBatchKMeans(n_clusters=13,batch_size=2048, random_state=42)
}


best_model = evaluate_clustering(models, X_lsa)

def print_terms(cm, num):
    original_space_centroids = cm.cluster_centers_
    order_centroids = original_space_centroids.argsort()[:, ::-1]
    terms = tfidf_vectorizer.get_feature_names_out()
    for i in range(num):
        print("Cluster %d:" % i, end='')
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind], end='')
        print()


print_terms(best_model, 10)


labels = pd.DataFrame(best_model.labels_) 
y = labels.apply(lambda x: x.mode().values[0], axis=1)

data["cluster"] = y


data.to_csv("output.csv", index=False)

