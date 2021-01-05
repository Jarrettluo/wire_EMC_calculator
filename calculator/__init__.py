# encoding: utf-8
"""
@version: 1.0
@author: Jarrett
@file: __init__.py
@time: 2020/12/16 22:16
"""
from PyQt5.QtCore import QThread, pyqtSignal
from calculator.calculate import ParameterCalculator


# 多线程计算
class Calculate(QThread):
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self, args_list):
        super().__init__()
        self.args_data = args_list

    def __del__(self):
        self.wait()

    def run(self):
        """
        将参数传入到计算公式中。需要哪些数据就将起放入emit的列表中
        :return:
        """
        # print(self.args_data) # 传入参数
        parameter_calculator = ParameterCalculator(self.args_data)
        surf_ave_e_feild = parameter_calculator.surface_average_electric_field()
        # print(surf_ave_e_feild) # 表面平均电场
        self_pot_coeff = parameter_calculator.self_potential_coefficient()
        # print(self_pot_coeff) # 自电势系数
        if self_pot_coeff is not None:
            Q = parameter_calculator.capacity_matrix_cal()
            # print(Q) # 电荷矩阵
        self.signal.emit([surf_ave_e_feild, self_pot_coeff, Q])  # 发射信号
