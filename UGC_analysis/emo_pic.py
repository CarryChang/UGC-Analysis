import matplotlib.pyplot as plt
import numpy as np
# 显示中文
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

sentiments_list = [0.994,0.01]
plt.hist(sentiments_list, bins=20)
plt.xlabel("情感值")
plt.ylabel("评论数目")
plt.title('整体情感极性分布图')
plt.show()
plt.close()