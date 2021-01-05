# -*- coding: utf-8 -*-

import os
import sys

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QDialog, QFileDialog, QTableWidgetItem

from calculator import Calculate
from read_config import InitParas, WriteConfig

CONFIG = 'config.ini'

class test1(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("ui_source/test1.ui", self)
        self.pushButton_caculate.clicked.connect(self.handleCalc)
        self.pushButton_readdata.clicked.connect(self.file_dialog)
        self.pushButton_savedata.clicked.connect(self.export_config)

        self.init_config_thread = InitParas(CONFIG)
        self.init_config_thread.signal.connect(self.init_paras_callback)
        self.init_config_thread.start()  # 启动线程

        self.parameters = {}

    # 读取保存参数的回调函数
    def init_paras_callback(self, value):
        if value:
            parameters = value[0]
            self.paras_keys = [x for x in parameters]
            for key in parameters:
                eval('self.' + key).setPlainText(parameters[key])
        else:
            pass

    # 导入文件窗口
    def file_dialog(self):
        # 设置文件扩展名过滤,注意用双分号间隔
        self.clg_file, filetype = QFileDialog.getOpenFileName(self, "选取文件", get_desk_path(),
                                                              "Text Files (*.clg);;All Files (*)")
        if self.clg_file:
            self.output_file = self.output_file + os.path.basename(self.clg_file)

    # 导入文件窗口
    def export_config(self):
        self.output_filepath = QFileDialog.getSaveFileName(self, "选择导出的文件夹位置", get_desk_path())
        if self.output_filepath:
            pass

    # 开始进行计算
    def handleCalc(self):
        result = self.acquire_paras_value()
        if result:
            self.calculate_thread = Calculate(self.parameters)  # 计算进程
            self.calculate_thread.signal.connect(self.result_panel)
            self.calculate_thread.start()  # 启动线程
            # 多线程保存数据

            self.save_paras_thread = WriteConfig(CONFIG, self.parameters)
            self.save_paras_thread.signal.connect(self.save_config_callback)
            self.save_paras_thread.start()  # 启动线程
        pass

    def result_panel(self, cal_result):
        """
        计算完毕进入的回调函数
        :param cal_result: 计算结果
        :return: None
        """
        # print(cal_result)
        self.child = Child(cal_result)  # 创建子窗口实例
        self.child.exec()

    def save_config_callback(self, value):
        if value:
            print(value)

    # 从面板中获取所有用户的值
    def acquire_paras_value(self):
        for value in self.paras_keys:
            user_define_paras = eval('self.' + value).toPlainText()
            if user_define_paras:
                self.parameters[value] = user_define_paras
            else:
                return False
        return True

class Child(QDialog):
    """
    查看客户端详情页。
    """

    def __init__(self, args, parent=None):
        super().__init__(parent)
        self.args = args
        self.initUI()

    def initUI(self):
        loadUi("ui_source/test1-1.ui", self)
        self.setWindowTitle("计算结果窗口")  # 设置窗口标题
        self.pushButton_12.clicked.connect(self.quit)  # 点击ok，隐士存在该方法
        self.pushButton_11.clicked.connect(self.save_result)  # 保存文件到指定文件路径

        # 将结果写入到表格中
        surf_ave_e_feild = self.args[0]  # 表面平均电场
        self_pot_coeff = self.args[1]  # 自电势系数
        q = self.args[2]  # 电荷矩阵
        self.tableWidget.setRowCount(7)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)

        # 添加数据
        newItem = QTableWidgetItem('表面平均电场')
        self.tableWidget.setItem(0, 0, newItem)
        surf_ave_e_feild =format(surf_ave_e_feild, '.3e')
        newItem1 = QTableWidgetItem(str(surf_ave_e_feild))
        self.tableWidget.setItem(0, 1, newItem1)
        newItem = QTableWidgetItem('自电势系数')
        self.tableWidget.setItem(1, 0, newItem)
        for i in range(3):
            for j in range(3):
                result_value = format(self_pot_coeff[i][j], '.3e')
                newItem = QTableWidgetItem(str(result_value))
                self.tableWidget.setItem(i + 1, j + 1, newItem)

        newItem = QTableWidgetItem('电荷矩阵')
        self.tableWidget.setItem(4, 0, newItem)
        for i in range(3):
            for j in range(1):
                result_value = format(q[i][j], '.3e')
                newItem = QTableWidgetItem(str(result_value))
                self.tableWidget.setItem(i + 4, j + 1, newItem)

    def save_result(self):
        self.output_filepath = QFileDialog.getSaveFileName(self, "选择导出的文件夹位置", get_desk_path())
        if self.output_filepath:
            pass

    def quit(self):  # 点击ok是发送内置信号
        self.close()


def get_desk_path():
    return os.path.join(os.path.expanduser('~'), "Desktop")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = test1()
    window.show()
    sys.exit(app.exec_())
