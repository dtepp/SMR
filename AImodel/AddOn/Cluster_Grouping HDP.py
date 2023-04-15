# -*- coding: utf-8 -*-

import csv
import re
from itertools import groupby
from gensim.models.hdpmodel import HdpModel
from gensim.corpora import Dictionary
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

# Read data from CSV file
with open('data.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    data = [row for row in reader]

# Data preprocessing: clean text data
stop_words = set(stopwords.words('english'))
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    tokens = [w for w in tokens if not w in stop_words]
    return ' '.join(tokens)


# Group data by cluster column
data_groups = {}
for key, group in groupby(data, lambda x: x['cluster']):
    data_groups[key] = list(group)

# Concatenate all "5" column text values for each group
for group in data_groups.values():
    group_text = ' '.join(clean_text(row['5']) for row in group)
    group[0]['text'] = group_text

# Data preprocessing: vectorize text data
vectorizer = CountVectorizer(stop_words='english',max_df=0.95, min_df=3)
X_counts = vectorizer.fit_transform([group[0]['text'] for group in data_groups.values()])
X_tfidf = TfidfTransformer().fit_transform(X_counts)

# Process text using HDP method for each group
texts = [[word.lower() for word in group[0]['text'].split()] for group in data_groups.values()]
stop_words = vectorizer.get_stop_words()
texts = [[word for word in text if word not in stop_words] for text in texts]
dictionary = Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
hdp = HdpModel(corpus, id2word=dictionary)

hdp_values = []
for group in data_groups.values():
    bow = dictionary.doc2bow([word.lower() for word in group[0]['text'].split()])
    hdp_value = hdp[bow][0][1]  # get HDP value from topic 0
    hdp_values.append(hdp_value)
    group[0]['hdp_value'] = hdp_value

# Perform text clustering on HDP values
kmeans = KMeans(n_clusters=10,random_state=42,init='k-means++', max_iter=2500)  # set number of clusters to 3
cluster_labels = kmeans.fit_predict(np.array(hdp_values).reshape(-1, 1))

# Evaluate clustering using silhouette score
silhouette_avg = silhouette_score(np.array(hdp_values).reshape(-1, 1), cluster_labels)

# Save cluster result to CSV file
with open('hdpoutput.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['cluster', 'hdp_value', 'label'])
    for group, hdp_value, label in zip(data_groups.values(), hdp_values, cluster_labels):
        writer.writerow([group[0]['cluster'], hdp_value, label])

hdp = pd.read_csv("hdpoutput.csv",header=0)

# merge the two dataframes based on the 'cluster' column
merged_df = pd.merge(data, hdp[['cluster', 'label']], on='cluster', how='left')

# save the merged dataframe to a new CSV file
merged_df.to_csv("HDPGroup.csv", index=False)



print(silhouette_avg)
