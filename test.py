import numpy as np
import matplotlib.pyplot as plt
from x_means import XMeans 

# データの準備
x = np.array([np.random.normal(loc, 0.1, 20) for loc in np.repeat([1,2], 2)]).flatten()
y = np.array([np.random.normal(loc, 0.1, 20) for loc in np.tile([1,2], 2)]).flatten()

# クラスタリングの実行
x_means = XMeans(random_state = 1).fit(np.c_[x,y]) 

# 結果をプロット
plt.scatter(x, y, c = x_means.labels_, s = 30)
plt.scatter(x_means.cluster_centers_[:,0], x_means.cluster_centers_[:,1], c = "r", marker = "+", s = 100)
plt.show()
