__author__ ="Oguzhan Onder"

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from LLT import LLT1
from webscrapping import *
import matplotlib.pylab as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import threading
import time

class Ui_MainWindow(object):
    ### Airfoils values
    def get_value_airfoils(self):
        global value_airfoil
        value_airfoil = self.airfoils_combobox.currentText()
        # print(value_airfoil)
        return value_airfoil
    ### Doublespinbox values
    def get_value_wingspan(self):
        value_wingspan = self.wing_span_QSpinBox.value()      
        # print(value_wingspan)
        return value_wingspan
    def get_value_rootchord(self):
        value_rootchord = self.root_chord_QSpinBox.value()
        # print(value_rootchord)
        return value_rootchord
    def get_value_tipchord(self):
        value_tipchord = self.tip_chord_QSpinBox.value()
        # print(value_tipchord)
        return value_tipchord
    def get_value_wingangle(self):
        value_wingangle = self.wing_angle_QSpinBox.value()
        # print(value_wingangle)
        return value_wingangle
    def get_value_roottwist(self):
        value_roottwist = self.root_twist_angle_QSpinBox.value()
        # print(value_roottwist)
        return value_roottwist
    def get_value_tiptwist(self):
        value_tiptwist = self.tip_twist_angle_QSpinBox.value()
        return value_tiptwist
    def get_value_liftcurveslope(self):
        value_liftcurveslope = self.lift_curve_slope_QSpinBox.value()
        return value_liftcurveslope
    ### Reynolds number combobox value
    def get_value_reynolds_number(self):
        global value_reynoldsnumber
        value_reynoldsnumber = int(self.reynolds_number_combobox.currentText())
        return value_reynoldsnumber

    ###
    
    def main_run(self):
        try:
            stall_risk = check_stall_risk(self.get_value_airfoils(),self.get_value_reynolds_number())
            
            if self.airfoils_combobox.currentIndex() !=0:
                
                if stall_risk[0]<self.get_value_wingangle()+self.get_value_roottwist()<stall_risk[1]:    
                   self.wing_angle_QSpinBox.setStyleSheet("QDoubleSpinBox"
                                                "{"
                                                "background : white;" 
                                                "}") 
                   self.root_twist_angle_QSpinBox.setStyleSheet("QDoubleSpinBox"
                                                "{"
                                                "background : white;"
                                                "}")
                   if stall_risk[0]<self.get_value_wingangle()+self.get_value_tiptwist()<stall_risk[1]:
                       self.wing_angle_QSpinBox.setStyleSheet("QDoubleSpinBox"
                                                "{"
                                                "background : white;" 
                                                "}") 
                       self.tip_twist_angle_QSpinBox.setStyleSheet("QDoubleSpinBox"
                                                "{"
                                                "background : white;"
                                                "}")
                       if self.get_value_wingspan() > 0 and self.get_value_rootchord() > 0 and self.get_value_tipchord() >0:
                            alpha00 = alpha0_calc(self.get_value_airfoils(),self.get_value_reynolds_number())
                            y_s,CL1,CL_wing,AR = LLT1(self.get_value_wingspan(),
                                  self.get_value_rootchord(),
                                  self.get_value_tipchord(),
                                  self.get_value_wingangle(),
                                  self.get_value_roottwist(),
                                  self.get_value_tiptwist(),
                                  self.get_value_liftcurveslope(),
                                  alpha00
                                  )
                       else:
                            msg1 = QMessageBox()
                            msg1.setIcon(QMessageBox.Critical)
                            msg1.setText("Please enter geometric values")
                            msg1.setWindowTitle("Error")
                            msg1.exec_()
                            self.lift_coefficient_value.clear()
                            self.lift_coefficient_value.setStyleSheet("QLineEdit"
                                                    "{"
                                                    "background : white;"
                                                    "}")
                   else:
                        msg2 = QMessageBox()
                        msg2.setIcon(QMessageBox.Critical)
                        if self.get_value_wingangle()+self.get_value_tiptwist() < 0:    
                            msg2.setText("{} degree is in stall region. Please try bigger degrees.".format(self.get_value_wingangle()+self.get_value_tiptwist()))
                            msg2.setWindowTitle("Error")
                            msg2.exec_()
                            self.lift_coefficient_value.clear()
                            self.lift_coefficient_value.setStyleSheet("QLineEdit"
                                                    "{"
                                                    "background : white;"
                                                    "}")
                            self.wing_angle_QSpinBox.setStyleSheet("QDoubleSpinBox"
                                                    "{"
                                                    "background : yellow;"
                                                    "}")
                            self.tip_twist_angle_QSpinBox.setStyleSheet("QDoubleSpinBox"
                                                    "{"
                                                    "background : yellow;"
                                                    "}")
                        elif self.get_value_wingangle()+self.get_value_tiptwist() > 0:
                            msg2.setText("{} degree is in stall region. Please try smaller degrees.".format(self.get_value_wingangle()+self.get_value_tiptwist()))
                            msg2.setWindowTitle("Error")
                            msg2.exec_()
                            self.lift_coefficient_value.clear()
                            self.lift_coefficient_value.setStyleSheet("QLineEdit"
                                                    "{"
                                                    "background : white;"
                                                    "}")
                            self.wing_angle_QSpinBox.setStyleSheet("QDoubleSpinBox"
                                                    "{"
                                                    "background : yellow;"
                                                    "}")
                            self.tip_twist_angle_QSpinBox.setStyleSheet("QDoubleSpinBox"
                                                    "{"
                                                    "background : yellow;"
                                                    "}")
                       
                       
                else:
                    msg2 = QMessageBox()
                    msg2.setIcon(QMessageBox.Critical)
                    if self.get_value_wingangle()+self.get_value_roottwist() < 0:    
                        msg2.setText("{} degree is in stall region. Please try bigger degrees.".format(self.get_value_wingangle()+self.get_value_roottwist()))
                        msg2.setWindowTitle("Error")
                        msg2.exec_()
                        self.lift_coefficient_value.clear()
                        self.lift_coefficient_value.setStyleSheet("QLineEdit"
                                                "{"
                                                "background : white;"
                                                "}")
                        self.wing_angle_QSpinBox.setStyleSheet("QDoubleSpinBox"
                                                "{"
                                                "background : yellow;"
                                                "}")
                        self.root_twist_angle_QSpinBox.setStyleSheet("QDoubleSpinBox"
                                                "{"
                                                "background : yellow;"
                                                "}")
                    elif self.get_value_wingangle()+self.get_value_roottwist() > 0:
                        msg2.setText("{} degree is in stall region. Please try smaller degrees.".format(self.get_value_wingangle()+self.get_value_roottwist()))
                        msg2.setWindowTitle("Error")
                        msg2.exec_()
                        self.lift_coefficient_value.clear()
                        self.lift_coefficient_value.setStyleSheet("QLineEdit"
                                                "{"
                                                "background : white;"
                                                "}")
                        self.wing_angle_QSpinBox.setStyleSheet("QDoubleSpinBox"
                                                "{"
                                                "background : yellow;"
                                                "}")
                        self.root_twist_angle_QSpinBox.setStyleSheet("QDoubleSpinBox"
                                                "{"
                                                "background : yellow;"
                                                "}")
            else:
                msg3 = QMessageBox()
                msg3.setIcon(QMessageBox.Critical)
                msg3.setText("Please select Airfoil")
                msg3.setWindowTitle("Error")
                msg3.exec_()
                self.lift_coefficient_value.clear()
                self.lift_coefficient_value.setStyleSheet("QLineEdit"
                                                "{"
                                                "background : white;"
                                                "}")
            figure = Figure()
            axes = figure.gca()
            axes.plot(y_s, CL1, marker="o")
            axes.set_title("Lifting Line Theory \n Lift Distribution")
            axes.set_xlabel("Semi-span location (m)")
            axes.set_ylabel("Lift coefficient")
            axes.grid(True)
            canvas = FigureCanvas(figure)
            proxy_widget = self.scene.addWidget(canvas)
            self.lift_distribution.resize(650, 500)
            self.lift_distribution.show()
            
            
            if AR < 7:
                self.lift_distribution.hide()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Aspect Ratio of wing below than 7. To accurate calculation please modify wing span or chords values.")
                msg.setInformativeText('Current Aspect Ratio of wing = {}'.format(round(AR,5)))
                msg.setWindowTitle("Error")
                msg.exec_()
                self.lift_coefficient_value.setStyleSheet("QLineEdit"
                                    "{"
                                    "background : #FC6464;"
                                    "}")
                line_wingspan = self.wing_span_QSpinBox.lineEdit()
                line_wingspan.setStyleSheet("QLineEdit"
                               "{"
                               "background-color : yellow;"
                               "}")
                line_rootchord = self.root_chord_QSpinBox.lineEdit()
                line_rootchord.setStyleSheet("QLineEdit"
                               "{"
                               "background-color : yellow;"
                               "}")
                line_tipchord = self.tip_chord_QSpinBox.lineEdit()
                line_tipchord.setStyleSheet("QLineEdit"
                               "{"
                               "background-color : yellow;"
                               "}")
            else:
                self.lift_coefficient_value.setStyleSheet("QLineEdit"
                                    "{"
                                    "background : lightgreen;"
                                    "}")
                line_wingspan = self.wing_span_QSpinBox.lineEdit()
                line_wingspan.setStyleSheet("QLineEdit"
                               "{"
                               "background-color : white;"
                               "}")
                line_rootchord = self.root_chord_QSpinBox.lineEdit()
                line_rootchord.setStyleSheet("QLineEdit"
                               "{"
                               "background-color : white;"
                               "}")
                line_tipchord = self.tip_chord_QSpinBox.lineEdit()
                line_tipchord.setStyleSheet("QLineEdit"
                               "{"
                               "background-color : white;"
                               "}")
            
                
            self.lift_coefficient_value.setText(str(round(CL_wing,10)))
        except:
           pass
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(284, 450)
        MainWindow.setMinimumSize(QtCore.QSize(284, 450))
        MainWindow.setMaximumSize(QtCore.QSize(284, 450))
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        MainWindow.setWindowIcon(QtGui.QIcon('winglogo.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.airfoils_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.airfoils_combobox.setGeometry(QtCore.QRect(20, 10, 241, 22))
        self.airfoils_combobox.setFrame(True)
        self.airfoils_combobox.setObjectName("airfoils_combobox")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.airfoils_combobox.addItem("")
        self.wing_span = QtWidgets.QLabel(self.centralwidget)
        self.wing_span.setGeometry(QtCore.QRect(20, 50, 141, 16))
        self.wing_span.setObjectName("wing_span")
        self.root_chord = QtWidgets.QLabel(self.centralwidget)
        self.root_chord.setGeometry(QtCore.QRect(20, 80, 151, 16))
        self.root_chord.setObjectName("root_chord")
        self.tip_chord = QtWidgets.QLabel(self.centralwidget)
        self.tip_chord.setGeometry(QtCore.QRect(20, 110, 141, 16))
        self.tip_chord.setObjectName("tip_chord")
        self.root_twist_angle = QtWidgets.QLabel(self.centralwidget)
        self.root_twist_angle.setGeometry(QtCore.QRect(20, 170, 141, 16))
        self.root_twist_angle.setObjectName("root_twist_angle")
        self.wing_angle = QtWidgets.QLabel(self.centralwidget)
        self.wing_angle.setGeometry(QtCore.QRect(20, 140, 151, 16))
        self.wing_angle.setObjectName("wing_angle")
        self.tip_twist_angle = QtWidgets.QLabel(self.centralwidget)
        self.tip_twist_angle.setGeometry(QtCore.QRect(20, 200, 151, 16))
        self.tip_twist_angle.setObjectName("tip_twist_angle")
        self.lift_curve_slope = QtWidgets.QLabel(self.centralwidget)
        self.lift_curve_slope.setGeometry(QtCore.QRect(20, 230, 151, 16))
        self.lift_curve_slope.setObjectName("lift_curve_slope")
        self.wing_span_QSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.wing_span_QSpinBox.setGeometry(QtCore.QRect(170, 50, 91, 22))
        self.wing_span_QSpinBox.setMaximum(999999999.99)
        self.wing_span_QSpinBox.setDecimals(5)
        self.wing_span_QSpinBox.setObjectName("wing_span_QSpinBox")
        self.root_chord_QSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.root_chord_QSpinBox.setGeometry(QtCore.QRect(170, 80, 91, 22))
        self.root_chord_QSpinBox.setMaximum(999999999.99)
        self.root_chord_QSpinBox.setDecimals(5)
        self.root_chord_QSpinBox.setObjectName("root_chord_QSpinBox")
        self.tip_chord_QSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.tip_chord_QSpinBox.setGeometry(QtCore.QRect(170, 110, 91, 22))
        self.tip_chord_QSpinBox.setMaximum(999999999.99)
        self.tip_chord_QSpinBox.setDecimals(5)
        self.tip_chord_QSpinBox.setObjectName("tip_chord_QSpinBox")
        self.wing_angle_QSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.wing_angle_QSpinBox.setGeometry(QtCore.QRect(170, 140, 91, 22))
        self.wing_angle_QSpinBox.setMaximum(9999.99)
        self.wing_angle_QSpinBox.setMinimum(-9999.99)
        self.wing_angle_QSpinBox.setObjectName("wing_angle_QSpinBox")
        self.root_twist_angle_QSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.root_twist_angle_QSpinBox.setGeometry(QtCore.QRect(170, 170, 91, 22))
        self.root_twist_angle_QSpinBox.setMaximum(9999.99)
        self.root_twist_angle_QSpinBox.setMinimum(-9999.99)
        self.root_twist_angle_QSpinBox.setObjectName("root_twist_angle_QSpinBox")
        self.tip_twist_angle_QSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.tip_twist_angle_QSpinBox.setGeometry(QtCore.QRect(170, 200, 91, 22))
        self.tip_twist_angle_QSpinBox.setMaximum(9999.99)
        self.tip_twist_angle_QSpinBox.setMinimum(-9999.99)
        self.tip_twist_angle_QSpinBox.setObjectName("tip_twist_angle_QSpinBox")
        self.lift_curve_slope_QSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.lift_curve_slope_QSpinBox.setGeometry(QtCore.QRect(170, 230, 91, 22))
        self.lift_curve_slope_QSpinBox.setDecimals(3)
        self.lift_curve_slope_QSpinBox.setMaximum(6.283)
        self.lift_curve_slope_QSpinBox.setSingleStep(1.0)
        self.lift_curve_slope_QSpinBox.setProperty("value", 6.283)
        self.lift_curve_slope_QSpinBox.setObjectName("lift_curve_slope_QSpinBox")
        self.lift_coefficient_value = QtWidgets.QLineEdit(self.centralwidget)
        self.lift_coefficient_value.setGeometry(QtCore.QRect(170, 360, 91, 20))
        self.lift_coefficient_value.setText("")
        self.lift_coefficient_value.setReadOnly(True)
        self.lift_coefficient_value.setObjectName("lift_coefficient_value")
        self.lift_coefficient = QtWidgets.QLabel(self.centralwidget)
        self.lift_coefficient.setGeometry(QtCore.QRect(20, 360, 161, 21))
        font = QtGui.QFont()
        font.setFamily("Noto Serif")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lift_coefficient.setFont(font)
        self.lift_coefficient.setTextFormat(QtCore.Qt.AutoText)
        self.lift_coefficient.setObjectName("lift_coefficient")
        self.scene = QtWidgets.QGraphicsScene()
        self.lift_distribution = QtWidgets.QGraphicsView(self.scene)
        # self.lift_distribution.setGeometry(QtCore.QRect(10, 410, 261, 192))
        # self.lift_distribution.setFrameShadow(QtWidgets.QFrame.Plain)
        # self.lift_distribution.setObjectName("lift_distribution")
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 310, 81, 31))
        self.pushButton.setObjectName("pushButton")
        self.reynolds_number = QtWidgets.QLabel(self.centralwidget)
        self.reynolds_number.setGeometry(QtCore.QRect(20, 260, 151, 16))
        self.reynolds_number.setObjectName("reynolds_number")
        self.reynolds_number_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.reynolds_number_combobox.setGeometry(QtCore.QRect(170, 260, 91, 22))
        self.reynolds_number_combobox.setObjectName("reynolds_number_combobox")
        self.reynolds_number_combobox.addItem("")
        self.reynolds_number_combobox.addItem("")
        self.reynolds_number_combobox.addItem("")
        self.reynolds_number_combobox.addItem("")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 284, 21))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuHelp.menuAction())
        
        #### connections 
        self.wing_span_QSpinBox.valueChanged.connect(self.get_value_wingspan)
        self.root_chord_QSpinBox.valueChanged.connect(self.get_value_rootchord)
        self.tip_chord_QSpinBox.valueChanged.connect(self.get_value_tipchord)
        self.wing_angle_QSpinBox.valueChanged.connect(self.get_value_wingangle)
        self.root_twist_angle_QSpinBox.valueChanged.connect(self.get_value_roottwist)
        self.tip_twist_angle_QSpinBox.valueChanged.connect(self.get_value_tiptwist)
        self.lift_curve_slope_QSpinBox.valueChanged.connect(self.get_value_liftcurveslope)
        #
        self.reynolds_number_combobox.activated.connect(self.get_value_reynolds_number)
        self.airfoils_combobox.activated.connect(self.get_value_airfoils)
        #
        self.pushButton.clicked.connect(self.main_run)
        
       
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Lift Coefficient Calculator"))
        self.airfoils_combobox.setCurrentText(_translate("MainWindow", "Select Airfoil..."))
        self.airfoils_combobox.setItemText(0, _translate("MainWindow", "Select Airfoil..."))
        self.airfoils_combobox.setItemText(1, _translate("MainWindow", "naca1408-il"))
        self.airfoils_combobox.setItemText(2, _translate("MainWindow", "naca1410-il"))
        self.airfoils_combobox.setItemText(3, _translate("MainWindow", "naca1412-il"))
        self.airfoils_combobox.setItemText(4, _translate("MainWindow", "naca2408-il"))
        self.airfoils_combobox.setItemText(5, _translate("MainWindow", "naca2410-il"))
        self.airfoils_combobox.setItemText(6, _translate("MainWindow", "naca2411-il"))
        self.airfoils_combobox.setItemText(7, _translate("MainWindow", "naca2412-il"))
        self.airfoils_combobox.setItemText(8, _translate("MainWindow", "naca2415-il"))
        self.airfoils_combobox.setItemText(9, _translate("MainWindow", "naca2418-il"))
        self.airfoils_combobox.setItemText(10, _translate("MainWindow", "naca2421-il"))
        self.airfoils_combobox.setItemText(11, _translate("MainWindow", "naca2424-il"))
        self.airfoils_combobox.setItemText(12, _translate("MainWindow", "naca4412-il"))
        self.airfoils_combobox.setItemText(13, _translate("MainWindow", "naca4415-il"))
        self.airfoils_combobox.setItemText(14, _translate("MainWindow", "naca4418-il"))
        self.airfoils_combobox.setItemText(15, _translate("MainWindow", "naca4421-il"))
        self.airfoils_combobox.setItemText(16, _translate("MainWindow", "naca4424-il"))
        self.airfoils_combobox.setItemText(17, _translate("MainWindow", "naca6412-il"))
        self.airfoils_combobox.setItemText(18, _translate("MainWindow", "n2414-il"))
        self.airfoils_combobox.setItemText(19, _translate("MainWindow", "naca22112-jf"))
        self.airfoils_combobox.setItemText(20, _translate("MainWindow", "naca23012-il"))
        self.airfoils_combobox.setItemText(21, _translate("MainWindow", "naca23015-il"))
        self.airfoils_combobox.setItemText(22, _translate("MainWindow", "naca23018-il"))
        self.airfoils_combobox.setItemText(23, _translate("MainWindow", "naca23021-il"))
        self.airfoils_combobox.setItemText(24, _translate("MainWindow", "naca23024-il"))
        self.airfoils_combobox.setItemText(25, _translate("MainWindow", "naca23112-jf"))
        self.airfoils_combobox.setItemText(26, _translate("MainWindow", "naca24112-jf"))
        self.airfoils_combobox.setItemText(27, _translate("MainWindow", "naca25112-jf"))
        self.airfoils_combobox.setItemText(28, _translate("MainWindow", "n63010a-il"))
        self.airfoils_combobox.setItemText(29, _translate("MainWindow", "n63012a-il"))
        self.airfoils_combobox.setItemText(30, _translate("MainWindow", "n63015a-il"))
        self.airfoils_combobox.setItemText(31, _translate("MainWindow", "n63210-il"))
        self.airfoils_combobox.setItemText(32, _translate("MainWindow", "n63212-il"))
        self.airfoils_combobox.setItemText(33, _translate("MainWindow", "n63215-il"))
        self.airfoils_combobox.setItemText(34, _translate("MainWindow", "n63215b-il"))
        self.airfoils_combobox.setItemText(35, _translate("MainWindow", "n63412-il"))
        self.airfoils_combobox.setItemText(36, _translate("MainWindow", "n63415-il"))
        self.airfoils_combobox.setItemText(37, _translate("MainWindow", "n64008a-il"))
        self.airfoils_combobox.setItemText(38, _translate("MainWindow", "n64012-il"))
        self.airfoils_combobox.setItemText(39, _translate("MainWindow", "n64012a-il"))
        self.airfoils_combobox.setItemText(40, _translate("MainWindow", "n64015-il"))
        self.airfoils_combobox.setItemText(41, _translate("MainWindow", "n64015a-il"))
        self.airfoils_combobox.setItemText(42, _translate("MainWindow", "n64108-il"))
        self.airfoils_combobox.setItemText(43, _translate("MainWindow", "n64110-il"))
        self.airfoils_combobox.setItemText(44, _translate("MainWindow", "n64212-il"))
        self.airfoils_combobox.setItemText(45, _translate("MainWindow", "n64212ma-il"))
        self.airfoils_combobox.setItemText(46, _translate("MainWindow", "n64212mb-il"))
        self.airfoils_combobox.setItemText(47, _translate("MainWindow", "n64215-il"))
        self.airfoils_combobox.setItemText(48, _translate("MainWindow", "n66021-il"))
        self.airfoils_combobox.setItemText(49, _translate("MainWindow", "naca63206-il"))
        self.airfoils_combobox.setItemText(50, _translate("MainWindow", "naca63209-il"))
        self.airfoils_combobox.setItemText(51, _translate("MainWindow", "naca632615-il"))
        self.airfoils_combobox.setItemText(52, _translate("MainWindow", "naca632a015-il"))
        self.airfoils_combobox.setItemText(53, _translate("MainWindow", "naca633018-il"))
        self.airfoils_combobox.setItemText(54, _translate("MainWindow", "naca633218-il"))
        self.airfoils_combobox.setItemText(55, _translate("MainWindow", "naca633418-il"))
        self.airfoils_combobox.setItemText(56, _translate("MainWindow", "naca633618-il"))
        self.airfoils_combobox.setItemText(57, _translate("MainWindow", "naca634221-il"))
        self.airfoils_combobox.setItemText(58, _translate("MainWindow", "naca643418-il"))
        self.airfoils_combobox.setItemText(59, _translate("MainWindow", "naca643618-il"))
        self.airfoils_combobox.setItemText(60, _translate("MainWindow", "naca644221-il"))
        self.airfoils_combobox.setItemText(61, _translate("MainWindow", "naca644421-il"))
        self.airfoils_combobox.setItemText(62, _translate("MainWindow", "naca64a010-il"))
        self.airfoils_combobox.setItemText(63, _translate("MainWindow", "naca64a210-il"))
        self.airfoils_combobox.setItemText(64, _translate("MainWindow", "naca64a410-il"))
        self.airfoils_combobox.setItemText(65, _translate("MainWindow", "naca651212-il"))
        self.airfoils_combobox.setItemText(66, _translate("MainWindow", "naca651212a06-il"))
        self.airfoils_combobox.setItemText(67, _translate("MainWindow", "naca651412-il"))
        self.airfoils_combobox.setItemText(68, _translate("MainWindow", "naca65206-il"))
        self.airfoils_combobox.setItemText(69, _translate("MainWindow", "naca65209-il"))
        self.airfoils_combobox.setItemText(70, _translate("MainWindow", "naca65210-il"))
        self.airfoils_combobox.setItemText(71, _translate("MainWindow", "naca652215-il"))
        self.airfoils_combobox.setItemText(72, _translate("MainWindow", "naca652415-il"))
        self.airfoils_combobox.setItemText(73, _translate("MainWindow", "naca652415a05-il"))
        self.airfoils_combobox.setItemText(74, _translate("MainWindow", "naca653218-il"))
        self.airfoils_combobox.setItemText(75, _translate("MainWindow", "naca653618-il"))
        self.airfoils_combobox.setItemText(76, _translate("MainWindow", "naca65410-il"))
        self.airfoils_combobox.setItemText(77, _translate("MainWindow", "naca654221-il"))
        self.airfoils_combobox.setItemText(78, _translate("MainWindow", "naca654421-il"))
        self.airfoils_combobox.setItemText(79, _translate("MainWindow", "naca654421a05-il"))
        self.airfoils_combobox.setItemText(80, _translate("MainWindow", "naca66-018-il"))
        self.airfoils_combobox.setItemText(81, _translate("MainWindow", "naca661212-il"))
        self.airfoils_combobox.setItemText(82, _translate("MainWindow", "naca66206-il"))
        self.airfoils_combobox.setItemText(83, _translate("MainWindow", "naca66209-il"))
        self.airfoils_combobox.setItemText(84, _translate("MainWindow", "naca66210-il"))
        self.airfoils_combobox.setItemText(85, _translate("MainWindow", "naca662215-il"))
        self.airfoils_combobox.setItemText(86, _translate("MainWindow", "naca662415-il"))
        self.airfoils_combobox.setItemText(87, _translate("MainWindow", "naca663218-il"))
        self.airfoils_combobox.setItemText(88, _translate("MainWindow", "naca663418-il"))
        self.airfoils_combobox.setItemText(89, _translate("MainWindow", "naca664221-il"))
        self.airfoils_combobox.setItemText(90, _translate("MainWindow", "naca671215-il"))
        self.wing_span.setText(_translate("MainWindow", "Wing span (m)                      :"))
        self.root_chord.setText(_translate("MainWindow", "Root chord (m)                     :"))
        self.tip_chord.setText(_translate("MainWindow", "Tip chord (m)                        :"))
        self.root_twist_angle.setText(_translate("MainWindow", "Root twist angle (deg.)        :"))
        self.wing_angle.setText(_translate("MainWindow", "Wing setting angle (deg.)    :"))
        self.tip_twist_angle.setText(_translate("MainWindow", "Tip twist angle (deg.)           :"))
        self.lift_curve_slope.setText(_translate("MainWindow", "Lift curve slope                     :"))
        self.lift_coefficient.setText(_translate("MainWindow", "Lift Coefficient               :"))
        self.pushButton.setText(_translate("MainWindow", "Calculate"))
        self.reynolds_number.setText(_translate("MainWindow", "Reynolds number                  :"))
        self.reynolds_number_combobox.setItemText(0, _translate("MainWindow", "100_000"))
        self.reynolds_number_combobox.setItemText(1, _translate("MainWindow", "200_000"))
        self.reynolds_number_combobox.setItemText(2, _translate("MainWindow", "500_000"))
        self.reynolds_number_combobox.setItemText(3, _translate("MainWindow", "1_000_000"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
