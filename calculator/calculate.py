# encoding: utf-8
"""
@version: 1.0
@author: Jarrett
@file: calculate
@time: 2020/12/16 22:17
"""

import numpy as np
import math


def calculate(num_fenlie):
    # # 对变量进行定义
    # delta_air = self.airp.toPlainText()
    # Kcp = self.Kcp.toPlainText()
    # rad = self.rad.toPlainText()
    # A_x = self.A_x.toPlainText()
    # A_y = self.A_y.toPlainText()
    # B_x = self.B_x.toPlainText()
    # B_y = self.B_y.toPlainText()
    # C_x = self.C_x.toPlainText()
    # C_y = self.C_y.toPlainText()
    # num_fenlie = self.num_fenlie.toPlainText()
    # r_20 = self.r_20.toPlainText()
    # fenliejianju = float(self.fenliejianju.toPlainText())

    # 分裂数 n
    n = float(num_fenlie)
    # 被测点与导线高度差
    H = float(A_y) - 2
    # 被干扰点距导线的距离
    D_num = (20 ** 2 + H ** 2) ** 0.5
    # 子导线直径
    d = 2 * float(rad)

    # 频率
    f = 50

    # 标准大气压空气密度
    delta0 = 1

    # peek公式计算表面电场强度
    Ele = 30.3 * float(delta_air) * float(Kcp) * (1 + (0.298 / (float(rad) / 10 * float(delta_air)) ** 0.5))
    print("起晕电场强度=", Ele)
    # 公式无误

    # 表面电场计算

    # 分裂导线所处圆的半径 cm
    R1 = fenliejianju / 10

    # 介电常数
    E0 = 8.854
    # 导线高度
    h2 = 2
    h = np.ones([3, 1])
    h[0] = A_y
    h[1] = B_y
    h[2] = C_y
    # 等效半径计算
    R = R1 / 2 / math.sin(math.pi / n)
    Req1 = n * float(rad) / 10
    Req2 = R ** (n - 1)
    Req3 = Req1 * Req2
    Req = Req3 ** (1 / n)

    print("req=", Req)

    # 需要修改矩阵中的数值

    # 计算Dij，数值要具体计算
    D = np.ones([3, 3])
    for i in range(3):
        for j in range(3):
            if i == j:
                D[i][j] = 1
            else:
                D[i][j] = 0

    # 下面数值还需具体计算

    D[0][1] = D[1][0] = ((float(A_x) - float(B_x)) ** 2 + float(float(A_y) + float(B_y)) ** 2) ** 0.5
    D[0][2] = D[2][0] = ((float(A_x) - float(C_x)) ** 2 + float(float(A_y) + float(C_y)) ** 2) ** 0.5
    D[1][2] = D[2][1] = ((float(B_x) - float(C_x)) ** 2 + float(float(B_y) + float(C_y)) ** 2) ** 0.5

    # 计算dij，需要修改矩阵中的数值
    d = []
    for i in range(3):
        d.append([])
        for j in range(3):
            d[i].append(1)
    d = np.array(d)
    # 下面数值还需具体计算
    d[0][1] = d[1][0] = ((float(A_x) - float(B_x)) ** 2 + float(float(A_y) - float(B_y)) ** 2) ** 0.5
    d[0][2] = d[2][0] = ((float(A_x) - float(C_x)) ** 2 + float(float(A_y) - float(C_y)) ** 2) ** 0.5
    d[1][2] = d[2][1] = ((float(B_x) - float(C_x)) ** 2 + float(float(B_y) - float(C_y)) ** 2) ** 0.5

    P = []
    for i in range(3):
        P.append([])
        for j in range(3):
            if i == j:
                P[i].append((1 / 2 / 3.14 / E0) * math.log(2 * h2 / Req))
            else:
                P[i].append((1 / 2 / 3.14 / E0) * math.log(D[i][j] / d[i][j]))
    P = np.array(P)
    print(D)
    print(d)
    print(P)
    # 对电位系数矩阵P求逆
    P_1 = np.linalg.inv(P)
    print(P_1)
    # 电压矩阵
    U = ([500], [500], [500])
    U = np.array(U)
    print(U)
    # 电荷矩阵
    Q = np.matmul(P_1, U)
    print(Q)
    # 子导线表面平均电场强度
    Eav = Q / (2 * math.pi * E0 * n * float(rad))
    print("bmdc=", Eav)
    # 子导线表面平均最大电场强度
    Emax = Eav * (1 + ((n - 1) * float(rad) / R))
    print(Emax)
    print(Ele)
    Emax = 3
    print(Emax)
    # 单回路无线电干扰场强计算
    # 电压小于750kV
    RI = 3.5 * Emax + 12 * float(rad) - 30 + 33 * math.log((22 / D_num), 10)
    # 电压大于等于750kV
    # RI = 48 + 3.5 * (Emax - 17.5) + 30 * math.log((d / 3.51), 10) + 20 * math.log((30.7 * H / D_num / D_num), 10) + 10 * (1 - f) + 40 * (1 - float(delta_air) / delta0)
    print(RI)
    # 单回路可听噪声计算


