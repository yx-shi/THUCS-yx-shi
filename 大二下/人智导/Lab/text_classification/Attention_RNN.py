import torch
import torch.nn as nn
import math

class Attention(nn.Module):
    """
    Attention 模块，用于计算注意力权重并加权求和
    """
    def __init__(self, hidden_dim):
        super(Attention, self).__init__()
        self.attention = nn.Linear(hidden_dim, 1, bias=False) 

    def forward(self, rnn_out):
        # 计算注意力分数 (batch_size, seq_len, 1)
        attn_scores = self.attention(rnn_out).squeeze(2)
        attn_weights = torch.softmax(attn_scores, dim=1)  
        # 加权求和 (batch_size, hidden_dim)
        context = torch.bmm(attn_weights.unsqueeze(1), rnn_out).squeeze(1)
        return context, attn_weights


class AttentionRNN(nn.Module):
    """
    带 Attention 的 RNN 模型
    """
    def __init__(self, vocab_size, embedding_dim, hidden_dim, label_num, num_layers=1, dropout_rate=0.5, pretrained_embeddings=None):
        super(AttentionRNN, self).__init__()
        self.num_layers = num_layers
        self.hidden_dim = hidden_dim
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        if pretrained_embeddings is not None:
            self.embedding.weight = nn.Parameter(pretrained_embeddings)
            self.embedding.weight.requires_grad = False  # 冻结词向量
        self.rnn = nn.RNN(
            input_size=embedding_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout_rate if num_layers > 1 else 0
        )
        self.attention = Attention(hidden_dim)
        self.fc = nn.Linear(hidden_dim, label_num)
        self.dropout = nn.Dropout(dropout_rate)

    def forward(self, x):
        x = self.embedding(x)  # (batch_size, seq_len, embedding_dim)
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).to(x.device)
        rnn_out, hidden = self.rnn(x, h0)  # rnn_out: (batch_size, seq_len, hidden_dim)
        context, attn_weights = self.attention(rnn_out)  # context: (batch_size, hidden_dim)
        context = self.dropout(context)
        output = self.fc(context)  # (batch_size, label_num)
        return output