from gensim.models import KeyedVectors
import numpy as np
import torch
import torch.nn as nn
from tqdm import tqdm

def load_word2vec_embeddings(word_table, word2vec_path: str, embedding_dim: int):
    """
    加载预训练词向量并对其词汇表
    """
    print("加载词向量...")
    # 初始化词向量矩阵为零矩阵
    embeddings = np.zeros((len(word_table.keys()) + 1, embedding_dim))
    print(len(word_table.keys()))
    
    word2vec = KeyedVectors.load_word2vec_format(word2vec_path, binary=True)
    for word, idx in tqdm(word_table.items()):
        if word in word2vec:
            embeddings[idx] = word2vec[word]

    embeddings[word_table['<pad>']] = np.zeros(embedding_dim)  # 填充
    embeddings[word_table['<unk>']] = np.zeros(embedding_dim)  # 未定义词
    embeddings_tensor = torch.tensor(embeddings, dtype=torch.float32)
    print("词向量加载完成")
    return embeddings_tensor

class Mydata:
    def __init__(self,path:str):
        self.path=path
        self.word_table={}#存储词汇-索引的字典
        self.sentence_list=[]#存储训练的句子，格式为[(标签，[索引序列]),...]
        
    def build_word_table(self):
        """
        构建词汇-索引的字典，索引从1开始
        """
        with open(self.path,'r',encoding='utf-8')as f:
            lines=f.readlines()
            for line in lines:
                line=line.strip().split('\t')
                label=int(line[0])  # 标签
                sentence=line[1]  # 句子
                line_words=sentence.split(' ')  # 分词
                for word in line_words:
                    if word not in self.word_table:
                        self.word_table[word]=len(self.word_table)+1
        self.word_table['<pad>']=0   #填充
        self.word_table['<unk>']=len(self.word_table)+1   #未定义词
        print("词汇表大小：",len(self.word_table.keys()))
        print("词汇表构建完成")

    def read_data(self):
        """
        读取数据集，返回数据集的列表,格式是[(标签,[索引序列]),...]
        """
        with open(self.path,'r',encoding='utf-8')as f:
            lines=f.readlines()
            for line in tqdm(lines,desc="读取数据集："):
                line=line.strip().split('\t')
                label=int(line[0])  # 标签
                sentence=line[1]  # 句子
                line_words=sentence.split(' ')  # 分词
                sentence=[]
                for word in line_words:
                    if word not in self.word_table:
                        word='<unk>'
                    sentence.append(self.word_table[word])
                self.sentence_list.append((label,sentence))


        