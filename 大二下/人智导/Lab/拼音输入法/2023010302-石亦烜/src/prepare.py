import json
from settings import *
from pypinyin import lazy_pinyin

#生成拼音-汉字表
def process_word_table(path1:str=PINYIN_WORD_TABLE,path2:str=ALL_WORDS):#path1为拼音汉字表，path2为一二级汉字表
        """
        将拼音-汉字表输出到文件中，生成拼音-汉字表时只考虑一二级汉字表中有的汉字。
        """
        word_table={}
        with open(path2, 'r', encoding='gbk') as f2:
            all_words= f2.read()#读取一二级汉字表
        with open(path1, 'r', encoding='gbk') as f1:
            lines = f1.readlines()#拼音汉字表的每行的列表
        for line in lines:
            temp=[]
            line = line.strip().split(" ")
            for word in line[1:]:
                if word in all_words:#如果拼音汉字表中的汉字在一二级汉字表中，则将其添加到拼音-汉字表中
                    temp.append(word)
            word_table[line[0]] = temp
        #将拼音-汉字表保存到文件中
        with open(WORD_TABLE, 'w', encoding='utf-8') as f:
            json.dump(word_table, f, ensure_ascii=False, indent=4)
        # print('拼音-汉字表生成完成')
        return word_table#返回{<拼音>: [<汉字>, <汉字>, ...], ...}的字典
    
# 生成汉字-拼音表
def process_pinyin_table(word_table:dict)->dict:
        """
        将拼音-汉字表转换为汉字-拼音表
        """
        pinyin_table = {}
        for pinyin, words in word_table.items():#items()方法返回一个包含字典中所有键值对的视图对象
            for word in words:
                if word not in pinyin_table:
                    pinyin_table[word] = pinyin       
        #将汉字-拼音表保存到文件中
        with open(PINYIN_TABLE, 'w', encoding='utf-8') as f:
            json.dump(pinyin_table, f, ensure_ascii=False, indent=4)
        # print('汉字-拼音表生成完成')
        return pinyin_table#返回{<汉字>: <拼音>, ...}的字典

def process_sina(path:str=SINA_NEWS):
        """
        读取新浪语料库，并进行预处理
        """
        #读取新浪语料库，月份从4到11
        for month in range(4,12):
            data=[]
            couple={}
            with open(path % month, 'r', encoding='gbk') as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip()
                content=json.loads(line)
                data.append(content["html"])
                data.append(content["title"])
            # print('读取新浪微博语料库，第%d个月读取完成' % month)
            # print(len(data))
            for sentence in data:
                 pinyin_sentence=lazy_pinyin(sentence,errors=lambda item: ['*' for i in range(len(item))])          
                 couple[sentence]=pinyin_sentence#将句子和拼音对应起来
            with open(PROCESSED_DATA%month, 'w', encoding='utf-8') as f:
                json.dump(couple, f, ensure_ascii=False, indent=4)
            # print('第%d个月预处理完成' % month)
        # print('新浪微博语料库预处理完成')
