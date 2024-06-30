import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency


def cramers_v(x, y):
    confusion_matrix = pd.crosstab(x, y)
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2_corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    r_corr = r - ((r - 1) ** 2) / (n - 1)
    k_corr = k - ((k - 1) ** 2) / (n - 1)
    return (phi2_corr / min((k_corr - 1), (r_corr - 1))) ** 0.5


# 示例数据
np.random.seed(0)
category1 = np.random.choice(['A', 'B', 'C'], size=100)
category2 = np.random.choice(['X', 'Y', 'Z'], size=100)

# 计算Cramer's V
cramers_v_value = cramers_v(category1, category1)
print('Cramer\'s V: {:.3f}'.format(cramers_v_value))