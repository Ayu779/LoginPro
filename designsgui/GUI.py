from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

import pymysql
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
from stegano import lsb


class Ui_MainWindowMainPage(object):
    def onclicklogin(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindowLogin()
        self.ui.setupUi(self.window)
        MainWindowMainPage.hide()
        self.window.show()
        
    def onclickregister(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindowRegister()
        self.ui.setupUi(self.window)
        MainWindowMainPage.hide()
        self.window.show()
        
    def setupUi(self, MainWindowMainPage):
        MainWindowMainPage.setObjectName("MainWindowMainPage")
        MainWindowMainPage.resize(796, 457)
        self.centralwidget = QtWidgets.QWidget(MainWindowMainPage)
        self.centralwidget.setObjectName("centralwidget")
        self.Loginbuttonmainpage = QtWidgets.QPushButton(self.centralwidget)
        self.Loginbuttonmainpage.setGeometry(QtCore.QRect(80, 280, 171, 91))
        
        self.Loginbuttonmainpage.clicked.connect(self.onclicklogin)
        
        font = QtGui.QFont()
        font.setFamily("Caladea")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Loginbuttonmainpage.setFont(font)
        self.Loginbuttonmainpage.setObjectName("Loginbuttonmainpage")
        self.SignupButtonMainpage = QtWidgets.QPushButton(self.centralwidget)
        self.SignupButtonMainpage.setGeometry(QtCore.QRect(520, 280, 171, 91))
        
        self.SignupButtonMainpage.clicked.connect(self.onclickregister)
        
        font = QtGui.QFont()
        font.setFamily("Caladea")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.SignupButtonMainpage.setFont(font)
        self.SignupButtonMainpage.setObjectName("SignupButtonMainpage")
        self.Logomainpage = QtWidgets.QLabel(self.centralwidget)
        self.Logomainpage.setGeometry(QtCore.QRect(270, 0, 221, 231))
        self.Logomainpage.setObjectName("Logomainpage")
        MainWindowMainPage.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindowMainPage)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 796, 21))
        self.menubar.setObjectName("menubar")
        MainWindowMainPage.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindowMainPage)
        self.statusbar.setObjectName("statusbar")
        MainWindowMainPage.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindowMainPage)
        QtCore.QMetaObject.connectSlotsByName(MainWindowMainPage)

    def retranslateUi(self, MainWindowMainPage):
        _translate = QtCore.QCoreApplication.translate
        MainWindowMainPage.setWindowTitle(_translate("MainWindowMainPage", "MainWindow"))
        self.Loginbuttonmainpage.setText(_translate("MainWindowMainPage", "Login"))
        self.SignupButtonMainpage.setText(_translate("MainWindowMainPage", "Signup"))
        self.Logomainpage.setText(_translate("MainWindowMainPage", "<html><head/><body><p><img src=\":/image/aa.png\"/></p></body></html>"))
