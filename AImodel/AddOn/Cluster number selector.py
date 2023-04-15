# Determine optimal number of clusters using silhouette score
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import numpy as np


# define the range of k values to test
k_values = range(120,140)
# initialize lists to store WCSS and silhouette scores for each k value
wcss_scores = []
silhouette_scores = []
X=X_lsa
# calculate WCSS and silhouette scores for each k value
for k in k_values:
    kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=2500,random_state=42)
    kmeans.fit(X)
    wcss_scores.append(kmeans.inertia_)  # Inertia: Sum of squared distances of samples to their closest cluster center.
    labels = kmeans.predict(X)
    silhouette_scores.append(silhouette_score(X, labels))
    print(silhouette_score(X, labels))

# plot the WCSS scores and look for the elbow point
plt.plot(k_values, wcss_scores, 'bx-')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Within-Cluster Sum of Squares (WCSS)')
plt.title('Elbow Method')
plt.show()

# plot the silhouette scores and look for the highest score
plt.plot(k_values, silhouette_scores, 'bx-')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Silhouette score')
plt.title('Silhouette Coefficient Method')
plt.show()

# # select the optimal k value based on the plots or domain-specific knowledge
# optimal_k = 22  # for example

# # perform k-means clustering with the selected k value-22
# kmeans = KMeans(n_clusters=optimal_k, random_state=42)
# kmeans.fit(X)
# labels = kmeans.predict(X)

from sklearn.mixture import GaussianMixture
import numpy as np
import matplotlib.pyplot as plt

# load your text data and create a feature matrix X
# ...

# define the range of k values to test
k_values = range(5, 50)

# initialize list to store BIC scores for each k value -17
bic_scores = []

# calculate BIC score for each k value
for k in k_values:
    gmm = GaussianMixture(n_components=k, random_state=42)
    gmm.fit(X)
    bic_scores.append(gmm.bic(X))

# plot the BIC scores and look for the lowest score
plt.plot(k_values, bic_scores, 'bx-')
plt.xlabel('Number of clusters (k)')
plt.ylabel('BIC score')
plt.title('Bayesian Information Criterion Method')
plt.show()

# load your text data and create a feature matrix X
# ...

# define the range of k values to test
k_values = range(10, 30)

# initialize list to store silhouette scores for each k value
silhouette_scores = []

# calculate silhouette score for each k value-16
for k in k_values:
    agg_clustering = AgglomerativeClustering(n_clusters=k)
    labels = agg_clustering.fit_predict(X)
    silhouette_scores.append(silhouette_score(X, labels))

# plot the silhouette scores and look for the highest score
plt.plot(k_values, silhouette_scores, 'bx-')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Silhouette score')
plt.title('Silhouette Score Method')
plt.show()

from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import silhouette_score
import numpy as np
import matplotlib.pyplot as plt

# load your text data and create a feature matrix X
# ...

# define the range of k values to test
k_values = range(10, 30)

# initialize list to store silhouette scores for each k value
silhouette_scores = []

# calculate silhouette score for each k value-13
for k in k_values:
    kmeans = MiniBatchKMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    labels = kmeans.predict(X)
    silhouette_scores.append(silhouette_score(X, labels))

# plot the silhouette scores and look for the highest score
plt.plot(k_values, silhouette_scores, 'bx-')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Silhouette score')
plt.title('Silhouette Score Method')
plt.show()

