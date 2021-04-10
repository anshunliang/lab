import sys,time,socket
import random,queue,openpyxl,cgitb,threading
from functools import partial
from PyQt5.QtCore import *
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline
from PyQt5.QtWidgets import *
from PyQt5 import *
import pyqtgraph as pg

from kpas import kpa     #导入压力转换模块
import globalvar as gl   #导入自建的全局变量

from x import Ui_MainWindow   #导入主窗口
import booll,floatt    #导入开关阀和调节阀子窗口 
import tx,qx
 
gl._init()            #全局变量初始化
cgitb.enable()        #异常捕捉



lock = QMutex()   #实例化锁,针对数据读取和数据刷新两个线程
lock1 = QMutex()   #实例化锁,针对自建的全局变量

q=queue.Queue()   #实例化队列，针对控制消息获取


#建立全局变量
xp=[]  #用于存储AI控件
xpindex=[]
xpd=[]  #用于存储DI控件
xpdindex=[]
xptype=[]
xh=[]  #用于存储采集的现场信号
jp=[]    #存储控件对应的数值索引


class Main(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        
    def prt(self):
        print("jjjj")


#建立TCP通信
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ("127.0.0.1",8000)
tcp_socket.connect(server_addr)
        



#读取配置表
data = openpyxl.load_workbook('F:\jiemian\AI.xlsx')
wsai = data.get_sheet_by_name('AI')
wsao = data.get_sheet_by_name('AO')
wsdi = data.get_sheet_by_name('DI')
wsdo = data.get_sheet_by_name('DO')

wsai_nrows = wsai.max_row  #获得AI行数
wsao_nrows = wsao.max_row  #获得AO行数
wsdi_nrows = wsdi.max_row  #获得DI行数
wsdo_nrows = wsdo.max_row  #获得DI行数
PZAI=[]                    #存储AI工位号
PZAO=[]                    #存储AO工位号
PZDI=[]
PZDO=[]
#读AI表格
for i in range(1,wsai_nrows):
    j= wsai.cell(row=i+1, column=1).value    #获取1+1行，第一列的值
    PZAI.append(j)
print(PZAI)
#读AO表格
for i in range(1,wsao_nrows):
    j= wsao.cell(row=i+1, column=1).value    #获取1+1行，第一列的值
    PZAO.append(j)
print(PZAO)

#读DI表格
for i in range(1,wsdi_nrows):
    j= wsdi.cell(row=i+1, column=1).value    #获取1+1行，第一列的值
    PZDI.append(j)
print(PZDI)

#读Do表格
for i in range(1,wsdo_nrows):
    j= wsdo.cell(row=i+1, column=1).value    #获取1+1行，第一列的值
    PZDO.append(j)
print(PZDO)

#计算模拟量的个数
xo=len(PZAI)+len(PZAO)
'''
#定义子窗口
class Child(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("使用教程")
        self.resize(250, 180)

        self.dk= QLabel(self)
        self.dk.setGeometry(30, 30, 100, 100)
        str='端口'
        self.dk.setText(str)
        
        
    def open(self):
        self.show()
'''


#首次运行时，根据配置表搜索前面板控件的函数，
def click_success():
    print("start qt5")
    
    global xp
    global PZAI
    global PZDI
    #for i in ["e1","e2","e3","e4",]:
    
    j1=0
    for i in PZAI:
        try:
            if MainWindow.findChild(QLineEdit,i):   #根据反馈AI工位号获取前面板控件
               xp.append(MainWindow.findChild(QLineEdit,i))
               xpindex.append(j1)
             
               j1+=1
            else:
                j1+=1
        except:
            pass
    j1=0
    j=0
  
    for i in PZDI:                                 #根据反馈DI工位号获取前面板控件
        try:
            if MainWindow.findChild(QPushButton,i):
                xpd.append(MainWindow.findChild(QPushButton,i))
                xpdindex.append(j)
                j+=1
            else:
                j+=1
        except:
            pass

        
    



#读取信号线程
class Mythread0(QThread):
    # 定义信号,定义参数为str类型
    breakSignal = pyqtSignal(object)
 
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        time.sleep(1)
        
        global xp
        global PZAI
        while True:
            time.sleep(0.2)
           
            #发送信号到刷新函数,触发界面刷新函数
            #self.breakSignal.emit(str(a))
            #模拟产生现场信号,用于刷新主界面
            lock.lock()
            global xh
            global tcp_socket
            '''
            xh.clear()
            for i in range(50):
                xh.append(random.randint(0,2))
            '''
            xxx=tcp_socket.recv(206)
            xh=xxx.decode('UTF-8').split(" ")
            
            xh=xh[1:]
            #lock1.lock()

            #将读取的信号写入自建全局变量
            try:
                j=0
                for i in PZAI+PZAO+PZDI+PZDO:
                    gl.set_value(i, str(xh[j]))     #设定值
                    j+=1

            except:
                pass
            
            #lock1.unlock()
            
            #发送信号到刷新函数,触发界面刷新函数
            self.breakSignal.emit(xh)

            lock.unlock()
            
            


#
class Mythread1(QThread):

    # 定义信号,定义参数为int类型
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def run(self):
        time.sleep(2)

        while True:
            time.sleep(0.1)


#获取操作员命令，发送控制信号的线程,将控制信号发送到下位机
class Mythread2(QThread):
    # 定义信号,定义参数为int类型
    breakSigna2 = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self): 
        while True:
            time.sleep(0.1)
            #此处获取操作员命令
            #xxx=gl.get_value('score') 
            if not q.empty():
                xxx=q.get()
                ui.ee.setText(str(xxx))
                send_data = xxx
                tcp_socket.send(send_data.encode("utf-8"))

