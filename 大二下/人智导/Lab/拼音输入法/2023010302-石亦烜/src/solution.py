from settings import *
import math
import json

def log(i):
    if i>=0:
        return math.log(i+1e-5)
    else:
        raise KeyError


def get_uni_frequency(uni_frequency:dict):
    """
    把所给的频率表转为{<汉字>:频率}的字典
    """
    word1_frequency = {}
    for pinyin in uni_frequency:
        for i in range(len(uni_frequency[pinyin]["words"])):
            word = uni_frequency[pinyin]["words"][i]
            count = float(uni_frequency[pinyin]["counts"][i])
            if word not in word1_frequency:
                word1_frequency[word] = count
            else:
                word1_frequency[word] += count
    return word1_frequency

def get_binary_frequency(binary_frequency:dict):
    """
    把所给的二元词频表转为{<汉字 汉字>:频率}的字典
    """
    word2_frequency = {}
    for pinyin in binary_frequency:
        for i in range(len(binary_frequency[pinyin]["words"])):
            word = binary_frequency[pinyin]["words"][i]
            count = float(binary_frequency[pinyin]["counts"][i])
            if word not in word2_frequency:
                word2_frequency[word] = count
            else:
                word2_frequency[word] += count
    return word2_frequency

def get_tri_frequency(tri_frequency:dict):
    """
    把所给的三元词频表转为{<汉字 汉字 汉字>:频率}的字典
    """
    word3_frequency = {}
    for pinyin in tri_frequency:
        for i in range(len(tri_frequency[pinyin]["words"])):
            word = tri_frequency[pinyin]["words"][i]
            count = float(tri_frequency[pinyin]["counts"][i])
            if word not in word3_frequency:
                word3_frequency[word] = count
            else:
                word3_frequency[word] += count
    return word3_frequency

def Viterbi(sentence:str,my_uni_frequency:dict,my_bi_frequency:dict,word_table:dict,para):
    """维特比算法实现拼音输入法，搜索最可能得汉字序列"""
    new_sentence=sentence.split()#把输入的拼音序列分割成单个拼音的列表
    n = len(new_sentence)

    # 初始化动态规划表和路径表
    dp=[{} for _ in range(n)]#动态规划表，存储每个拼音对应的汉字和概率
    path=[{} for _ in range(n)]#路径表，存储每个拼音对应的汉字和前一个拼音的索引

    # 初始化第一个拼音的概率和路径
    first_word=''
    for word in new_sentence:
        if word in word_table:
            first_word=word
            break
    if first_word == '':
        return ''
    for word in word_table[first_word]:
        now_frequency = my_uni_frequency.get(word,0.0)#获取当前拼音的频率
        if now_frequency <= 0.0:
            continue
        dp[0][word] = log(now_frequency)-log(para) 
        path[0][word] = ''#前一个拼音的索引为空

    for i in range(1, n):
        for last_word in dp[i-1]:
            last_frequency = my_uni_frequency.get(last_word,0.0)#获取前一个拼音的频率,若不存在则为0
            if last_frequency <= 0.0:
                continue
            for now_word in word_table[new_sentence[i]]:
                # 计算当前拼音的概率
                now_frequency = my_uni_frequency.get(now_word,0.0)#获取当前拼音的频率
                if now_frequency <= 0.0:
                    continue
                now_bi_frequency = my_bi_frequency.get(last_word + ' ' + now_word,0.0)#获取二元组的频率
                p =ALPHA*now_bi_frequency/last_frequency+(1.0-ALPHA)*now_frequency/para
                # if p > 1:
                #     print(last_word, now_word)
                #     print(ALPHA, now_bi_frequency, last_frequency, now_frequency, para)
                #     exit(0)
                if now_word not in dp[i]:
                    dp[i][now_word] = dp[i-1][last_word] + log(p)
                    path[i][now_word] = last_word
                elif dp[i-1][last_word] + log(p) > dp[i][now_word]:
                    dp[i][now_word] = dp[i-1][last_word] + log(p)
                    path[i][now_word] = last_word

    # 找到最后一个拼音的最大概率和对应的汉字
    max_prob = float('-inf')
    best_word =''#初始化为第一个汉字
    for word in dp[-1]:
        if dp[-1][word] > max_prob:
            max_prob = dp[-1][word]
            best_word = word

    # with open("./dp.json", 'w', encoding='utf-8') as f:
    #      f.write(str(dp))
    # 回溯路径，找到最优的汉字序列
    best_path = ""
    for i in range(n-1, -1, -1):
        # print(dp[i][best_word])
        best_path = best_word + best_path
        best_word = path[i][best_word]
    return best_path#返回最优的汉字序列


