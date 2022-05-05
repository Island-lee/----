# from pyhanlp import *
# import hanlp
# # 通过 SafeJClass 取得 HanLP 中的 CorpusLoader 类
# CorpusLoader = SafeJClass('com.hankcs.hanlp.corpus.document.CorpusLoader')
# sents = CorpusLoader.convert2SentenceList(r'C:\Users\lab702\Desktop\1.txt')
# for sent in sents:
#     print(sent)

# from pyhanlp import *
# from test_utility import ensure_data
#
# PerceptronNameGenderClassifier = JClass('com.hankcs.hanlp.model.perceptron.PerceptronNameGenderClassifier')
# cnname = ensure_data('cnname', 'http://file.hankcs.com/corpus/cnname.zip')
# TRAINING_SET = os.path.join(cnname, 'train.csv')
# TESTING_SET = os.path.join(cnname, 'test.csv')
# MODEL = cnname + ".bin"

# def run_classifier(averaged_perceptron):
#     print('=====%s=====' % ('平均感知机算法' if averaged_perceptron else '朴素感知机算法'))
#     classifier = PerceptronNameGenderClassifier()
#     print('训练集准确率：', classifier.train(TRAINING_SET, 10, averaged_perceptron))
#     model = classifier.getModel()
#     print('特征数量：', len(model.parameter))
#     # model.save(MODEL, model.featureMap.entrySet(), 0, True)
#     # classifier = PerceptronNameGenderClassifier(MODEL)
#     for name in "赵建军", "沈雁冰", "陆雪琪", "李冰冰":
#         print('%s=%s' % (name, classifier.predict(name)))
#     print('测试集准确率：', classifier.evaluate(TESTING_SET))

# if __name__ == '__main__':
#     run_classifier(False)
#     run_classifier(True)



import pandas as pd
test =pd.read_csv(r'D:\anaconda3\envs\newpytorch1\Lib\site-packages\pyhanlp\static\data\test\cnname\train.csv',header=None)
# print(test.iloc[[0]][1])
# print(test.head())
# for i,line in test.iterrows():
#     if i==10:
#         break
#     print(i,line)

# with open('labelList1.csv', 'w') as f:
#     for i,line in test.iterrows():
#         # if i == 1000:
#         #     break
#         if line[1]=='男':
#             f.write('0 1')
#             f.write('\n')
#         else:
#             f.write('1 0')
#             f.write('\n')

name = ""
for i, line in test.iterrows():
    name += line[0][1:]
a = set(list(name+'_'))
aa = list(a)
# #保存词典
with open('NameList1.txt','w') as f:
    f.writelines(aa)

# 读取词典
# with open('NameList1.txt','r') as f:
#     for t in f:
#         print(t)
#         print(len(t))

#编码
# with open('NameList1.txt','r') as f:
#     for t in f:
#         with open('train1.csv','w')as ft:
#             for i,line in test.iterrows():
#                 if i==1000:
#                     break
#                 temp = [0]*len(t)
#                 if len(line[0])==3:
#                     index1 =t.index(line[0][1])
#                     index2 =t.index(line[0][2])
#                     temp[index1]=1
#                     temp[index2]=1
#                     # print(str(temp))
#                     # print(str(temp)[1:-1])
#                     ft.write(str(temp)[1:-1]+'\n')
#                 if len(line[0])==2:
#                     index1 = t.index(line[0][1])
#                     index2 = t.index('_')
#                     temp[index1]=1
#                     temp[index2]=1
#                     ft.write(str(temp)[1:-1]+'\n')

# with open('train1.csv','r') as f:
    # for t in f:
        # print(t)

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
# train_data = pd.read_csv('train1.csv',header=None)
# train_label =pd.read_csv('labelList2.csv',header=None)

# test_data =1
# test_label =1

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
# test_data = Name(False,img_transform)
BATCH_SIZE = 100
train_data = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=1)
# val_data = DataLoader(val_data, batch_size=BATCH_SIZE, shuffle=False, num_workers=1)

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