import abc_rc
class Ui_MainWindowRegister(object):
    def onclicklogin(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindowLogin()
        self.ui.setupUi(self.window)
        #MainWindowMainPage.hide()
        self.window.show()
    
    def onclickbrowse(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)

        if dlg.exec_():
           filenames = dlg.selectedFiles()
           self.Selectimageregisterinput.setText(filenames[0])
        
    def onclickregister(self):
        import re, time
        print("Registering User !")
        time.sleep(1)
        fname = self.fnameinputregister.text()
        userid = self.useridinputregister.text()
        email = self.emailregisterinput.text()
        password = self.passwordregisterinput.text()
        
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        
        image = self.Selectimageregisterinput.text()
        imagename = image.split("/")[-1]
        outimage = "C:/Users/ayush/Desktop/3rd Year/New folder/encryptedimage/" + imagename
        
        if(fname=="" or userid=="" or email=="" or password == "" or image==""):
            msg2 = QMessageBox()
            msg2.setWindowTitle("Error !")
            msg2.setText("All field are mandatory !")
            x = msg2.exec_()
        
        if(re.search(regex,email)):
            BLOCK_SIZE = 16
            pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
            unpad = lambda s: s[:-ord(s[len(s) - 1:])]
            passw = userid
            def encrypt(raw, password):
                private_key = hashlib.sha256(password.encode("utf-8")).digest()
                raw = pad(raw)
                iv = Random.new().read(AES.block_size)
                cipher = AES.new(private_key, AES.MODE_CBC, iv)
                return base64.b64encode(iv + cipher.encrypt(raw))
            
            idd = f'{email}:{password}'
            encrypted = str(encrypt(idd, passw)).split("'")[1]
            lsb.hide(image, message = encrypted).save(outimage)
            print("Registered User!")
            print("...")
            print("Encrypted Text: " + encrypted)
            print("Processing Steganography")
            time.sleep(0.5)
            print("Image Encryption Done ! Please Find the image in Encrypted Image Folder")
            
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error !")
            msg.setText("Invalid Email")
            x = msg.exec_()
            
        flag=0;
        flag2=0
        try:
            db = pymysql.connect("localhost","root","","loginpro")
            flag=1
            print("db connected")
        except:
            print("error")

        if(flag==1):
            cursor = db.cursor()
            sql = "INSERT INTO `user` (`FullName`, `Userid`, `Email`, `Password`) VALUES (%s, %s, %s, %s);"
            try:
                cursor.execute(sql,(fname,userid,email,password))
                db.commit()
                flag2=1
                print("Registered User!")
                print("...")
                print("Encrypted Text: " + encrypted)
                print("Processing Steganography")
                time.sleep(0.5)
                print("Image Encryption Done ! Please Find the image in Encrypted Image Folder")
                print("\n\n\n\n\n")
            except Exception as e :
                msg3 = QMessageBox()
                msg3.setWindowTitle("Error !")
                msg3.setText(str(e))
                xx = msg3.exec_()
                
            if(flag2==1):
                self.window = QtWidgets.QMainWindow()
                self.ui = Ui_MainWindowafterregistration()
                self.ui.setupUi(self.window)
                #MainWindowMainPage.hide()
                self.window.show()
                self.emailregisterinput.setText("")
                self.fnameinputregister.setText("")
                self.useridinputregister.setText("")
                self.passwordregisterinput.setText("")
        
        
        
        
        
        
    def setupUi(self, MainWindowRegister):
        MainWindowRegister.setObjectName("MainWindowRegister")
        MainWindowRegister.resize(631, 596)
        self.centralwidget = QtWidgets.QWidget(MainWindowRegister)
        self.centralwidget.setObjectName("centralwidget")
        self.logoregister = QtWidgets.QLabel(self.centralwidget)
        self.logoregister.setGeometry(QtCore.QRect(200, 0, 231, 221))
        self.logoregister.setMinimumSize(QtCore.QSize(231, 221))
        self.logoregister.setObjectName("logoregister")
        self.fnamelabelregister = QtWidgets.QLabel(self.centralwidget)
        self.fnamelabelregister.setGeometry(QtCore.QRect(110, 250, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Caladea")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.fnamelabelregister.setFont(font)
        self.fnamelabelregister.setObjectName("fnamelabelregister")
        self.fnameinputregister = QtWidgets.QLineEdit(self.centralwidget)
        self.fnameinputregister.setGeometry(QtCore.QRect(300, 250, 251, 21))
        self.fnameinputregister.setObjectName("fnameinputregister")
        self.useridregisterlabel = QtWidgets.QLabel(self.centralwidget)
        self.useridregisterlabel.setGeometry(QtCore.QRect(110, 290, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Caladea")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.useridregisterlabel.setFont(font)
        self.useridregisterlabel.setObjectName("useridregisterlabel")
        self.useridinputregister = QtWidgets.QLineEdit(self.centralwidget)
        self.useridinputregister.setGeometry(QtCore.QRect(300, 290, 251, 21))
        self.useridinputregister.setObjectName("useridinputregister")
        self.Emailregisterlabel = QtWidgets.QLabel(self.centralwidget)
        self.Emailregisterlabel.setGeometry(QtCore.QRect(110, 330, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Caladea")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Emailregisterlabel.setFont(font)
        self.Emailregisterlabel.setObjectName("Emailregisterlabel")
        self.emailregisterinput = QtWidgets.QLineEdit(self.centralwidget)
        self.emailregisterinput.setGeometry(QtCore.QRect(300, 330, 251, 21))
        self.emailregisterinput.setObjectName("emailregisterinput")
        self.Passwordregisterlabel = QtWidgets.QLabel(self.centralwidget)
        self.Passwordregisterlabel.setGeometry(QtCore.QRect(110, 370, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Caladea")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Passwordregisterlabel.setFont(font)
        self.Passwordregisterlabel.setObjectName("Passwordregisterlabel")
        self.passwordregisterinput = QtWidgets.QLineEdit(self.centralwidget)
        self.passwordregisterinput.setGeometry(QtCore.QRect(300, 370, 251, 21))
        self.passwordregisterinput.setObjectName("passwordregisterinput")
        self.passwordregisterinput.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.selectimageregisterlabel = QtWidgets.QLabel(self.centralwidget)
        self.selectimageregisterlabel.setGeometry(QtCore.QRect(110, 410, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Caladea")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.selectimageregisterlabel.setFont(font)
        self.selectimageregisterlabel.setObjectName("selectimageregisterlabel")
        self.browseregisterbutton = QtWidgets.QPushButton(self.centralwidget)
        self.browseregisterbutton.setGeometry(QtCore.QRect(480, 440, 75, 23))
        self.browseregisterbutton.setObjectName("browseregisterbutton")
        
        self.browseregisterbutton.clicked.connect(self.onclickbrowse)
        
        self.submitregisterbutton = QtWidgets.QPushButton(self.centralwidget)
        self.submitregisterbutton.setGeometry(QtCore.QRect(460, 490, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Caladea")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.submitregisterbutton.setFont(font)
        self.submitregisterbutton.setObjectName("submitregisterbutton")
        
        self.submitregisterbutton.clicked.connect(self.onclickregister)
        
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(90, 460, 271, 17))
        self.checkBox.setObjectName("checkBox")
        self.Selectimageregisterinput = QtWidgets.QLineEdit(self.centralwidget)
        self.Selectimageregisterinput.setGeometry(QtCore.QRect(300, 410, 251, 21))
        self.Selectimageregisterinput.setObjectName("Selectimageregisterinput")
        self.Loginbuttonregister = QtWidgets.QPushButton(self.centralwidget)
        self.Loginbuttonregister.setGeometry(QtCore.QRect(100, 490, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Caladea")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Loginbuttonregister.setFont(font)
        self.Loginbuttonregister.setObjectName("Loginbuttonregister")
        
        self.Loginbuttonregister.clicked.connect(self.onclicklogin)
        
        MainWindowRegister.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindowRegister)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 631, 21))
        self.menubar.setObjectName("menubar")
        MainWindowRegister.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindowRegister)
        self.statusbar.setObjectName("statusbar")
        MainWindowRegister.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindowRegister)
        QtCore.QMetaObject.connectSlotsByName(MainWindowRegister)

    def retranslateUi(self, MainWindowRegister):
        _translate = QtCore.QCoreApplication.translate
        MainWindowRegister.setWindowTitle(_translate("MainWindowRegister", "MainWindow"))
        self.logoregister.setText(_translate("MainWindowRegister", "<html><head/><body><p><img src=\":/image2/images-removebg-preview.png\"/></p></body></html>"))
        self.fnamelabelregister.setText(_translate("MainWindowRegister", "Full Name"))
        self.useridregisterlabel.setText(_translate("MainWindowRegister", "User ID"))
        self.Emailregisterlabel.setText(_translate("MainWindowRegister", "Email"))
        self.Passwordregisterlabel.setText(_translate("MainWindowRegister", "Password"))
        self.selectimageregisterlabel.setText(_translate("MainWindowRegister", "Select Image"))
        self.browseregisterbutton.setText(_translate("MainWindowRegister", "Browse..."))
        self.submitregisterbutton.setText(_translate("MainWindowRegister", "Register"))
        self.checkBox.setText(_translate("MainWindowRegister", "I agree to all the Terms and Conditions"))
        #self.backbuttonregister.setText(_translate("MainWindowRegister", "Back"))
        self.Loginbuttonregister.setText(_translate("MainWindowRegister", "Login"))
import abcd_rc

class Ui_MainWindowLogin(object):  
    def onclickregister(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindowRegister()
        self.ui.setupUi(self.window)
        #MainWindowLogin.hide()
        self.window.show()
        
    def onclickbrowse(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)

        if dlg.exec_():
           filenames = dlg.selectedFiles()
           self.inputimagelogin.setText(filenames[0])
           print("Selected Image: " + filenames[0])
        
    def onclicklogin(self):
        print("onclicklogin() called...")
        userid = self.useridinputlogin.text()
        pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
        unpad = lambda s: s[:-ord(s[len(s) - 1:])]
        def decrypt(enc, password):
            private_key = hashlib.sha256(password.encode("utf-8")).digest()
            enc = base64.b64decode(enc)
            iv = enc[:16]
            cipher = AES.new(private_key, AES.MODE_CBC, iv)
            return unpad(cipher.decrypt(enc[16:]))
        
        img = self.inputimagelogin.text()
        try:
            text = lsb.reveal(img)
            print("On decoding the image the text we found : " + text)
        except Exception as e :
            if(str(e) == "'str' object has no attribute 'read'"):
                msg7 = QMessageBox()
                msg7.setWindowTitle("Error !")
                msg7.setText("All Fields are Required.")
                xy = msg7.exec_()
        aaa = decrypt(text,userid)
        aaa= str(aaa).split("'")[1]
        print("Decryption Started")
        print("Text After Decryption : " + aaa)
        
        cred =aaa.split(":")
        flag=0
        if(img=="" or userid ==""):
            msg6 = QMessageBox()
            msg6.setWindowTitle("Error !")
            msg6.setText("All Fields are Required.")
            xy = msg6.exec_()
        else:
            try:
                db = pymysql.connect("localhost","root","","loginpro")
                flag=1
                print("db connected")
            except:
                print("error")

            if(flag==1):
                cursor = db.cursor()
                sql = f"SELECT password FROM user WHERE email = '{cred[0]}'"
                cursor.execute(sql)
                results = cursor.fetchone()
                if(results):
                    if(results[0] == cred[1]):
                        self.window = QtWidgets.QMainWindow()
                        self.ui = Ui_MainWindowafterlogin()
                        self.ui.setupUi(self.window)
                        #MainWindowMainPage.hide()
                        self.window.show()
                    else:
                        msg4 = QMessageBox()
                        msg4.setWindowTitle("Error !")
                        msg4.setText("Wrong UserId for the Image")
                        xy = msg4.exec_()
                else:
                    msg5= QMessageBox()
                    msg5.setWindowTitle("Error !")
                    msg5.setText("Username Not Found !")
                    xz = msg5.exec_()
                
        self.inputimagelogin.setText("")
        self.useridinputlogin.setText("")
    def setupUi(self, MainWindowLogin):
        MainWindowLogin.setObjectName("MainWindowLogin")
        MainWindowLogin.resize(631, 596)
        self.centralwidget = QtWidgets.QWidget(MainWindowLogin)
        self.centralwidget.setObjectName("centralwidget")
        self.Logologinpage = QtWidgets.QLabel(self.centralwidget)
        self.Logologinpage.setGeometry(QtCore.QRect(200, 20, 241, 221))
        self.Logologinpage.setMinimumSize(QtCore.QSize(211, 191))
        self.Logologinpage.setObjectName("Logologinpage")
        self.useridlabellogin = QtWidgets.QLabel(self.centralwidget)
        self.useridlabellogin.setGeometry(QtCore.QRect(100, 310, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Caladea")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.useridlabellogin.setFont(font)
        self.useridlabellogin.setObjectName("useridlabellogin")
        self.useridinputlogin = QtWidgets.QLineEdit(self.centralwidget)
        self.useridinputlogin.setGeometry(QtCore.QRect(300, 310, 281, 21))
        self.useridinputlogin.setObjectName("useridinputlogin")
        self.imagelabellogin = QtWidgets.QLabel(self.centralwidget)
        self.imagelabellogin.setGeometry(QtCore.QRect(100, 370, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Caladea")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.imagelabellogin.setFont(font)
        self.imagelabellogin.setObjectName("imagelabellogin")
        self.inputimagelogin = QtWidgets.QLineEdit(self.centralwidget)
        self.inputimagelogin.setGeometry(QtCore.QRect(300, 370, 281, 21))
        self.inputimagelogin.setObjectName("inputimagelogin")
        self.RegisterButtonLogin = QtWidgets.QPushButton(self.centralwidget)
        self.RegisterButtonLogin.setGeometry(QtCore.QRect(130, 490, 91, 41))
        
        self.RegisterButtonLogin.clicked.connect(self.onclickregister)
        
        
        font = QtGui.QFont()
        font.setFamily("Caladea")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.RegisterButtonLogin.setFont(font)
        self.RegisterButtonLogin.setObjectName("RegisterButtonLogin")
        '''self.RegisterButtonLogin = QtWidgets.QPushButton(self.centralwidget)
        self.RegisterButtonLogin.setGeometry(QtCore.QRect(300, 490, 91, 41))
        
        self.RegisterButtonLogin.clicked.connect(self.onclickregister)
        
        
        font = QtGui.QFont()
        font.setFamily("Caladea")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.RegisterButtonLogin.setFont(font)
        self.RegisterButtonLogin.setObjectName("RegisterButtonLogin")'''
        self.submitlogin = QtWidgets.QPushButton(self.centralwidget)
        self.submitlogin.setGeometry(QtCore.QRect(470, 490, 91, 41))
        
        self.submitlogin.clicked.connect(self.onclicklogin)
        
        font = QtGui.QFont()
        font.setFamily("Caladea")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.submitlogin.setFont(font)
        self.submitlogin.setObjectName("submitlogin")
        self.broesebuttonlogin = QtWidgets.QPushButton(self.centralwidget)
        self.broesebuttonlogin.setGeometry(QtCore.QRect(510, 400, 75, 23))
        self.broesebuttonlogin.setObjectName("broesebuttonlogin")
        self.broesebuttonlogin.clicked.connect(self.onclickbrowse)
        MainWindowLogin.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindowLogin)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 631, 21))
        self.menubar.setObjectName("menubar")
        MainWindowLogin.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindowLogin)
        self.statusbar.setObjectName("statusbar")
        MainWindowLogin.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindowLogin)
        QtCore.QMetaObject.connectSlotsByName(MainWindowLogin)

    def retranslateUi(self, MainWindowLogin):
        _translate = QtCore.QCoreApplication.translate
        MainWindowLogin.setWindowTitle(_translate("MainWindowLogin", "MainWindow"))
        self.Logologinpage.setText(_translate("MainWindowLogin", "<html><head/><body><p><img src=\":/images3/images-removebg-preview.png\"/></p></body></html>"))
        self.useridlabellogin.setText(_translate("MainWindowLogin", "User ID"))
        self.imagelabellogin.setText(_translate("MainWindowLogin", "Enter ID IMAGE"))
        #self.BackButtonLogin.setText(_translate("MainWindowLogin", "Register"))
        self.RegisterButtonLogin.setText(_translate("MainWindowLogin", "Register"))
        self.submitlogin.setText(_translate("MainWindowLogin", "Login"))
        self.broesebuttonlogin.setText(_translate("MainWindowLogin", "Browse..."))
import abcde_rc

class Ui_MainWindowafterregistration(object):
    def setupUi(self, MainWindowafterregistration):
        MainWindowafterregistration.setObjectName("MainWindowafterregistration")
        MainWindowafterregistration.resize(631, 596)
        self.centralwidget = QtWidgets.QWidget(MainWindowafterregistration)
        self.centralwidget.setObjectName("centralwidget")
        self.greentickafterregistration = QtWidgets.QLabel(self.centralwidget)
        self.greentickafterregistration.setGeometry(QtCore.QRect(200, 70, 231, 221))
        self.greentickafterregistration.setObjectName("greentickafterregistration")
        self.Affterregistrationmessage = QtWidgets.QTextBrowser(self.centralwidget)
        self.Affterregistrationmessage.setGeometry(QtCore.QRect(80, 360, 471, 151))
        font = QtGui.QFont()
        font.setFamily("Caladea")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Affterregistrationmessage.setFont(font)
        self.Affterregistrationmessage.setObjectName("Affterregistrationmessage")
        MainWindowafterregistration.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindowafterregistration)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 631, 21))
        self.menubar.setObjectName("menubar")
        MainWindowafterregistration.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindowafterregistration)
        self.statusbar.setObjectName("statusbar")
        MainWindowafterregistration.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindowafterregistration)
        QtCore.QMetaObject.connectSlotsByName(MainWindowafterregistration)

    def retranslateUi(self, MainWindowafterregistration):
        _translate = QtCore.QCoreApplication.translate
        MainWindowafterregistration.setWindowTitle(_translate("MainWindowafterregistration", "MainWindow"))
        self.greentickafterregistration.setText(_translate("MainWindowafterregistration", "<html><head/><body><p><img src=\":/image4/test/Webp-removebg-preview.png\"/></p></body></html>"))
        self.Affterregistrationmessage.setHtml(_translate("MainWindowafterregistration", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Caladea\'; font-size:16pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:18pt;\">You\'ve Successfully Registered !! </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:18pt;\">Please Restart the Application and Login with the Image!! </span></p></body></html>"))
import abcdef_rc

class Ui_MainWindowafterlogin(object):
    def onclicklogout(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindowLogin()
        self.ui.setupUi(self.window)
        self.window.show()
        
    def setupUi(self, MainWindowafterlogin):
        MainWindowafterlogin.setObjectName("MainWindowafterlogin")
        MainWindowafterlogin.resize(631, 596)
        self.centralwidget = QtWidgets.QWidget(MainWindowafterlogin)
        self.centralwidget.setObjectName("centralwidget")
        self.Affterloginmessage = QtWidgets.QTextBrowser(self.centralwidget)
        self.Affterloginmessage.setGeometry(QtCore.QRect(180, 330, 271, 151))
        font = QtGui.QFont()
        font.setFamily("Caladea")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Affterloginmessage.setFont(font)
        self.Affterloginmessage.setObjectName("Affterloginmessage")
        self.greentick = QtWidgets.QLabel(self.centralwidget)
        self.greentick.setGeometry(QtCore.QRect(200, 60, 231, 221))
        self.greentick.setObjectName("greentick")
        self.Logoutbutton = QtWidgets.QPushButton(self.centralwidget)
        self.Logoutbutton.setGeometry(QtCore.QRect(544, 0, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Caladea")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Logoutbutton.setFont(font)
        self.Logoutbutton.setObjectName("Logoutbutton")
        self.Logoutbutton.clicked.connect(self.onclicklogout)
        MainWindowafterlogin.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindowafterlogin)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 631, 21))
        self.menubar.setObjectName("menubar")
        MainWindowafterlogin.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindowafterlogin)
        self.statusbar.setObjectName("statusbar")
        MainWindowafterlogin.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindowafterlogin)
        QtCore.QMetaObject.connectSlotsByName(MainWindowafterlogin)

    def retranslateUi(self, MainWindowafterlogin):
        _translate = QtCore.QCoreApplication.translate
        MainWindowafterlogin.setWindowTitle(_translate("MainWindowafterlogin", "MainWindow"))
        self.Affterloginmessage.setHtml(_translate("MainWindowafterlogin", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Caladea\'; font-size:16pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:18pt;\">You\'ve Successfully Login !! Congratulations !!</span></p></body></html>"))
        self.greentick.setText(_translate("MainWindowafterlogin", "<html><head/><body><p><img src=\":/image4/test/Webp-removebg-preview.png\"/></p></body></html>"))
        self.Logoutbutton.setText(_translate("MainWindowafterlogin", "Logout"))
import abcdef_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindowMainPage = QtWidgets.QMainWindow()
    ui = Ui_MainWindowMainPage()
    ui.setupUi(MainWindowMainPage)
    MainWindowMainPage.show()
    sys.exit(app.exec_())