def Viterbi_3gram(sentence:str,my_uni_frequency:dict,my_bi_frequency:dict,my_tri_frequency:dict,word_table:dict,para):
    """维特比算法实现拼音输入法，搜索最可能得汉字序列"""
    new_sentence=sentence.split()#把输入的拼音序列分割成单个拼音的列表
    n = len(new_sentence)
    # 初始化动态规划表和路径表
    dp=[{} for _ in range(n)]#动态规划表，存储每个拼音对应的汉字和概率
    path=[{} for _ in range(n)]#路径表，存储每个拼音对应的汉字和前一个拼音的索引
    for word in word_table[new_sentence[0]]:
        first_frequency = my_uni_frequency.get(word,0.0)#获取当前拼音的频率
        if first_frequency <= 0.0:
            continue
        dp[0][word] = log(first_frequency)-log(para)
        path[0][word] = ''#前一个拼音的索引为空
        for second_word in word_table[new_sentence[1]]:
            second_frequency=my_uni_frequency.get(second_word,0.0)#获取当前拼音的频率
            bi_frequency=my_bi_frequency.get(word +' ' + second_word,0.0)#获取二元组的频率
            if second_frequency <= 0.0:
                continue
            p =ALPHA*bi_frequency/first_frequency+(1.0-ALPHA)*second_frequency/para
            if second_word not in dp[1]:
                dp[1][second_word] = dp[0][word] + log(p)
                path[1][second_word] = word
            elif dp[0][word] + log(p) > dp[1][second_word]:
                dp[1][second_word] = dp[0][word] + log(p)
                path[1][second_word] = word

    for i in range(2, n):
        for first_word in dp[i-2]:
            for second_word in dp[i-1]:
                last_bi_frequency = my_bi_frequency.get(first_word +' ' + second_word,0.0)#获取二元组的频率
                second_frequency=my_uni_frequency.get(second_word,0.0)#获取当前拼音的频率
                if last_bi_frequency <= 0.0 or second_frequency <= 0.0:
                    continue
                for now_word in word_table[new_sentence[i]]:
                    # 计算当前拼音的概率
                    now_frequency = my_uni_frequency.get(now_word,0.0)#获取当前拼音的频率
                    now_bi_frequency = my_bi_frequency.get(second_word +' ' + now_word,0.0)#获取当前二元组的频率
                    if now_frequency <= 0.0:
                        continue
                    now_tri_frequency = my_tri_frequency.get(first_word +' ' + second_word +' ' + now_word,0.0)#获取三元组的频率
                    p =LAMBDA*now_tri_frequency/last_bi_frequency+(1.0-LAMBDA)*(ALPHA*now_bi_frequency/second_frequency+(1.0-ALPHA)*now_frequency/para)
                    if now_word not in dp[i]:
                        dp[i][now_word] = dp[i-1][second_word] + log(p)
                        path[i][now_word] = second_word
                    elif dp[i-1][second_word] + log(p) > dp[i][now_word]:
                        dp[i][now_word] = dp[i-1][second_word] + log(p)
                        path[i][now_word] = second_word

    # 找到最后一个拼音的最大概率和对应的汉字
    max_prob = float('-inf')
    best_word =''#初始化为第一个汉字
    for word in dp[-1]:
        if dp[-1][word] > max_prob:
            max_prob = dp[-1][word]
            best_word = word

    best_path = ""
    for i in range(n-1, -1, -1):
        # print(dp[i][best_word])
        best_path = best_word + best_path
        best_word = path[i][best_word]
    return best_path#返回最优的汉字序列