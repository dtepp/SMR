# -*- coding: utf-8 -*-

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

# Load the data
df = pd.read_csv('NMFGroup.csv')

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

df['5'] = df['5'].apply(preprocess_text)

# Group the data by 'group' column
grouped = df.groupby('label')['5'].apply(lambda x: ' '.join(x)).reset_index()

# Use CountVectorizer to create a document-term matrix
vectorizer = CountVectorizer(max_df=0.95, min_df=3)
doc_term_matrix = vectorizer.fit_transform(grouped['5'])

# Use Latent Dirichlet Allocation (LDA) for topic modeling
lda_model = LatentDirichletAllocation(n_components=10, random_state=42,max_iter=500)
lda_model.fit(doc_term_matrix)

# Evaluate the model
perplexity = lda_model.perplexity(doc_term_matrix)
print(f"Perplexity of the model: {perplexity}")

# Save the result
topic_dist = lda_model.transform(doc_term_matrix)
grouped['topic'] = topic_dist.argmax(axis=1)
grouped.to_csv('NMFGropuTopic.csv', index=False)

