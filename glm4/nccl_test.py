import torch
#单卡
x = torch.rand(1024, 1024, device='cuda:0')
print(torch.cuda.nccl.is_available(x))
#多卡
x = torch.rand(1024, 1024, device='cuda:0')
y = torch.rand(1024, 1024, device='cuda:2')
print(torch.cuda.nccl.is_available([x, y]))