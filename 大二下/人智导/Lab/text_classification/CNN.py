from gensim.models import KeyedVectors
from data_reader import load_word2vec_embeddings
import tqdm
import numpy as np
import torch
import torch.nn as nn


class CNN(nn.Module):
    def __init__(self, vocab_size, embedding_dim, label_num, kernel_sizes, num_filters, dropout_rate,pretrained_embeddings=None):
        super(CNN, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        if pretrained_embeddings is not None:
            self.embedding.weight = nn.Parameter(pretrained_embeddings)
            self.embedding.weight.requires_grad = False  # 冻结词向量
        self.cnn_layers=nn.ModuleList()
        for k_size in kernel_sizes:
            self.cnn_layers.append(nn.Conv2d(1, num_filters, (k_size,embedding_dim)))
        self.dropout=nn.Dropout(dropout_rate)
        self.fc = nn.Linear(len(kernel_sizes) * num_filters, label_num)
        self.relu=nn.ReLU()

    def forward(self, x):
        x=self.embedding(x)  # (batch_size, seq_len, embedding_dim)
        x = x.unsqueeze(1)  # 变为 (batch_size, 1, seq_len, embedding_dim)
        conved=[]
        for cnn in self.cnn_layers:
            conved.append(self.relu(cnn(x)).squeeze(3))# (batch_size, num_filters, seq_len - kernel_size + 1)
        pooled = [torch.max_pool1d(i, i.size(2)).squeeze(2) for i in conved]  # 输出形状 (batch_size, num_filters)
        x = torch.cat(pooled, 1)  #输出形状 (batch_size, len(kernel_sizes) * num_filters)
        x = self.dropout(x)
        x = self.fc(x)            
        return x