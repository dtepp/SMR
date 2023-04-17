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

def find_similar_courses(user_input, filtered_data,total):
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

    # Load the Word2Vec model
    model = Word2Vec.load('word2vec.model')

    # Generate embeddings for user input
    user_input_tokens = preprocess_text(user_input)
    user_input_vec = np.zeros((500,))
    for token in user_input_tokens:
        if token in model.wv.key_to_index:
            user_input_vec += model.wv[token]
    user_input_vec = user_input_vec.reshape(1, -1)

    # Preprocess the course descriptions
    filtered_data.loc[:, 'course_desc_tokens'] = filtered_data['5'].apply(preprocess_text)

    # Get the average word vectors for each course description
    filtered_data.loc[:, 'course_desc_vec'] = filtered_data['course_desc_tokens'].apply(lambda x: np.mean([model.wv[token] for token in x if token in model.wv.key_to_index], axis=0))

    # Convert the course vectors to a numpy array
    filtered_data_vec = np.array(filtered_data['course_desc_vec'].tolist())

    # Perform K-means clustering
    km = KMeans(n_clusters=98, random_state=42, init='k-means++', max_iter=1000)
    km.fit(filtered_data_vec)

    # Get the cluster centroids
    cluster_centroids = km.cluster_centers_


   

     # Find the top 5 most similar courses
    similarities = cosine_similarity(user_input_vec, cluster_centroids)
    most_similar_clusters_idx = np.argsort(similarities[0])[::-1][:5]
    print("\nThe Top 5 similar cluster courses:\n")

 # Print the most similar clusters
    CourseList=[]
    n=0
    
    for i, cluster_idx in enumerate(most_similar_clusters_idx):
        print(f"\n similar courses in cluster {cluster_idx+1}:\n")
        
        # Get the courses in the current cluster
        current_cluster = filtered_data[km.labels_ == cluster_idx]
        current_cluster_desc = current_cluster.iloc[:, :5].values.tolist()

        # Calculate similarities between user input and courses in the current cluster
        current_cluster_vec = filtered_data_vec[km.labels_ == cluster_idx]
        current_cluster_similarities = cosine_similarity(user_input_vec, current_cluster_vec)

        # Sort courses in the current cluster by similarity score
        courses_sorted_by_score = sorted(zip(current_cluster_desc, current_cluster_similarities[0]), key=lambda x: x[1], reverse=True)

        # Print top 20 courses and their similarity scores
        if (n<total):
            for j, (course, score) in enumerate(courses_sorted_by_score[:20]):
                print(f"{j+1}. {course} (Score: {score:.2f})")
                if (n<total):
                    CourseList.append(course)
                    n=n+1
                else:
                    break
        else:
                break
                
            
    return CourseList