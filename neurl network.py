import pandas as pd
test =pd.read_csv(r'D:\anaconda3\envs\newpytorch1\Lib\site-packages\pyhanlp\static\data\test\cnname\train.csv',header=None)
name = ""
for i, line in test.iterrows():
    name += line[0][1:]
a = set(list(name+'_'))
aa = list(a)

# #保存词典
with open('NameList1.txt','w') as f:
    f.writelines(aa)

#建立网络
import torch
import torch.nn as nn
from torch.utils.data import Dataset
import numpy
from torchvision.transforms import transforms
from torch.utils.data import DataLoader
from torch import optim
from torch.autograd import Variable


class Perceptron(nn.Module):
    def __init__(self):
        super(Perceptron, self).__init__()
        self.linear = nn.Linear(5496,64)
        self.linear2 = nn.Linear(64, 2)
        self.relu = nn.ReLU(inplace=True)
    def forward(self,x):
        # print(x,x.shape)
        x = torch.reshape(x, (100, -1))
        # print(x, x.shape)
        x = self.linear(x)
        output = self.linear2(x)
        return output

def img_transform(img, label):
    label = numpy.array(label)
    img = torch.tensor(img)
    label = torch.from_numpy(label)
    return img, label,

def one_hot(line,t):
    temp = [0]*len(t)
    if len(line[0])==3:
        index1 =t.index(line[0][1])
        index2 =t.index(line[0][2])
        temp[index1]=1
        temp[index2]=1
    if len(line[0])==2:
        index1 = t.index(line[0][1])
        index2 = t.index('_')
        temp[index1]=1
        temp[index2]=1
    # print(line[1],type(line[1]))
    if line[1]=='男':
        label = [0,1]
    else:
        label = [1,0]
    return temp,label

class Name(Dataset):
    def __init__(self,train=True,transform=None):
        test = pd.read_csv(r'D:\anaconda3\envs\newpytorch1\Lib\site-packages\pyhanlp\static\data\test\cnname\train.csv',
                           header=None)
        self.train = train
        self.traindata =test
        # self.testdata = test_data
        # self.testlabel = test_label
        if self.train:
            self.data = self.traindata
        # else:
        #     self.data = self.testdata
        #     self.labels = self.testlabel
        self.transform = transform
        with open('NameList1.txt', 'r') as f:
            for t in f:
                self.Namelist = t
    def __getitem__(self, index):
        # data = self.data.iloc[index:index+1].values
        # print(self.data.iloc[[index]].values)
        data = self.data.iloc[[index]].values
        data, label = one_hot(data[0], self.Namelist)

        data, label = self.transform(data, label)
        sample = {'data': data, 'label': label}
        return sample

    def __len__(self):
        return int(len(self.data))

train_data = Name(True,img_transform)

BATCH_SIZE = 100
train_data = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=1)

def main():
    net = Perceptron()
    net = net.cuda()
    criterion = nn.MSELoss().cuda()
    optimizer = optim.Adam(net.parameters(), lr=1e-4)

    print('-----------------------train-----------------------')

    for epoch in range(20):
        if epoch % 10 == 0 and epoch != 0:
            for group in optimizer.param_groups:
                group['lr'] *= 0.5
        for i, sample in enumerate(train_data):
            # imgdata2 = Variable(sample['img'].float().cuda())
            imgdata1 = Variable(sample['data'].float().cuda())
            imglabel = Variable(sample['label'].float().cuda())
            optimizer.zero_grad()
            out = net(imgdata1)
            loss = criterion(out, imglabel)
            print(loss)
            loss.backward()
            optimizer.step()
    torch.save(net.state_dict(),'1.tar')

if __name__ == '__main__':
    main()
    net = Perceptron()
    net.load_state_dict(torch.load('1.tar'))
    net = net.cuda()
    with open('NameList1.txt', 'r') as f:
        for t in f:
            temp = [0] * len(t)
            index1 = t.index('智')
            index2 = t.index('瑞')
            temp[index1] = 1
            temp[index2] = 1
    temp = [temp for i in range(100)]
    # print(temp,len(temp))
    variablex = torch.tensor(temp, dtype=torch.float32)
    variablex = variablex.float().cuda()
    ans = net(variablex)
    ans = ans.max(dim=1)[1].cpu().numpy()
    if ans[0]==0:
        print('结果预测为：女')
    else:
        print('结果预测为：男')








