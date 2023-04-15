
from sklearn.decomposition import TruncatedSVD
import numpy as np
import matplotlib.pyplot as plt

# Load or create your unlabeled data (e.g. X_unlabeled)
# ...

# Create a TruncatedSVD object
svd = TruncatedSVD(200)

# Fit the SVD object to the unlabeled data
svd.fit(X_lsa)

# Get the explained variance of each component
explained_variances = svd.explained_variance_

# Compute the cumulative sum of the explained variances
cumulative_explained_variances = np.cumsum(explained_variances)

# Create a scree plot to visualize the explained variances
plt.plot(range(1, len(cumulative_explained_variances) + 1), cumulative_explained_variances)
plt.xlabel('Number of components')
plt.ylabel('Cumulative explained variance')
plt.title('Scree plot')
plt.show()


