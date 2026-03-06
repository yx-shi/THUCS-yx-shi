import torch
import torch.nn as nn

class RNN(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, label_num, num_layers=1, dropout_rate=0.5, pretrained_embeddings=None):
        super(RNN, self).__init__()
        self.num_layers=num_layers
        self.hidden_size=hidden_dim
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        if pretrained_embeddings is not None:
            self.embedding.weight = nn.Parameter(pretrained_embeddings)
            self.embedding.weight.requires_grad = False  # 冻结词向量
        self.rnn = nn.RNN(
            input_size=embedding_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            bias=True,
            batch_first=True,
            dropout=dropout_rate if num_layers > 1 else 0  # 如果只有 1 层，不使用 dropout
        )
        self.fc = nn.Linear(hidden_dim, label_num)
        self.dropout = nn.Dropout(dropout_rate)
    def forward(self, x):
        x = self.embedding(x)  # (batch_size, seq_len, embedding_dim)
        h0=torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        rnn_out, hidden = self.rnn(x,h0) # rnn_out: (batch_size, seq_len, hidden_dim)
        pooled,_ = torch.max(rnn_out, dim=1)  # 最大池化
        pooled = self.dropout(pooled)
        output = self.fc(pooled)
        # # Dropout
        # last_hidden = hidden[-1]  # 取最后一层的隐藏状态 (batch_size, hidden_dim)
        # last_hidden = self.dropout(last_hidden)
        # # 全连接层
        # output = self.fc(last_hidden)  # (batch_size, label_num)
        return output


class LSTM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, label_num, num_layers=1, dropout_rate=0.5, pretrained_embeddings=None):
        super(LSTM, self).__init__()
        self.num_layers = num_layers
        self.hidden_size = hidden_dim
        self.bidirectional = True  # 启用双向 LSTM
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        if pretrained_embeddings is not None:
            self.embedding.weight = nn.Parameter(pretrained_embeddings)
            self.embedding.weight.requires_grad = False  # 冻结词向量
        self.lstm = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            bias=True,
            batch_first=True,
            dropout=dropout_rate if num_layers > 1 else 0,
            bidirectional=self.bidirectional  # 启用双向
        )
        self.fc = nn.Linear(hidden_dim * 2, label_num)
        self.dropout = nn.Dropout(dropout_rate)

    def forward(self, x):
        x = self.embedding(x)  # (batch_size, seq_len, embedding_dim)

        # 初始化 LSTM 的隐藏状态和细胞状态
        h0 = torch.zeros(self.num_layers * 2, x.size(0), self.hidden_size).to(x.device)  # 双向 LSTM 的层数是 num_layers * 2
        c0 = torch.zeros(self.num_layers * 2, x.size(0), self.hidden_size).to(x.device)
        lstm_out, (hidden, cell) = self.lstm(x, (h0, c0))  # lstm_out: (batch_size, seq_len, hidden_dim * 2)
        last_hidden_forward = hidden[-2]  
        last_hidden_backward = hidden[-1]  
        last_hidden = torch.cat((last_hidden_forward, last_hidden_backward), dim=1)  # 拼接正向和反向的隐藏状态 (batch_size, hidden_dim * 2)
        last_hidden = self.dropout(last_hidden)
        output = self.fc(last_hidden)  # (batch_size, label_num)
        return output