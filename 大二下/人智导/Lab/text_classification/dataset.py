from torch.utils.data import Dataset
      

class Mydataset(Dataset):
    def __init__(self,sentence_list:list):
        self.sentence_list=sentence_list

    def __len__(self):
        return len(self.sentence_list)
    
    def __getitem__(self,index:int):
        label,sentence=self.sentence_list[index]
        return sentence,label
        