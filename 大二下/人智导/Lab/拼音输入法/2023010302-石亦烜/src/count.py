import json
from settings import *
import tqdm

def count_frequency(path:str=PROCESSED_DATA) -> tuple:
    """
    统计句子中每个拼音的一元词频和二元词频，返回两个字典。
    :param couple: {<句子>: <拼音序列>} 的字典
    :return: (一元词频字典, 二元词频字典)
    """
    uni_frequency = {}
    bi_frequency = {}
    for month in range(4,12):
        couple = {}
        with open(path % month, 'r', encoding='utf-8') as f:
            couple = json.load(f)
    #测试
    # couple={}
    # with open("./test.json",'r',encoding='utf-8')as f:
    #     couple=json.load(f)
        for sentence, pinyin_sentence in tqdm.tqdm(couple.items(), desc="统计词频", unit="句子"):
            for i in range(len(sentence)):
                # 处理一元词频 
                pinyin = pinyin_sentence[i]
                word = sentence[i]
                if pinyin=='*':
                    continue
                if pinyin not in uni_frequency:
                    uni_frequency[pinyin] = {"words": [], "counts": []}
                if word in uni_frequency[pinyin]["words"]:
                    index = uni_frequency[pinyin]["words"].index(word)
                    uni_frequency[pinyin]["counts"][index] += 1
                else:
                    uni_frequency[pinyin]["words"].append(word)
                    uni_frequency[pinyin]["counts"].append(1)

                # 处理二元词频
                if i < len(sentence) - 1:  # 确保不越界
                    if pinyin_sentence[i + 1] == '*':
                        continue
                    bi_pinyin = pinyin_sentence[i] + ' ' + pinyin_sentence[i + 1]
                    bi_word = sentence[i] + ' ' + sentence[i + 1]
                    if bi_pinyin not in bi_frequency:
                        bi_frequency[bi_pinyin] = {"words": [], "counts": []}
                    if bi_word in bi_frequency[bi_pinyin]["words"]:
                        index = bi_frequency[bi_pinyin]["words"].index(bi_word)
                        bi_frequency[bi_pinyin]["counts"][index] += 1
                    else:
                        bi_frequency[bi_pinyin]["words"].append(bi_word)
                        bi_frequency[bi_pinyin]["counts"].append(1)

    with open(UNI_WORD, 'w', encoding='utf-8') as f:
        json.dump(uni_frequency, f, ensure_ascii=False, indent=4)
    with open(BI_WORD, 'w', encoding='utf-8') as f:
        json.dump(bi_frequency, f, ensure_ascii=False, indent=4)
    # with open("./test_1word", 'w', encoding='utf-8') as f:
    #     json.dump(uni_frequency, f, ensure_ascii=False, indent=4)
    # with open("./test_2_word", 'w', encoding='utf-8') as f:
    #     json.dump(bi_frequency, f, ensure_ascii=False, indent=4)
    return uni_frequency, bi_frequency
    
def count_3gram_frequency(path:str=PROCESSED_DATA) -> tuple:
    """
    统计句子中每个拼音的三元词频，返回一个字典。
    :param couple: {<句子>: <拼音序列>} 的字典"
    """
    three_gram_frequency = {}
    for month in range(4,12):
        couple = {}
        with open(path % month, 'r', encoding='utf-8') as f:
            couple = json.load(f)
        for sentence, pinyin_sentence in tqdm.tqdm(couple.items(), desc="统计三元词频", unit="句子"):
            for i in range(len(sentence)):
                # 处理三元词频
                if i < len(sentence) - 2:  # 确保不越界
                    if pinyin_sentence[i]=='*' or pinyin_sentence[i + 1] == '*' or pinyin_sentence[i + 2] == '*':
                        continue
                    else:
                        three_pinyin = pinyin_sentence[i] +' ' + pinyin_sentence[i + 1] +' ' + pinyin_sentence[i + 2]
                        three_word = sentence[i] +' ' + sentence[i + 1] +' ' + sentence[i + 2]
                        if three_pinyin not in three_gram_frequency:
                            three_gram_frequency[three_pinyin] = {"words": [], "counts": []}
                        if three_word in three_gram_frequency[three_pinyin]["words"]:
                            index = three_gram_frequency[three_pinyin]["words"].index(three_word)
                            three_gram_frequency[three_pinyin]["counts"][index] += 1
                        else:
                            three_gram_frequency[three_pinyin]["words"].append(three_word)
                            three_gram_frequency[three_pinyin]["counts"].append(1)
    with open("./sets/3_word.json", 'w', encoding='utf-8') as f:
        json.dump(three_gram_frequency, f, ensure_ascii=False, indent=4)
