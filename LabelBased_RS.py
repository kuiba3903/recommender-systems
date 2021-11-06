#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/11/6 10:56
# @Author : Xiao Feng
# 基于标签的推荐系统
from math import log
def cal_info(G):
    user_tags = dict()  # 用户打过标签的次数
    tag_items = dict()  # 音乐被打过标签的次数，代表歌曲流行度
    tag_user = dict()  # 标签被用户标记次数
    item_user = dict()  # 音乐被不同用户标记次数
    for key, value in G.items():
        user_tags.setdefault(key, dict())
        for name, tag in value.items():
            user_tags[key].setdefault(tag, 0)
            user_tags[key][tag] += 1

            tag_items.setdefault(tag, dict())
            tag_items[tag].setdefault(name, 0)
            tag_items[tag][name] += 1

            tag_user.setdefault(tag, dict())
            tag_user[tag].setdefault(key, 0)
            tag_user[tag][key] += 1

            item_user.setdefault(name, dict())
            item_user[name].setdefault(key, 0)
            item_user[name][key] += 1

    print("用户打过标签的次数:")
    print(user_tags)
    print("音乐被打过标签的次数:")
    print(tag_items)
    print("标签被用户使用次数: ")
    print(tag_user)
    print("音乐被不同用户标记次数:")
    print(item_user)
    return user_tags,tag_items,tag_user,item_user

def recommend(user,user_tags,tag_items):
    recommend_items = dict()
    for tag,num_tag in user_tags[user].items():
        for item,num_item in tag_items[tag].items():
            if item not in recommend_items:
                recommend_items[item] = num_tag * num_item  # 计算用户对物品兴趣度
            else:
                recommend_items[item] += num_tag * num_item
    rec = sorted(recommend_items.items(), key=lambda x: x[1], reverse=True)  # 将推荐歌曲按兴趣度排名
    print("基于标签的用户对歌曲兴趣度: ", rec)
    return rec

def TagBasedTFIDF(user,user_tags,tag_items,tag_user):
    recommend_items = dict()
    for tag, num_tag in user_tags[user].items():
        for item, num_item in tag_items[tag].items():
            if item not in recommend_items:
                recommend_items[item] = num_tag * num_item/log(1+len(tag_user[tag]))  # 计算用户对物品兴趣度
            else:
                recommend_items[item] += num_tag * num_item/log(1+len(tag_user[tag]))
    rec = sorted(recommend_items.items(), key=lambda x: x[1], reverse=True)  # 将推荐歌曲按兴趣度排名
    print("基于TagBasedTFIDF的用户对歌曲兴趣度: ", rec)
    return rec

def TagBasedTFIDF_add(user,user_tags,tag_items,tag_user,item_user):
    recommend_items = dict()
    for tag, num_tag in user_tags[user].items():
        for item, num_item in tag_items[tag].items():
            if item not in recommend_items:
                recommend_items[item] = num_tag * num_item/(log(1+len(tag_user[tag]))*log(1+len(item_user[item])))  # 计算用户对物品兴趣度
            else:
                recommend_items[item] += num_tag * num_item/(log(1+len(tag_user[tag]))*log(1+len(item_user[item])))
    rec = sorted(recommend_items.items(), key=lambda x: x[1], reverse=True)  # 将推荐歌曲按兴趣度排名
    print("基于TagBasedTFIDF++的用户对歌曲兴趣度: ", rec)
    return rec

if __name__=="__main__":
    G = {
        'A':{"一曲相思":"流行","生僻字":"流行","最后的莫西干人":"纯音乐","倩女幽魂":"经典","突然好想你":"寂寞"},
        'B':{"故乡的原风景":"纯音乐","生僻字":"流行","重头再来":"励志"},
        'C':{"倩女幽魂":"经典","海阔天空":"经典","走西口":"民歌","重头再来":"励志"},
        'D':{"海阔天空":"经典","走西口":"民歌","倩女幽魂":"经典","最后的莫西干人":"纯音乐"}
    }
    user_tags, tag_items,tag_user,item_user = cal_info(G)
    recommend('A',user_tags,tag_items)
    TagBasedTFIDF('A',user_tags, tag_items,tag_user)
    TagBasedTFIDF_add('A',user_tags, tag_items,tag_user,item_user)
