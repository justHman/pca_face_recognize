import os
from torch.utils.data import Dataset
import cv2
from datetime import datetime, timedelta
import numpy as np

class face_dataset_ml(Dataset):
    def __init__(self, root, transform=None):
        super().__init__()
        
        self.transform = transform
        self.images, self.labels = [], []
        self.maps = os.listdir(root)
        for label, in4 in enumerate(os.listdir(root)):
            in4_path = os.path.join(root, in4)
            for f in os.listdir(in4_path):  
                f_path = os.path.join(in4_path, f)
                self.images.append(f_path)
                self.labels.append(label)

    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, index):
        label = self.labels[index]
        path = self.images[index]
        data = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if self.transform:
            data = self.transform(data)
        return data, label
    

class face_dataset(Dataset):
    def __init__(self, root, train=True, transform=None):
        super().__init__()
        self.transform = transform 
        if train:
            root_path = os.path.join(root, 'train')
        else:
            root_path = os.path.join(root, 'valid')

        types = ['jpg', 'jpeg']
        self.names = ['Bao', 'Sang', 'Linh', 'Nam', 'Binh', 'Truong', 'Hung', 'Viet', 'Phat']
        self.datas, self.reals, self.labels = [], [], []
        for real, typ in enumerate(os.listdir(root_path)):
            typ_path = os.path.join(root_path, typ)
            for i, name in enumerate(os.listdir(typ_path)):
                name_path = os.path.join(typ_path, name)
                for file in os.listdir(name_path):
                    if file.split('.')[-1] in types:
                        self.datas.append(os.path.join(name_path, file))
                        self.reals.append(real)
                        self.labels.append(i)

    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, index):
        real = self.reals[index]
        label = self.labels[index]
        path = self.datas[index]
        data = cv2.imread(path)
        data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
        if self.transform:
            data = self.transform(data)
        return data, real, label
    
class flood_dataset(Dataset):
    def __init__(self, root, train=True, transform=None):
        super().__init__()
        self.transform = transform 
        if train:
            root_path = os.path.join(root, 'train')
        else:
            root_path = os.path.join(root, 'valid')

        types = ['npy']
        self.datas, self.days, self.durations = [], [], []
        for province in os.listdir(root_path):
            province_path = os.path.join(root_path, province)
            for label in os.listdir(province_path):
                day, duration = label.split('_')
                label_path = os.path.join(province_path, label)
                for file in os.listdir(label_path):
                    if file.split('.')[-1] in types:
                        self.datas.append(os.path.join(label_path, file))
                        d1 = datetime.strptime(day, "%d-%m-%Y")
                        d2 = datetime.strptime("01-01-2000", "%d-%m-%Y")
                        delta = d1 - d2
                        self.days.append(delta.days)
                        self.durations.append(int(duration))

    def __len__(self):
        return len(self.durations)
    
    def __getitem__(self, index):
        day = self.days[index]
        duration = self.durations[index]
        path = self.datas[index]
        data = np.load(path).astype(np.uint8)
        if self.transform:
            data = self.transform(data)
        return data, day, duration
    
if __name__ == '__main__':
    from torchvision.transforms import ToTensor

    dataset = flood_dataset(root='data/tablulars/flood_dataset', train=True, transform=ToTensor())
    print(len(dataset))
    data, day, duration = dataset[0]
    print(data)
    print(data.shape)
    start = datetime.strptime('01-01-2000', "%d-%m-%Y") + timedelta(days=day)
    print(start)
    end = start + timedelta(days=duration)
    print(end)