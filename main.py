from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
import pyqtgraph as pg
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
import numpy as np
import serial
import serial.tools.list_ports
import sys
from untitled import Ui_MainWindow
# from haveclolor import Ui_MainWindow
import time
import re
import pylab as pl
from matplotlib.pylab import mpl
import math
import numpy as np
import random
import encodedatas
from threading import Thread


class embedbutton(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(embedbutton,self).__init__()
        self.setupUi(self)
        self.init()
        self.ser = serial.Serial()                      #串口初始化
        # self.xasx = np.linspace(0,2,101)
        self.datas = []                                 #创建x轴数据属性
        self.ydatas = []                                #创建Y轴数据属性
        self.zdatas = []                                #创建Z轴数据列表属性
        self.adatas = []                                #创建总量数据列表属性
        self.measuredatas = []                          #X方向测量数据存储列表初始化
        self.ymeasuredatas = []                              #Y方向测量数据存储列表初始化
        self.zmeasuredatas = []                              #Z方向测量数据存储列表初始化
        self.ameasuredatas = []                              #总量测量数据存储列表初始化
        self.px_time = self.graphicsView.addPlot()           #创建x轴时间域图像
        self.px_freq = self.graphicsView_2.addPlot()         #创建x轴频率域图像

        self.py_time = self.graphicsView_3.addPlot()         #创建y轴时间域图像
        self.py_freq = self.graphicsView_4.addPlot()         #创建y轴频率域图像

        self.pz_time = self.graphicsView_5.addPlot()         #创建z轴时间域图像
        self.pz_freq = self.graphicsView_6.addPlot()         #创建z轴频率域图像

        self.pa_time = self.graphicsView_7.addPlot()         #创建总场时间域图像
        self.pa_freq = self.graphicsView_8.addPlot()         #创建总场频率域图像

        self.curvex_time = self.px_time.plot(self.datas, pen="r")   #导入X方向数据
        self.curvex_freq = self.px_freq.plot(pen="r")

        self.curvey_time = self.py_time.plot(self.ydatas,pen="g")   #导入Y方向数据
        self.curvey_freq = self.py_freq.plot(pen="g")

        self.curvez_time = self.pz_time.plot(self.zdatas,pen="b")   #导入Z方向数据
        self.curvez_freq = self.pz_freq.plot(pen="b")

        self.curvea_time = self.pa_time.plot(self.zdatas, pen="y")  #导入总量数据
        self.curvea_freq = self.pa_freq.plot(pen="y")


        # 设置图像栅格
        self.px_time.showGrid(x=True, y=True)                    #打开图像栅格
        self.px_time.setLabel(axis="left", text="x轴磁场值/nT")
        self.px_time.setLabel(axis="bottom", text="步长/s")

        self.py_time.showGrid(x=True, y=True)                   # 打开图像栅格
        self.py_time.setLabel(axis="left", text="y轴磁场值/nT")
        self.py_time.setLabel(axis="bottom", text="步长/s")

        self.pz_time.showGrid(x=True, y=True)                   # 打开图像栅格
        self.pz_time.setLabel(axis="left", text="z轴磁场值/nT")
        self.pz_time.setLabel(axis="bottom", text="步长/s")

        self.pa_time.showGrid(x=True, y=True)                   # 打开图像栅格
        self.pa_time.setLabel(axis="left", text="磁场总强度/nT")
        self.pa_time.setLabel(axis="bottom", text="步长/s")

        self.px_freq.showGrid(x=True, y=True)                   # 打开图像栅格
        self.px_freq.setLabel(axis="left", text="x轴磁场值/nT")
        self.px_freq.setLabel(axis="bottom", text="步长/s")

        self.py_freq.showGrid(x=True, y=True)                   # 打开图像栅格
        self.py_freq.setLabel(axis="left", text="y轴磁场值/nT")
        self.py_freq.setLabel(axis="bottom", text="步长/s")

        self.pz_freq.showGrid(x=True, y=True)                   # 打开图像栅格
        self.pz_freq.setLabel(axis="left", text="z轴磁场值/nT")
        self.pz_freq.setLabel(axis="bottom", text="步长/s")

        self.pa_freq.showGrid(x=True, y=True)                   # 打开图像栅格
        self.pa_freq.setLabel(axis="left", text="磁场总强度/nT")
        self.pa_freq.setLabel(axis="bottom", text="步长/s")

        self.vbp1_time = self.px_time.vb  # X方向鼠标定位图像初始化
        self.vbp2_time = self.py_time.vb  # Y方向鼠标定位图像初始化
        self.vbp3_time = self.pz_time.vb  # Z方向鼠标定位图像初始化
        self.vbp4_time = self.pa_time.vb  # 总量鼠标定位图像初始化
        self.counter = 0
        self.passfirstdata = 0
        self.slice_len = 0
        self.timescap = 0
        self.x = []
        self.sampling = 0

        def mouseMoved(evt):
            self.pos = evt[0]
            if self.px_time.sceneBoundingRect().contains(self.pos):
                self.mousePoint = self.vbp1_time.mapSceneToView(self.pos)
                self.index = float(self.mousePoint.x())
                if self.index > 0 and self.index < len(self.measuredatas):
                    self.lineEdit_2.setText(
                        str('%.2f' % self.mousePoint.x()) + "," + str(
                            '%.2f' % self.datas[int(self.index / self.timescap)]))

        self.proxy = pg.SignalProxy(self.px_time.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)

        def ymouseMoved(evt):
            self.pos2 = evt[0]
            if self.py_time.sceneBoundingRect().contains(self.pos2):
                self.ymousePoint = self.vbp2_time.mapSceneToView(self.pos2)
                self.yindex = float(self.ymousePoint.x())
                if self.yindex > 0 and self.yindex < len(self.ymeasuredatas):
                    self.lineEdit_6.setText(
                        str('%.2f' % self.ymousePoint.x()) + "," + str(
                            '%.2f' % self.ydatas[int(self.yindex / self.timescap)]))

        self.yproxy = pg.SignalProxy(self.py_time.scene().sigMouseMoved, rateLimit=60, slot=ymouseMoved)

        def zmouseMoved(evt):
            self.pos3 = evt[0]
            if self.pz_time.sceneBoundingRect().contains(self.pos3):
                self.zmousePoint = self.vbp3_time.mapSceneToView(self.pos3)
                self.zindex = float(self.zmousePoint.x())
                if self.zindex > 0 and self.zindex < len(self.zmeasuredatas):
                    self.lineEdit_10.setText(
                        str('%.2f' % self.zmousePoint.x()) + "," + str(
                            '%.2f' % self.zdatas[int(self.zindex / self.timescap)]))

        self.zproxy = pg.SignalProxy(self.pz_time.scene().sigMouseMoved, rateLimit=60, slot=zmouseMoved)

        def amouseMoved(evt):
            self.pos4 = evt[0]
            if self.pa_time.sceneBoundingRect().contains(self.pos4):
                self.amousePoint = self.vbp4_time.mapSceneToView(self.pos4)
                self.aindex = float(self.amousePoint.x())
                if self.aindex > 0 and self.aindex < len(self.ameasuredatas):
                    self.lineEdit_14.setText(
                        str('%.2f' % self.amousePoint.x()) + "," + str(
                            '%.2f' % self.adatas[int(self.aindex / self.timescap)]))

        self.aproxy = pg.SignalProxy(self.pa_time.scene().sigMouseMoved, rateLimit=60, slot=amouseMoved)


    def init(self):
        self.pushButton.clicked.connect(lambda :self.port_open())
        self.pushButton_2.clicked.connect(lambda :self.port_close())
        self.pushButton_3.clicked.connect(lambda :self.cleardata())
        self.pushButton_4.clicked.connect(lambda :self.save_datas())
        self.pushButton_5.clicked.connect(lambda :self.save_measuredatas())
        threadTimeDefine = Thread(target=self.Timerdefine())
        threadTimeDefine.start()
    def Timerdefine(self):
        self.timerx_time = QTimer(self)                         #初始化x时域图像更新时钟
        self.timerx_freq = QTimer(self)                         #初始化x频域图像更新时钟
        self.timerx_time.timeout.connect(lambda :self.data_receive())
        self.timerx_freq.timeout.connect(lambda :self.FFT())


    def port_open(self):
        try:
            port_list = list(serial.tools.list_ports.comports())
            port = str(port_list[0]).split(" ")[0]
            self.ser.port = port
            self.ser.baudrate = 115200
            self.ser.open()
        except:
            QMessageBox.critical(self, "Port Error", "无串口连接！")
            return None
        threadSer = Thread(target=self.OpenTimer)
        threadSer.start()

        # self.timer.start(20)
        if self.ser.isOpen():
            self.pushButton.setEnabled(False)  # 设置按键锁定
            self.pushButton_2.setEnabled(True)
        self.timerx_time.start(int(self.timescap * 1000))  # 开启定时器
        self.timerx_freq.start(1000)

    def OpenTimer(self):
        # 获取数据接收频率
        freqstring = self.comboBox.currentText()
        fre = freqstring.split("H")[0]
        if int(fre) == 1:
            self.spinBox.setValue(2)
        print("信号接收频率:" + fre)
        self.timescap = 1 / int(fre)
        print("每隔" + str(self.timescap) + "秒接收一次数据")

    #停止采样
    def port_close(self):
        try:
            self.ser.close()
        except:
            pass
        self.pushButton.setEnabled(True)               #按键锁定
        self.pushButton_2.setEnabled(False)

    # 接收数据
    def data_receive(self):
        global datas, measuredatas
        global ydatas, ymeasuredatas
        global zdatas, zmeasuredatas
        global adatas, ameasuredatas
        global x, timescap, slice_len
        try:
            num = self.ser.inWaiting()
        except:
            self.port_close()
            return None
        self.slice_len = (self.spinBox.value()) / self.timescap
        print("步长内接收数据长度为：" + str(self.slice_len))
        xaix = np.linspace(0, int((self.slice_len) * (self.timescap)), int(self.slice_len + 1))
        x = xaix[0:int(self.slice_len)]
        while True:
            if str(type(self.datas)) == "<class 'numpy.ndarray'>":
                break
            if len(self.datas) > int(self.slice_len) - 1:
                break  # 确保横坐标长度不变
            # da = self.ser.readline()
            # d = encodedatas.jiexi(da)
            # print(d)
            d = [0,0,0]
            if self.counter > 0:  # 省略第一个数据
                self.datas.append(float(d[0]))
                self.ydatas.append(float(d[1]))
                self.zdatas.append(float(d[2]))
                a = float(d[0])
                b = float(d[1])
                c = float(d[2])
                ad = math.sqrt(pow(a, 2) + pow(b, 2) + pow(c, 2))
                self.adatas.append(float(ad))
                self.measuredatas.append(a)
                self.ymeasuredatas.append(b)
                self.zmeasuredatas.append(c)
                self.ameasuredatas.append(ad)
            self.counter += 1
        da = self.ser.readline()
        updata = encodedatas.jiexi(da)
        if len(updata) != 3:
            updata = [0,0,0]
        print(updata)
        xupdata = float(updata[0])
        yupdata = float(updata[1])
        zupdata = float(updata[2])
        aupdata = float(math.sqrt(pow(xupdata, 2) + pow(yupdata, 2) + pow(zupdata, 2)))
        # 设置x方向图像
        self.measuredatas.append(xupdata)
        self.lineEdit.setText(str(xupdata))
        self.datas[:-1] = self.datas[1:]
        self.datas[-1] = float(updata[0])
        # 设置y方向图像
        self.ymeasuredatas.append(yupdata)
        self.lineEdit_5.setText(str(yupdata))
        self.ydatas[:-1] = self.ydatas[1:]
        self.ydatas[-1] = yupdata
        # 设置Z方向图像
        self.zmeasuredatas.append(zupdata)
        self.lineEdit_9.setText(str(zupdata))
        self.zdatas[:-1] = self.zdatas[1:]
        self.zdatas[-1] = zupdata
        # 设置总量图像
        self.ameasuredatas.append(aupdata)
        self.lineEdit_13.setText(str('%.2f' % aupdata))
        self.adatas[:-1] = self.adatas[1:]
        self.adatas[-1] = aupdata

        threadDraw = Thread(target=self.DramGraph(x))
        threadDraw.start()

    def DramGraph(self,x):
        print("x长度："+str(len(x)))
        print("数据长度："+str(len(self.datas)))
        print(self.datas)

        # self.curvex_time.setData(x, self.datas)
        # self.curvey_time.setData(x, self.ydatas)
        # self.curvez_time.setData(x, self.zdatas)
        # self.curvea_time.setData(x, self.adatas)

        self.curvex_time.setData(self.datas)
        self.curvey_time.setData(self.ydatas)
        self.curvez_time.setData(self.zdatas)
        self.curvea_time.setData(self.adatas)


    def FFT(self):
        global datas, ydatas, zdatas, adatas, sampling_rate
        #绘制X轴频谱图
        sampling_rate = 200
        fftdata = self.datas
        sig_size = len(self.datas)
        yfft = np.fft.rfft(fftdata)/(sig_size)
        freqs = np.linspace(0, int(sampling_rate/2), int(sig_size/2 + 1))
        abs_yfft = abs(yfft)
        self.curvex_freq.setData(freqs[:int(sig_size/2)]*sampling_rate/sig_size, abs_yfft[:int(sig_size/2)])
        xidx = np.argmax(abs_yfft)
        xpro = np.amax(abs_yfft)
        xmaxvaluefreq = freqs[int(xidx)]
        print("频率点："+str(xmaxvaluefreq))
        print("频谱幅值："+str(xpro))
        self.lineEdit_3.setText(str('%.2f' %xpro))                  #设置X轴主频峰值
        self.lineEdit_4.setText(str('%.2f' %xmaxvaluefreq))         #设置X轴主峰频点

        #绘制Y轴频谱图
        fftydata = self.ydatas
        yyfft = np.fft.rfft(fftydata)/(sig_size)
        yfreqs = np.linspace(0, int(sampling_rate/2), int(sig_size/2 + 1))
        abs_yyfft = abs(yyfft)
        self.curvey_freq.setData(yfreqs[:int(sig_size/2)]*sampling_rate/sig_size, abs_yyfft[:int(sig_size/2)])
        #找到Y轴最大值及其频点
        yidx = np.argmax(abs_yyfft)
        ypro = np.amax(abs_yyfft)
        ymaxvaluefreq = freqs[int(yidx)]
        print("频率点：" + str(ymaxvaluefreq))
        print("频谱幅值：" + str(ypro))
        self.lineEdit_7.setText(str('%.2f' % ypro))             # 设置Y轴主频峰值
        self.lineEdit_8.setText(str('%.2f' % ymaxvaluefreq))    # 设置Y轴主峰频点

        #绘制Z轴频谱图
        fftzdata = self.zdatas
        zyfft = np.fft.rfft(fftzdata)/(sig_size)
        zfreqs = np.linspace(0, int(sampling_rate / 2), int(sig_size / 2 + 1))
        abs_zyfft = abs(zyfft)
        # abs_zyfft_n = abs_zyfft / len(self.zdatas)
        # zyfft_log = np.log10(np.clip(abs_zyfft_n, 1e-20, 1e1000))
        self.curvez_freq.setData(zfreqs[:int(sig_size/2)]*sampling_rate/sig_size, abs_zyfft[:int(sig_size/2)])
        # 找到Z轴最大值及其频点
        zidx = np.argmax(abs_zyfft)
        zpro = np.amax(abs_zyfft)
        zmaxvaluefreq = freqs[int(zidx)]
        print("频率点：" + str(zmaxvaluefreq))
        print("频谱幅值：" + str(zpro))
        self.lineEdit_11.setText(str('%.2f' % zpro))             # 设置Z轴主频峰值
        self.lineEdit_12.setText(str('%.2f' % zmaxvaluefreq))    # 设置Z轴主峰频点

        #绘制总量频谱图
        fftadata = self.adatas
        ayfft = np.fft.rfft(fftadata)/(sig_size)
        afreqs = np.linspace(0, int(sampling_rate / 2), int(sig_size / 2 + 1))
        abs_ayfft = abs(ayfft)
        # abs_ayfft_n = abs_ayfft / len(self.adatas)
        # ayfft_log = np.log10(np.clip(abs_ayfft_n, 1e-20, 1e1000))
        self.curvea_freq.setData(afreqs[:int(sig_size/2)]*sampling_rate/sig_size, abs_ayfft[:int(sig_size/2)])
        # 找到总场最大值及其频点
        aidx = np.argmax(abs_ayfft)
        apro = np.amax(abs_ayfft)
        amaxvaluefreq = freqs[int(aidx)]
        print("频率点：" + str(amaxvaluefreq))
        print("频谱幅值：" + str(apro))
        self.lineEdit_15.setText(str('%.2f' % apro))            # 设置总场主频峰值
        self.lineEdit_16.setText(str('%.2f' % amaxvaluefreq))   # 设置总场主峰频点

    # 清楚数据窗口
    def cleardata(self):
        datalen = len(self.datas)
        ydatalen = len(self.ydatas)
        zdatalen = len(self.zdatas)
        adatalen = len(self.adatas)

        self.datas = [0] * datalen
        self.ydatas = self.datas
        self.zdatas = self.datas
        self.adatas = self.datas
        clearx = np.zeros(len(self.datas))
        self.curvex_time.setData(clearx, self.datas)                #清除x轴时域和频域图像
        self.curvex_freq.setData(clearx, self.datas)

        self.curvey_time.setData(clearx, self.ydatas)               #清除y轴时域和频域图像
        self.curvey_freq.setData(clearx, self.ydatas)

        self.curvez_time.setData(clearx, self.zdatas)               #清除z轴时域和频域图像
        self.curvez_freq.setData(clearx, self.zdatas)

        self.curvea_time.setData(clearx, self.adatas)               #清除z轴时域和频域图像
        self.curvea_freq.setData(clearx, self.adatas)


    # 保存测量接收数据
    def save_measuredatas(self):
        if len(self.datas) == 0:
            QMessageBox.critical(self, "Error", "未采集到数据")
        else:
            # 添加头文件
            headfile = ['"All data are saved as follows"'
                , '"Fluxgate three-component magnetometer of China University of Geosciences (Wuhan)"'
                , '"China University of Geosciences, Hongshan District, Wuhan City, Hubei Province"'
                , '"Made by School of Mechanical Engineering and Electronic Information"']
            # 获取当前时间为保存文件名
            localtime = time.asctime(time.localtime(time.time()))
            timestring = localtime.split(" ")
            print(timestring)
            fenmiao = timestring[3]
            timestring[3] = fenmiao.replace(":", "")
            now = ""
            for i in range(len(timestring) - 1):
                now = now + str(timestring[i]) + "-"
            headfile.append(str(time.asctime(time.localtime(time.time()))) + " " + str(
                now + str(timestring[len(timestring) - 1])))
            filepath = QtWidgets.QFileDialog.getExistingDirectory(None, "请选择文件夹路径")
            now = "alldatas-" + now + str(timestring[len(timestring) - 1]) + ".txt"
            measuredatas_filepath = filepath + "\\" + now
            print(measuredatas_filepath)
            with open(measuredatas_filepath, "a+", encoding="utf-8") as f:
                for head in headfile:
                    f.write(head)
                    f.write("\n")

            with open(measuredatas_filepath, "a+", encoding="utf-8") as f:
                for i in range(len(self.measuredatas)):
                    f.write("The number " + str(i + 1) + " data is " + str(self.measuredatas[i]) + "、" + str(
                        self.ymeasuredatas[i]) + "、" + str(self.zmeasuredatas[i]) + "、" + str(
                        self.ameasuredatas[i]))
                    f.write("\n")
            QMessageBox.information(self, "提醒", "文件已经保存为" + measuredatas_filepath)
            return None

    # 保存窗口函数
    def save_datas(self):
        # 添加头文件
        headfile = ['"The display data is saved as follows"'
            , '"Fluxgate three-component magnetometer of China University of Geosciences (Wuhan)"'
            , '"China University of Geosciences, Hongshan District, Wuhan City, Hubei Province"'
            , '"Made by School of Mechanical Engineering and Electronic Information"']

        if len(self.datas) == 0:
            QMessageBox.critical(self, "Error", "未采集到数据")
        else:
            # 获取当前时间为保存文件名
            localtime = time.asctime(time.localtime(time.time()))
            timestring = localtime.split(" ")
            print(timestring)
            fenmiao = timestring[3]
            timestring[3] = fenmiao.replace(":", "")
            now = ""
            for i in range(len(timestring) - 1):
                now = now + str(timestring[i]) + "-"
            headfile.append('"The current time is ' + str(now + str(timestring[len(timestring) - 1])) + '"')
            filepath = QtWidgets.QFileDialog.getExistingDirectory(None, "请选择文件夹路径")
            now = "nowdatas-" + now + str(timestring[len(timestring) - 1]) + ".txt"
            measuredatas_filepath = filepath + "\\" + now
            print(measuredatas_filepath)
            with open(measuredatas_filepath, "a+", encoding="utf-8") as f:
                for head in headfile:
                    f.write(head)
                    f.write("\n")

            with open(measuredatas_filepath, "a+", encoding="utf-8") as f:
                for i in range(len(self.datas)):
                    f.write("The number " + str(i + 1) + " data is " + str(self.datas[i]) + "、" + str(
                        self.ydatas[i]) + "、" + str(self.zdatas[i]) + "、" + str(self.adatas[i]))
                    f.write("\n")
            QMessageBox.information(self, "提醒", "文件已经保存为" + measuredatas_filepath)
        return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = embedbutton()
    a.setWindowIcon(QIcon("exepic.ico"))
    a.setWindowTitle("中国地质大学(武汉)")
    a.show()
    sys.exit(app.exec_())





