import random

import numpy as np
from scipy.stats import norm, pearsonr
import matplotlib.pyplot as plt
from scipy.linalg import cho_factor, cho_solve


# 假设你有两个直方图，代表两个边缘分布
# 这里我们简化处理，直接定义累积分布函数（CDF）的逆函数
def inverse_cdf_hist1(u):
    # 这里应该是根据直方图数据计算出的逆CDF，这里仅作示意
    # u 是从[0, 1]均匀分布中抽取的样本
    # 这里简单地假设逆CDF是一个线性映射，实际情况需要根据直方图数据计算
    u[u < 0.2] = np.random.uniform(0, 10, size=np.sum(u < 0.2))
    u[(u < 0.5) & (u > 0.2)] = np.random.uniform(10, 20, size=np.sum((u < 0.5) & (u > 0.2)))
    u[(u <= 1.0) & (u > 0.5)] = np.random.uniform(20, 30, size=np.sum((u <= 1.0) & (u > 0.5)))
    return u

def inverse_cdf_hist2(u):
    u[u < 0.1] = np.random.uniform(0, 10, size=np.sum(u < 0.1))
    u[(u < 0.3) & (u > 0.1)] = np.random.uniform(10, 20, size=np.sum((u < 0.3) & (u > 0.1)))
    u[(u <= 0.7) & (u > 0.3)] = np.random.uniform(20, 30, size=np.sum((u <= 0.7) & (u > 0.3)))
    u[(u <= 1.0) & (u > 0.7)] = np.random.uniform(30, 40, size=np.sum((u <= 1.0) & (u > 0.7)))
    return u

# 定义相关系数矩阵
rho = 0.6
correlation_matrix = np.array([[1, rho], [rho, 1]])

# Cholesky分解
L = np.linalg.cholesky(correlation_matrix)

# 生成独立的标准正态分布样本
n_samples = 10000
mvnorm_samples = np.random.multivariate_normal(mean=np.zeros(2), cov=correlation_matrix, size=n_samples)
correlation, p_value = pearsonr(mvnorm_samples[:, 0], mvnorm_samples[:, 1])
print('多元正态分布相关性：', correlation)


# 将正态样本转换为具有直方图分布的样本
u1 = norm.cdf(mvnorm_samples[:, 0])
u2 = norm.cdf(mvnorm_samples[:, 1])


samples_hist1 = inverse_cdf_hist2(u1)
samples_hist2 = inverse_cdf_hist1(u2)

# 绘制模拟的联合直方图分布样本
correlation, p_value = pearsonr(samples_hist1, samples_hist2)
print('直方图样本相关性：', correlation)
print('属性1')
print('新概率分布   原概率分布')
print((np.sum(samples_hist1 < 10)) / n_samples, 0.2)
print((np.sum(samples_hist1 < 20) - np.sum(samples_hist1 < 10)) / n_samples, 0.3)
print((np.sum(samples_hist1 < 30) - np.sum(samples_hist1 < 20)) / n_samples, 0.5)
print()
print('属性2')
print('新概率分布   原概率分布')
print((np.sum(samples_hist2 < 10)) / n_samples, 0.1)
print((np.sum(samples_hist2 < 20) - np.sum(samples_hist2 < 10)) / n_samples, 0.2)
print((np.sum(samples_hist2 < 30) - np.sum(samples_hist2 < 20)) / n_samples, 0.4)
print((np.sum(samples_hist2 < 40) - np.sum(samples_hist2 < 30)) / n_samples, 0.3)
# plt.scatter(samples_hist1, samples_hist2, alpha=0.5)
# plt.xlabel('Random Variable 1 (Histogram-based)')
# plt.ylabel('Random Variable 2 (Histogram-based)')
# plt.title('Simulated Joint Distribution from Histograms')
# plt.show()

