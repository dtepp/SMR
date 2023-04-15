# -*- coding: utf-8 -*-


import pandas as pd
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Step 1: Read data from a CSV file with header
df = pd.read_csv('data.csv')

stop_words = set(stopwords.words('english')+ ['introduction', 'compulsory', 'course'])

def preprocess(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    tokens = [w for w in tokens if not w in stop_words]
    return ' '.join(tokens)

df['5'] = df['5'].apply(preprocess)

# Step 3: Group the data by the 'cluster' column
grouped = df.groupby('cluster')

# Step 4: Loop through every group and concatenate all '5' column text values into one long sentence
sentences = []
for name, group in grouped:
    text = ' '.join(group['5'].tolist())
    sentences.append(text)

# Step 5: Use NMF method on the concatenated sentences
vectorizer = CountVectorizer(stop_words='english',max_df=0.95, min_df=3)
tfidf = vectorizer.fit_transform(sentences)
nmf = NMF(n_components=7, random_state=42)
nmf_values = nmf.fit_transform(tfidf)

# Step 6: Perform text clustering on the NMF values
kmeans = KMeans(n_clusters=10,random_state=42,init='k-means++', max_iter=2500)
cluster_labels = kmeans.fit_predict(nmf_values)

# Step 7: Evaluate the cluster result using silhouette score
score = silhouette_score(nmf_values, cluster_labels)

# Step 8: Save the cluster result
result = pd.DataFrame({'cluster': grouped.groups.keys(), 'group_labels': cluster_labels})
result.to_csv('NMFresult.csv', index=False)

print(score)

NMF = pd.read_csv("NMFresult.csv",header=0)

# merge the two dataframes based on the 'cluster' column
merged_df = pd.merge(data, NMF[['cluster', 'group_labels']], on='cluster', how='left')

# save the merged dataframe to a new CSV file
merged_df.to_csv("NMFGroup.csv", index=False)

silhouette_scores = []
components_range = range(2, 11)
for n_components in components_range:
    nmf = NMF(n_components=n_components, random_state=42)
    nmf_values = nmf.fit_transform(tfidf)
    cluster_labels = KMeans(n_clusters=10, random_state=42,init='k-means++', max_iter=2500).fit_predict(nmf_values)
    score = silhouette_score(nmf_values, cluster_labels)
    silhouette_scores.append(score)

best_n_components = components_range[np.argmax(silhouette_scores)]
print("Best number of components:", best_n_components)

