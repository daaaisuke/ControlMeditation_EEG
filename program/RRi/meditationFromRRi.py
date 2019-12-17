import collections
import matplotlib.pyplot as plt
import csv

cut_dis1 = 25
cut_dis2 = 150
cut_rri = 860
num_overlap = 2

# ----- 四捨五入関数 -----
def my_round(val, digit=0):
    p = 10 ** digit
    return int((val * p * 2 + 1) // 2 / p)

# ----- 必要データの抽出&整形 -----
data_graph = []
# データの形
# data_graph = [
#   [RRI 0, RRI 1, RRI 2, ... RRI k-1],
#   [RRI 1, RRI 2, RRI 3, ... RRI k]
# ]
#with open("../../csv/RRi/sleep_close2_remove.csv","r", encoding='utf-8-sig') as f:
with open("/Users/daisuke/Book1.csv","r", encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    RRi_data = []
    for row in reader:
        RRi_data.append(row)

for i in range(len(RRi_data)):
    for j in range(len(RRi_data[i])):
        #RRi_data[i][j] = my_round(int(RRi_data[i][j]), -1)
        RRi_data[i][j] = int(RRi_data[i][j])

data_graph.append(RRi_data[0])
data_graph.append(RRi_data[1])

# ----- データの重複が少ない部分を削除 -----
#data_str = []
#print(len(data_graph[0]))
#for i in range(len(data_graph[0])):
#  print(i)
#  data_str.append(str(data_graph[0][i]) + ',' + str(data_graph[1][i]))
#n_count = collections.Counter(data_str).most_common()   # 組み合わせの個数の配列
#for i in range(len(n_count)-1, -1, -1):   # range(開始の数, 終了の数-1, 増減) | 重複している部分を削除
#    if num_overlap <= n_count[i][1]:
#        del n_count[i]
#for c in n_count:   # 重複の少ないデータを削除
#  for i in range(len(data_graph[1])-1, -1, -1):   #削除時の配列要素数の変化を防ぐため逆から回す
#    if (data_graph[0][i] == float(c[0].split(',')[0])) and (data_graph[1][i] == float(c[0].split(',')[1])):
#      del data_graph[0][i], data_graph[1][i]


plus_max, plus_min = 0, cut_rri+cut_rri
minus_max, minus_min = 0, cut_rri
for i in range(len(data_graph[0])):
  plus_max = max(plus_max, data_graph[0][i]+data_graph[1][i])
  plus_min = min(plus_min, data_graph[0][i]+data_graph[1][i])
  minus_max = max(minus_max, data_graph[1][i]-data_graph[0][i]+cut_rri)
  minus_min = min(minus_min, data_graph[1][i]-data_graph[0][i]+cut_rri)
print(plus_max)
print(plus_min)
print(minus_max)
print(minus_min)
plus_length = plus_max/2 - plus_min/2
minus_length = minus_max/2 - minus_min/2
print(plus_length)
print(minus_length)


# ----- グラフ描画 -----
plt.figure()

plt.xlim([500, 1200])
plt.ylim([500, 1200])
plt.title('RRi', fontsize=7)
#plt.text(750, 1050, r'$\frac{\nearrow}{\searrow}=%s$'%str(round(plus_length/minus_length, 2)), fontsize=10)
plt.text(750, 1050, r'$\frac{\nearrow}{\searrow}=%s$'%str(plus_length/minus_length), fontsize=10)
plt.scatter(data_graph[0], data_graph[1], s=15, c="red", marker='s', alpha=0.1, linewidth=0)
plt.tick_params(labelsize=5)

plt.tight_layout()
plt.show()
