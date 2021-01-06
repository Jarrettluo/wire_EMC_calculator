# encoding: utf-8
"""
@version: 1.0
@author: Jarrett
@file: __init__.py
@time: 2020/12/19 17:35
"""
import configparser

from PyQt5.QtCore import QThread, pyqtSignal


class InitParas(QThread):
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self, args_list):
        super().__init__()
        self.config_file = args_list

    def __del__(self):
        self.wait()

    def run(self):
        # 创建配置文件对象
        con = configparser.ConfigParser()
        # 读取文件
        con.read(self.config_file, encoding='utf-8')
        # 获取特定section
        init_parameters = con.items('parameters')  # 返回结果为元组
        # 可以通过dict方法转换为字典
        init_parameters = dict(init_parameters)
        # 获取参数对应关系
        paras_map = con.items('paras_map')
        paras_map = dict(paras_map)
        self.signal.emit([init_parameters, paras_map])  # 发射信号

class WriteConfig(QThread):
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self, args_list, paras, paras_map):
        super().__init__()
        self.config_file = args_list
        self.paras = paras
        self.paras_map = paras_map

    def __del__(self):
        self.wait()

    def run(self):
        # 创建配置文件对象
        con = configparser.ConfigParser()
        # 读取文件
        con.read(self.config_file, encoding='utf-8')
        # con.add_section("parameters")
        for key in self.paras:
            con.set("parameters", key, self.paras[key])

        # 写入参数对应关系
        for key in self.paras_map:
            con.set("paras_map", key, self.paras_map[key])

        try:
            with open(self.config_file, "w+", encoding='utf-8') as f:
                con.write(f)
        except ImportError:
            self.signal.emit([])  # 发射空信号
        else:
            self.signal.emit([True])  # 发射信号



