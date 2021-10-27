from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import pearsonr
import numpy as np
import pandas as pd

i = [1,0,0,0]
j = [1,0.5,0.5,0]
# 余弦相似度
print(cosine_similarity([i,j]))
# 皮尔逊相关系数
#     r : float
#         Pearson's correlation coefficient.
#     p-value : float
#         Two-tailed p-value.
print(pearsonr(i,j))

# 用户对4中物品的打分
users = [[5,3,4,4],
         [3,1,2,3],
         [4,3,4,3],
         [3,3,1,5],
         [1,5,5,2]]
print(cosine_similarity(users))# 余弦相似性
print(np.corrcoef(users))# 皮尔逊相关系数

print("-----------------------")
# 定义数据集， 也就是那个表格， 注意这里我们采用字典存放数据， 因为实际情况中数据是非常稀疏的， 很少有情况是现在这样
def loadData():
    items={'A': {1: 5, 2: 3, 3: 4, 4: 3, 5: 1},
           'B': {1: 3, 2: 1, 3: 3, 4: 3, 5: 5},
           'C': {1: 4, 2: 2, 3: 4, 4: 1, 5: 5},
           'D': {1: 4, 2: 3, 3: 3, 4: 5, 5: 2},
           'E': {2: 3, 3: 5, 4: 4, 5: 1}
          }
    users={1: {'A': 5, 'B': 3, 'C': 4, 'D': 4},
           2: {'A': 3, 'B': 1, 'C': 2, 'D': 3, 'E': 3},
           3: {'A': 4, 'B': 3, 'C': 4, 'D': 3, 'E': 5},
           4: {'A': 3, 'B': 3, 'C': 1, 'D': 5, 'E': 4},
           5: {'A': 1, 'B': 5, 'C': 5, 'D': 2, 'E': 1}
          }
    return items,users

items, users = loadData()
item_df = pd.DataFrame(items).T
user_df = pd.DataFrame(users).T
print(item_df)
print(user_df)
# 计算用户的相似度
similarity_matrix = pd.DataFrame(np.zeros((len(users),len(users))),index=[1,2,3,4,5],columns=[1,2,3,4,5])
# print(similarity_matrix)
# 遍历每条用户-物品评分数据
for user_id in users:
    for otheruser_id in users:
        vec_user = []
        vec_otheruser = []
        if user_id != otheruser_id:
            for item in items:# 遍历物品-用户评分数据
                itemRatings = items[item]# 返回一个字典

                if user_id in itemRatings and otheruser_id in itemRatings:
                    vec_user.append(itemRatings[user_id])
                    vec_otheruser.append(itemRatings[otheruser_id])
            # 这里可以获得相似性矩阵(共现矩阵)
            similarity_matrix[user_id][otheruser_id] = np.corrcoef(np.array(vec_user), np.array(vec_otheruser))[0][1]
            # similarity_matrix[userID][otheruserId] = cosine_similarity(np.array(vec_user), np.array(vec_otheruser))[0][1]
print(similarity_matrix)
print("-----------------------")

# 计算前n个相似的用户
n = 2
similarity_users = similarity_matrix[1].sort_values(ascending=False)[:n].index.to_list()
print(similarity_users)

"""计算最终得分"""
base_score = np.mean(np.array([value for value in users[1].values()]))
weighted_scores = 0.
corr_values_sum = 0.
for user in similarity_users:  # [2, 3]
    corr_value = similarity_matrix[1][user]            # 两个用户之间的相似性
    mean_user_score = np.mean(np.array([value for value in users[user].values()]))    # 每个用户的打分平均值
    weighted_scores += corr_value * (users[user]['E']-mean_user_score)      # 加权分数
    corr_values_sum += corr_value
final_scores = base_score + weighted_scores / corr_values_sum
print('用户Alice对物品5的打分: ', final_scores)
user_df.loc[1]['E'] = final_scores
print(user_df)