#界面刷新函数，a是线程发送过来的信号，用于刷新界面
def chuli(a):
    global xh
    global xpdindex
    global xpindex
    global xp
    global xpd
    global xo
    
    for i,j in zip(xp,xpindex):
        i.setText(str(xh[j]))
              
    
    for k,p in zip(xpd,xpdindex):
        #print(str(xh[14+p]))
        if str(xh[xo+p])=="1":
            k.setStyleSheet("background: rgb(0,255,0)")
        else:
            k.setStyleSheet("background: rgb(255,255,255)")
  
    #xh.clear()

    '''
    xxx=gl.get_value('score') 
    ui.e7.setText(str(xxx))
    lock.acquire()
    xh.append(random.randint(0,9))
    lock.release()
    '''
   
    #xxx=gl.get_value('score')   #获取值
    #gl.set_value('e2', "23")     #设定值
    '''
    ui.e1.setText(a)
    ui.e2.setText(a)
    ui.e3.setText(a)
    '''


#打开 调节阀窗口函数
def convert( x,p):
    print(x)
    p.open()
    '''
    Ph.open()
    '''
    
#打开 开关阀窗口函数
def convertt( x,p):
    print(x)
    p.open()
   
    


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Main()
    ui.setupUi(MainWindow)
    
    #第一种打开子窗口的方式
    #实例化自定义窗口
    #实例化自定义子窗口
    child = QMainWindow()          
    child_ui = tx.Ui_MainWindow()
    child_ui.setupUi(child)
    #打开自定义子窗口
    ui.tx.clicked.connect( child.show ) 



    #打开曲线窗口
    cqx = QMainWindow()          
    cqx_ui = qx.Ui_MainWindow()
    cqx_ui.setupUi(cqx)
    ui.opqx.clicked.connect( cqx.show )   #打开
    
    
   
    #第二种打开子窗口的方式
    #实例化阀门窗口
    eh=floatt.Demo("e2",q,lock1)         #"e2代表阀门号。q代表传入子窗口的队列，用于发送控制消息。lock1用于锁住自建全局变量"
    dh=booll.Demo("e1",q,lock1)
    #打开子窗口
    ui.p1.clicked.connect(dh.open)
    ui.p2.clicked.connect(eh.open)


    #第三种打开子窗口的方式
    #重新实例化子窗口
    #Ph=floatt.Demo("e2",q,lock1)         #"e2代表阀门号。q代表传入子窗口的队列，用于发送控制消息。lock1用于锁住自建全局变量"
    #Ph=floatt.Demo()

    #为p1控件（阀门按钮）绑定事件
    ui.p5.clicked.connect(partial(convert, "p5",floatt.Demo("p5",q,lock1)))
    ui.p6.clicked.connect(partial(convert, "p6",floatt.Demo("p6",q,lock1)))
    ui.p7.clicked.connect(partial(convert, "p7",floatt.Demo("p7",q,lock1)))

    ui.bb5.clicked.connect(partial(convertt, "b5",booll.Demo("b5",q,lock1)))
    ui.bb6.clicked.connect(partial(convertt, "b6",booll.Demo("b6",q,lock1)))
    ui.bb7.clicked.connect(partial(convertt, "b7",booll.Demo("b7",q,lock1)))






    
    #首次运行，根据配置表搜索前面板控件的函数
    click_success()
   
    
    # 创建线程,用于读取信号，自动后台运行
    thread0 = Mythread0()
    thread0.breakSignal.connect(chuli)  
    thread0.start()

    # 创建线程,用于刷新界面信号，自动后台运行
    thread1 = Mythread1()
    thread1.start()

    #创建线程，用于发送控制信号
    thread2 = Mythread2()
    thread2.breakSigna2.connect(chuli)
    thread2.start()


    
    MainWindow.show()
    sys.exit(app.exec_())