DK = 8.85  # 介电常数Dielectric constant


class ParameterCalculator:
    def __init__(self, parameters):
        """
        对参数进行初始化
        :param parameters:输入进来的参数，格式为json
        """
        self.split_space = float(parameters.get('fenliejianju'))  # 分裂间距
        self.split_num = float(parameters.get('num_fenlie'))  # 分裂数，单位n
        self.wire_radius = float(parameters.get('rad'))  # 半径，
        self.a_x = float(parameters.get('a_x'))
        self.a_y = float(parameters.get('a_y'))
        self.b_x = float(parameters.get('b_x'))
        self.b_y = float(parameters.get('b_y'))
        self.c_x = float(parameters.get('c_x'))
        self.c_y = float(parameters.get('c_y'))

        self.wire_height = [self.a_y, self.b_y, self.c_y]  # 导线高度，单位m，组成列表方便取用
        self.potential_matrix = None  # 准备计算的返回值，电势矩阵

    def circle_radius_calculate(self):
        """
        中间步骤，计算圆周半径，单位cm
        :return: 返回圆周半径
        """
        # 计算圆周半径，单位cm
        self.circle_radius = self.split_space / (2 * math.sin(math.pi / self.split_num))

    def surface_average_electric_field(self):
        """
        计算表面平均电场。如果在前置步骤中计算失败，则返回空。
        :return: 返回表面平均电场 self.surf_ave_e_field
        """
        # 计算表面平均电场
        if self.split_space and self.split_num:
            self.circle_radius_calculate()
            extract_circle_radius = pow(self.circle_radius, self.split_num - 1)
            self.surf_ave_e_field = pow(self.split_num * self.wire_radius * extract_circle_radius, 1 / self.split_num)
            return self.surf_ave_e_field
        else:
            return False

    def self_potential_coefficient(self):
        """
        计算电位系数P
        :return: 返回电位系数P
        """
        # 计算自电位系数
        if self.surf_ave_e_field:
            D = np.identity(3)  # 创建一个对角三维矩阵D
            D[0][1] = D[1][0] = math.sqrt(pow(self.a_x - self.b_x, 2) + pow(self.a_y + self.b_y, 2))
            D[0][2] = D[2][0] = math.sqrt(pow(self.a_x - self.c_x, 2) + pow(self.a_y + self.c_y, 2))
            D[1][2] = D[2][1] = math.sqrt(pow(self.b_x - self.c_x, 2) + pow(self.b_y + self.c_y, 2))
            # print(D)
            d = np.identity(3)  # 创建一个对角三维矩阵d
            d[0][1] = d[1][0] = math.sqrt(pow(self.a_x - self.b_x, 2) + pow(self.a_y - self.b_y, 2))
            d[0][2] = d[2][0] = math.sqrt(pow(self.a_x - self.c_x, 2) + pow(self.a_y - self.c_y, 2))
            d[1][2] = d[2][1] = math.sqrt(pow(self.b_x - self.c_x, 2) + pow(self.b_y - self.c_y, 2))
            # print(d)
            if np.any(d == 0):
                return False  # d 矩阵不能具有0元素，否则会报错
            P = np.identity(3)  # 创建一个对角三维矩阵P
            for i in range(3):
                for j in range(3):
                    if i == j:
                        P[i][j] = (1 / (2 * math.pi * DK)) * math.log(
                            2 * self.wire_height[i] * 100 / self.surf_ave_e_field) * 1e12  # 转换单位
                    else:
                        P[i][j] = (1 / (2 * math.pi * DK)) * math.log(D[i][j] / d[i][j]) * 1e12
            self.potential_matrix = P
            return self.potential_matrix
        else:
            return False

    def capacity_matrix_cal(self):
        """
        电容矩阵计算公式
        :return: 返回电容矩阵
        """
        if self.potential_matrix is not None:
            # 对电位系数矩阵P求逆
            P_1 = np.linalg.inv(self.potential_matrix)
            # print(P_1)
            U = np.array(([500], [500], [500]))  # 电压矩阵
            Q = np.matmul(P_1, U)  # 电荷矩阵
            # print(Q)
            return Q


def test_parameterCalculator():
    """
    这个方程用来测试参数计算器。
    :return:
    """
    parameters = {
        'fenliejianju': '45',
        'num_fenlie': '4',
        'rad': '1.5',

        'a_x': '-19',
        'a_y': '29',
        'b_x': '0',
        'b_y': '31',
        'c_x': '19',
        'c_y': '29',
    }
    parameter_calculator = ParameterCalculator(parameters)
    surf_ave_e_feild = parameter_calculator.surface_average_electric_field()
    print(surf_ave_e_feild)
    self_pot_coeff = parameter_calculator.self_potential_coefficient()
    print(self_pot_coeff)
    if self_pot_coeff is not None:
        Q = parameter_calculator.capacity_matrix_cal()
        print(Q)


def test_matrix():
    """
    测试矩阵的创建等
    :return:
    """


if __name__ == "__main__":
    test_parameterCalculator()
    # test_matrix()
