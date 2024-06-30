import numpy as np
from scipy.stats import norm

def gaussian_copula(hist_probs, corr_matrix, num_samples):
    # 1. Generate multivariate normal samples
    mvnorm_samples = np.random.multivariate_normal(mean=np.zeros(len(hist_probs)), cov=corr_matrix, size=num_samples)

    # 2. Apply the univariate CDF (which is the inverse of the PDF)
    unif_samples = norm.cdf(mvnorm_samples)

    # 3. Transform uniform samples to match the histogram probabilities
    hist_samples = [np.percentile(unif_samples[:,i], q=100*hist_probs[i]) for i in range(len(hist_probs))]

    return np.array(hist_samples).T

# Example usage:
hist_probs = [0.1, 0.2, 0.3, 0.4]  # replace with your histogram probabilities
corr_matrix = np.eye(len(hist_probs))  # replace with your correlation matrix
num_samples = 1000

joint_samples = gaussian_copula(hist_probs, corr_matrix, num_samples)
print(joint_samples)
