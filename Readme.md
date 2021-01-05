#### 送电线路电磁环境计算程序
---

#### 软件功能
- 手动输入导线参数后，软件能够将输入的参数保存到指定路径中
- 软件能够载入上次导出的参数文件，用户可以对参数文件进行手动修改
- 根据用户输入的参数自动化计算所需结果，计算的内容包括`表面平均电场` `自电势系数` `电荷矩阵`
- 选择结果保存的路径后，计算结果可以保存位特定文件。

#### 软件界面展示
![参数输入界面 ](https://github.com/Jarrettluo/wire_EMC_calculator/blob/master/screeshot/window1.png)
![计算结果 ](https://github.com/Jarrettluo/wire_EMC_calculator/blob/master/screeshot/window2.png)

#### 软件使用方法 
1 新建虚拟环境，安装依赖库
```pip install -r requirements.txt```

2 运行程序
`python window.py`
:joy: