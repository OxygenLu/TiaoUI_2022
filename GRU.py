# import torch.nn as nn
# import torch
#
#
# class GRU(nn.Module):
#     def __init__(self, in_dim, hidden_dim, num_layer, num_classes):
#         super(GRU, self).__init__()
#         self.in_dim = in_dim
#         self.hidden_dim = hidden_dim
#         self.num_layer = num_layer  # GRU网络层数
#         self.lstm = nn.GRU(input_size=in_dim, hidden_size=hidden_dim, num_layers=num_layer, batch_first=True,
#                            dropout=0.5)
#         self.relu = nn.PReLU()  # PReLU激活函数，防止死亡ReLU问题
#         self.classes = nn.Sequential(
#             nn.Linear(in_features=hidden_dim, out_features=num_classes),  # num_classes为分类数
#         )
#
#     def forward(self, x):
#         x, h_0 = x  # 将输入拆分
#         batch_size = x.shape[0]  # 获取x的batch_size
#         out, h_t1 = self.lstm(x, h_0)  # 将数据传入GRU网络训练
#         out = h_t1[-1:, :, :]  # 取得最后一层GRU的输出
#         out = out.view(batch_size, -1)  # 将维度从(1, b, hiddem) => (b, hiddem)
#         out = self.classes(out)  # 进入全连接层训练
#         out = self.relu(out)  # 激活输出
#         return out, h_t1  # 返回out输出及h_t给下一层


# ------------------------------------------------------------------
import torch.nn as nn


class GRU(nn.Module):
    def __init__(self, in_dim, hidden_dim, num_layer, num_classes):
        super(GRU, self).__init__()
        self.in_dim = in_dim
        self.hidden_dim = hidden_dim
        self.num_layer = num_layer
        # self.num_classes = num_classes

        self.lstm = nn.GRU(input_size=in_dim, hidden_size=hidden_dim, num_layers=num_layer, batch_first=True)

        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)
        self.classes = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.Dropout(0.5),
            nn.ReLU(),
            nn.Linear(hidden_dim, num_classes)
        )

    def forward(self, x):
        x, h_0 = x
        # print(x.shape, h_0.shape, c_0.shape)
        # print(x, h_0, c_0)
        batch_size = x.shape[0]
        out, h_t = self.lstm(x, h_0)
        # h_t = h_t[:,:,:]
        # print(h_t.shape)
        out = h_t[-1:, :, :]
        # print('out: ',out.shape)
        out = out.view(batch_size, -1)
        # print('out : ',out.shape)
        # print('h_t: ',h_t.shape)
        # print('c_t: ', c_t.shape)
        # h_t = self.relu(h_t)
        out = self.classes(out)
        # out = self.softmax(out)
        # out = self.relu(out)
        # print(out.shape)
        # out = self.relu(out)

        return out, h_t
