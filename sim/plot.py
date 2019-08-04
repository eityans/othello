import matplotlib.pyplot as plt
import pickle
import numpy as np

# ファイルをオープンする
list = []

with open('list.txt', 'r') as f:
    for line in f:
        text = line.replace('\n','')
        list.append(int(text))
    print(list)

list = np.array(list)
# 一行ずつ表示する
plt.hist(list, bins=100)
plt.show()

