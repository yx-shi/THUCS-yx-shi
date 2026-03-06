import torch
import torch.nn as nn

class MLP(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, label_num, dropout_rate=0.5, pretrained_embeddings=None):
        super(MLP, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        if pretrained_embeddings is not None:
            self.embedding.weight = nn.Parameter(pretrained_embeddings)
            self.embedding.weight.requires_grad = False  # 冻结词向量
        self.fc1 = nn.Linear(embedding_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, label_num)
        self.dropout = nn.Dropout(dropout_rate)
        self.relu = nn.ReLU()
    def forward(self, x):
        x = self.embedding(x)  # (batch_size, seq_len, embedding_dim)
        hidden=self.relu(self.fc1(x.mean(dim=1)))
        hidden=self.dropout(hidden)
        output = self.fc2(hidden)  # (batch_size, label_num)
        return output

        