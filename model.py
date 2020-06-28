import numpy as np
import matplotlib.pyplot as plt
import torch as t
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as feeder
import torch.optim as optim
import torch.utils.data as data_utils

use_gpu = t.cuda.is_available()
print("GPU Available: {}".format(use_gpu))


class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.conv1 = nn.Conv2d(1, 4, 3, padding=1)
        self.conv2 = nn.Conv2d(4, 4, 7, padding=3)
        self.pooling = nn.MaxPool2d(11, stride=1, padding=5)
        self.conv3 = nn.Conv2d(4, 3, 11, padding=5)
        # self.conv4 = nn.Conv2d(4, 4, 15, padding=7)
        # self.conv5 = nn.Conv2d(4, 3, 19, padding=9)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pooling(x)
        x = F.relu(self.conv2(x))
        x = self.pooling(x)
        x = F.relu(self.conv3(x))
        # x = F.relu(self.conv4(x))
        # x = F.relu(self.conv5(x))
        return x


if __name__ == "__main__":
    model = Model()
    if t.cuda.is_available():  # verifies if gpu is available on the current machine
        model = model.cuda()  # transfers the model to gpu memory

    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()

    data = t.Tensor(np.load("data_processed.npy")).cuda()
    answers = t.Tensor(np.load("data_truth.npy")).cuda()
    validation = t.Tensor(np.load("data_processed1.npy")[:2]).cuda()
    valians = t.Tensor(np.load("data_truth1.npy")[:2]).cuda()

    dataset = feeder.TensorDataset(data, answers)
    loader = feeder.DataLoader(dataset, batch_size=20)

    for epoch in range(2):  # loop over the dataset multiple times

        running_loss = 0.0
        for i, data in enumerate(loader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, solutions = data
            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = model(inputs)
            # print(outputs.shape)
            loss = criterion(outputs, solutions.cuda())
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            # if i % 2000 == 1999:    # print every 2000 mini-batches
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 2000))
            running_loss = 0.0
    print('Finished Training')

    valout = model(validation)
    plt.imshow(valians[0, 0].cpu())
    plt.show()
    plt.imshow(valout[0, 0].cpu().detach().numpy())
    plt.show()
