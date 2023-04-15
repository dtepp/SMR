# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.base import BaseEstimator, TransformerMixin

stopword = set(stopwords.words('english')+['introduction', 'compulsory', 'course','student'])
lemmatizer = WordNetLemmatizer()

class TextPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self, preprocessing_steps):
        self.preprocessing_steps = preprocessing_steps
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        for step_name, step_func in self.preprocessing_steps:
            X = X.apply(step_func)
        return X


# Load data from CSV file
df = pd.read_csv('NMFGroup.csv')

# Define the preprocessing steps for text data
preprocessing_steps = [
    ('lowercase', lambda x: x.lower()),
    ('stopwords', lambda x: ' '.join(word for word in x.split() if word not in stopwords)),
    ('lemmatize', lambda x: ' '.join(lemmatizer.lemmatize(word) for word in x.split()))
]

# Define the pipeline for topic modeling
pipeline = Pipeline([
    ('preprocess', TextPreprocessor(preprocessing_steps)),
    ('vectorizer', CountVectorizer()),
    ('model', LatentDirichletAllocation())
])

# Define the parameter grid for GridSearchCV
param_grid = {
    'vectorizer__max_df': [0.95],
    'vectorizer__min_df': [ 3],
    'model__n_components': [5,10,15,20]
}

# Perform grid search to find the best parameters
grid_search = GridSearchCV(pipeline, param_grid=param_grid, cv=5, n_jobs=-1)
grid_search.fit(df['5'], df['group_labels'])

# Print the best parameters and their corresponding score
print(f"Best parameters: {grid_search.best_params_}")
print(f"Best score: {grid_search.best_score_}")

