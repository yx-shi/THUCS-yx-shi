import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence
from sklearn.metrics import accuracy_score, f1_score
from dataset import Mydataset
from data_reader import Mydata,load_word2vec_embeddings
from CNN import CNN
from RNN import RNN, LSTM
from Attention_RNN import AttentionRNN
from MLP import MLP
import argparse  



def collate_fn(batch):
    """
    自定义数据加载器的 collate_fn 函数
    """
    sentences, labels = zip(*batch)
    sentences = [torch.tensor(sentence, dtype=torch.long) for sentence in sentences]
    labels = torch.tensor(labels, dtype=torch.long)
    max_kernel_size = max([3, 4, 5])  
    sentences = [torch.cat([torch.zeros(max(0, max_kernel_size - len(sentence)), dtype=torch.long), sentence]) for sentence in sentences]
    sentences = pad_sequence(sentences, batch_first=True, padding_value=0)
    return sentences, labels


def train_model(model, train_loader, val_loader, criterion, optimizer, device, epochs=10, patience=3):
    """
    epochs: 最大训练轮数
    patience: 早停的容忍次数
    """
    model.to(device)
    best_val_f1 = 0.0  # 保存验证集的最佳 F1 分数
    best_model_state = None  # 保存最佳模型的状态
    patience_counter = 0 


    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for sentences, labels in train_loader:
            sentences, labels = sentences.to(device), labels.to(device)
            outputs = model(sentences)
            loss = criterion(outputs, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        # 打印训练损失和验证集性能
        print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(train_loader):.4f}")
        val_acc, val_f1 = evaluate_model(model, val_loader, device, return_metrics=True)
        print(f"Validation Accuracy: {val_acc:.4f}, F1 Score: {val_f1:.4f}")
        if val_f1 > best_val_f1:
            best_val_f1 = val_f1
            best_model_state = model.state_dict()  # 保存当前模型状态
            patience_counter = 0  
            print("Validation F1 improved, saving the model...")
        else:
            patience_counter += 1
            print(f"No improvement in validation F1 for {patience_counter} epoch(s).")
        
        # 检查是否需要早停
        if patience_counter >= patience:
            print("Early stopping triggered.")
            break

    # 加载验证集效果最好的模型
    if best_model_state is not None:
        model.load_state_dict(best_model_state)
        print("Loaded the best model based on validation performance.")



def evaluate_model(model, data_loader, device, return_metrics=False):
    """
    return_metrics: 表示是否返回性能指标
    """
    model.eval()
    all_preds = []
    all_labels = []
    with torch.no_grad():
        for sentences, labels in data_loader:
            sentences, labels = sentences.to(device), labels.to(device)
            outputs = model(sentences)
            preds = torch.argmax(outputs, dim=1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    acc = accuracy_score(all_labels, all_preds)
    f1 = f1_score(all_labels, all_preds, average='binary')
    if return_metrics:
        return acc, f1
    else:
        print("测试结果为：")
        print(f"Accuracy: {acc:.4f}, F1 Score: {f1:.4f}")


def main():
    # 添加命令行参数解析
    parser = argparse.ArgumentParser(description="Text Classification with Different Models")
    parser.add_argument('--model', '-m',default='CNN',type=str, choices=['CNN', 'RNN', 'LSTM', 'AttentionRNN', 'MLP'],
                        help="Choose the model to use: CNN, RNN, LSTM, AttentionRNN, or MLP")
    args = parser.parse_args()

    # 数据路径和参数
    train_data_path = "/root/code/Python/text_classification/data/train.txt"   # 训练集
    valid_data_path = "/root/code/Python/text_classification/data/validation.txt"   # 验证集
    test_data_path = "/root/code/Python/text_classification/data/test.txt"   # 测试集
    word2vec_path = "/root/code/Python/text_classification/data/wiki_word2vec_50.bin"
    embedding_dim = 50
    batch_size = 32
    num_classes = 2
    kernel_sizes = [3, 4, 5]
    num_filters = 100
    dropout_rate = 0.3
    learning_rate = 0.0005
    epochs = 30
    patience = 10
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # device=torch.device("cpu")
    
    # 构建训练集
    train_data_reader = Mydata(train_data_path)
    train_data_reader.build_word_table()
    train_data_reader.read_data()
    
    # 构建验证集
    valid_data_reader = Mydata(valid_data_path)
    valid_data_reader.word_table = train_data_reader.word_table  # 使用相同的词汇表
    valid_data_reader.read_data()
    
    # 构建测试集
    test_data_reader = Mydata(test_data_path)
    test_data_reader.word_table = train_data_reader.word_table  # 使用相同的词汇表
    test_data_reader.read_data()
    
    # 加载预训练词向量
    pretrained_embeddings = load_word2vec_embeddings(train_data_reader.word_table, word2vec_path, embedding_dim)
    train_dataset = Mydataset(train_data_reader.sentence_list)
    valid_dataset = Mydataset(valid_data_reader.sentence_list)
    test_dataset = Mydataset(test_data_reader.sentence_list)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, collate_fn=collate_fn)
    val_loader = DataLoader(valid_dataset, batch_size=batch_size, shuffle=False, collate_fn=collate_fn)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, collate_fn=collate_fn)
    
    # 根据命令行参数选择模型
    if args.model == 'CNN':
        model = CNN(
            vocab_size=len(train_data_reader.word_table),
            embedding_dim=embedding_dim,
            label_num=num_classes,
            kernel_sizes=kernel_sizes,
            num_filters=num_filters,
            dropout_rate=dropout_rate,
            pretrained_embeddings=torch.tensor(pretrained_embeddings, dtype=torch.float)
        )
    elif args.model == 'RNN':
        model = RNN(
            vocab_size=len(train_data_reader.word_table),
            embedding_dim=embedding_dim,
            hidden_dim=128,
            label_num=num_classes,
            num_layers=1,
            dropout_rate=dropout_rate,
            pretrained_embeddings=torch.tensor(pretrained_embeddings, dtype=torch.float)
        )
    elif args.model == 'LSTM':
        model = LSTM(
            vocab_size=len(train_data_reader.word_table),
            embedding_dim=embedding_dim,
            hidden_dim=64,
            label_num=num_classes,
            num_layers=3,
            dropout_rate=dropout_rate,
            pretrained_embeddings=torch.tensor(pretrained_embeddings, dtype=torch.float)
        )
    elif args.model == 'AttentionRNN':
        model = AttentionRNN(
            vocab_size=len(train_data_reader.word_table),
            embedding_dim=embedding_dim,
            hidden_dim=256,
            label_num=num_classes,
            num_layers=2,
            dropout_rate=dropout_rate,
            pretrained_embeddings=torch.tensor(pretrained_embeddings, dtype=torch.float)
        )
    elif args.model == 'MLP':
        model = MLP(
            vocab_size=len(train_data_reader.word_table),
            embedding_dim=embedding_dim,
            hidden_dim=128,
            label_num=num_classes,
            dropout_rate=dropout_rate,
            pretrained_embeddings=torch.tensor(pretrained_embeddings, dtype=torch.float)
        )
    else:
        raise ValueError("Invalid model name. Choose from: CNN, RNN, LSTM, AttentionRNN, MLP")
    
    # 定义损失函数和优化器
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    print(f"开始训练模型: {args.model}...")
    train_model(model, train_loader, val_loader, criterion, optimizer, device, epochs, patience)
    print(f"开始测试模型: {args.model}...")
    evaluate_model(model, test_loader, device)

if __name__ == "__main__":
    main()