try:
    from PySide6 import QtCore, QtGui, QtWidgets
    from shiboken6 import wrapInstance
except:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui

import importlib
from openai import OpenAI
from . import api_key 
from . import mayaPilotUtil as aiReq
import re
import maya.cmds as cmds

importlib.reload(api_key)
importlib.reload(aiReq)

class mayaPilotDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(450, 800)
        self.setWindowTitle('NoCodeAnymore Maya')

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.setStyleSheet(
            '''
                font-family: Courier ;
                background-color: #161924;
                color: #51d24b;
            '''
        )
        self.mainLayout.setContentsMargins(25, 0, 25, 25)   # ไม่มีช่องว่างรอบ layout
        self.mainLayout.setSpacing(0)                    # ไม่มีช่องว่างระหว่าง widget

        sub_text = """
*******************************************************
*******************************************************
888888ba            a88888b.                dP          
88    `8b          d8'   `88                88          
88     88 .d8888b. 88        .d8888b. .d888b88 .d8888b. 
88     88 88'  `88 88        88'  `88 88'  `88 88ooood8 
88     88 88.  .88 Y8.   .88 88.  .88 88.  .88 88.  ... 
dP     dP `88888P'  Y88888P' `88888P' `88888P8 `88888P' 

.-.-.-.-.-.-.-.-.-.-.-. Anymore .-.-.-.-.-.-.-.-.-.-.-.                                                                                                                   
        """

        self.sublogoLabel = QtWidgets.QLabel(sub_text)
        font2 = QtGui.QFont("Courier")
        font2.setPointSize(5)
        font2.setPixelSize(5)
        self.sublogoLabel.setFont(font2)
        self.mainLayout.addWidget(self.sublogoLabel)

        self.inputLayout = QtWidgets.QFormLayout()
        self.mainLayout.addLayout(self.inputLayout)

        self.userLabel = QtWidgets.QLabel('You:')
        self.userTextEdit = QtWidgets.QTextEdit()
        self.userTextEdit.setReadOnly(True)     

        self.aiLabel = QtWidgets.QLabel('Ai:')
        self.aiTextEdit = QtWidgets.QTextEdit()
        #self.aiTextEdit.setReadOnly(True)

        #Header----------------------------------------------
        
        self.headerChat = QtWidgets.QTextEdit("Chat Transcript/")
        self.headerChat.setReadOnly(True)
        self.headerChat.setStyleSheet("""
            QTextEdit {
                font-family: Courier ;
                color: #161924;               /* สีตัวอักษร */
                background-color: #5ab556;    /* สีพื้นหลัง */
                border: 0.5px solid #5ab556;    /* สีขอบ */
                padding: 0px;                 /* ระยะห่างขอบ */
                font-size: 12pt;
                font-weight: bold;
        }
        """)
        self.headerChat.setFixedHeight(25)
        self.mainLayout.addWidget(self.headerChat)

        #หน้าต่างแสดงผลการแชท
        self.transcript_Layout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.transcript_Layout)

        self.transcript = QtWidgets.QTextEdit()
        self.transcript.setReadOnly(True)
        self.transcript.setStyleSheet("""
            QTextEdit {
                font-family: Chakra Petch ;
                color: white;               /* สีตัวอักษร */
                background-color: #161924;    /* สีพื้นหลัง */
                border: 0.5px solid #5ab556;    /* สีขอบ */
                padding: 6px;                 /* ระยะห่างขอบ */
                font-size: 8pt;
                line-height: 0.5px;
        }
        """)

        self.transcript_Layout.addWidget(self.transcript)
        self.userLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.userLayout)
        self.setLayout(self.mainLayout)

        #Layout กลาง
        self.inputLineEdit = QtWidgets.QLineEdit()
        self.inputLineEdit.setStyleSheet(
            '''
                QLineEdit {
                    font-family: Chakra Petch ;
                    background-color: #161924;
                    color: white;
                    border: 0.5px solid #5ab556;    
                    font-size: 10pt                             
                }
            '''
        ) 
        self.sendButton = QtWidgets.QPushButton('Send')
        self.sendButton.clicked.connect(self.on_send)
        self.sendButton.setStyleSheet(
            '''
                QPushButton {
                    background-color: #293B31;
                    font-color: black;
                    border: 0.5px solid  #5ab556;
                    font-size: 16px;
                    font-family: courier;
                    font-weight: bold;
                    padding: 8px 20px;
                }
                QPushButton:hover {
                    background-color: #0E59F0;
                }
                QPushButton:pressed {
                    background-color: #0EF065;
                }
            ''')

        self.userLayout.addWidget(self.inputLineEdit)
        self.userLayout.addWidget(self.sendButton)

        self.codeLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.codeLayout)

        self.codescript = QtWidgets.QTextEdit()
        self.codescript.setText("")
        # เชื่อมต่อสัญญาณ textChanged ไปยังเมธอด (Slot) ที่ชื่อ on_code_changed
        #self.codescript.textChanged.connect(self.runCode)

        #self.codescript.setReadOnly(True)
        self.codescript.setStyleSheet("""
            QTextEdit {
                font-family: Chakra Petch ;
                color: white;               /* สีตัวอักษร */
                background-color: #161924;    /* สีพื้นหลัง */
                border: 0.5px solid #5ab556;    /* สีขอบ */
                padding: 6px;                 /* ระยะห่างขอบ */
                font-size: 8pt;
                line-height: 0.5px;
        }
        """)
        self.codeLayout.addWidget(self.codescript)

        # Layout ปุ่ม ----------------------------------------------

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.buttonLayout)

        # ปุ่ม Close Button ----------------------------------------

        self.closeBtLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.addLayout(self.closeBtLayout)

        self.closeButton = QtWidgets.QPushButton('Close')
        self.closeButton.setStyleSheet(
            '''
                QPushButton {
                    background-color: #293B31;
                    font-color: black;
                    border: 0.5px solid  #5ab556;
                    font-size: 16px;
                    font-family: courier;
                    font-weight: bold;
                    padding: 13px 20px;
                }
                QPushButton:hover {
                    background-color: #0E59F0;
                }
                QPushButton:pressed {
                    background-color: #0EF065;
                }
            ''')

        self.closeBtLayout.addWidget(self.closeButton)
        self.closeButton.clicked.connect(self.close)       
        self.closeBtLayout.addStretch()

        # ปุ่ม Save Button ----------------------------------------
        self.saveButton = QtWidgets.QPushButton('save')
        self.saveButton.clicked.connect(self.saveCode)  
        self.saveButton.setStyleSheet(
            '''
                QPushButton {
                    background-color: #293B31;
                    font-color: black;
                    border: 0.5px solid  #5ab556;
                    font-size: 16px;
                    font-family: courier;
                    font-weight: bold;
                    padding: 13px 20px;
                }
                QPushButton:hover {
                    background-color: #0E59F0;
                }
                QPushButton:pressed {
                    background-color: #0EF065;
                }
            ''')
        self.buttonLayout.addWidget(self.saveButton)
             
        # ปุ่ม Run Button ----------------------------------------
        self.runButton = QtWidgets.QPushButton('RunCode')
        self.runButton.setStyleSheet(
            '''
                QPushButton {
                    background-color: #293B31;
                    font-color: black;
                    border: 0.5px solid  #5ab556;
                    font-size: 16px;
                    font-family: courier;
                    font-weight: bold;
                    padding: 13px 20px;
                }
                QPushButton:hover {
                    background-color: #0E59F0;
                }
                QPushButton:pressed {
                    background-color: #0EF065;
                }
            ''')
        self.runButton.clicked.connect(self.runCode)
        self.buttonLayout.addWidget(self.runButton)

    def onClickRequestResFromAI(self): 
        userInput = self.inputLineEdit.text()
        aiReq.requestResFromAI(userInput)
        
    def _append(self, who, text):

        self.transcript.append(f"[{who}]")
        self.transcript.append(text)
        self.transcript.append("")
        #aiReq.requestResFromAI(userInput)

    def on_send(self, *arg):
        user_Label = "You"
        ai_Label = "AI"

        q = self.inputLineEdit.text()
        if not q:
            return

        self._append(f'{user_Label}', q)  

        userInput = self.inputLineEdit.text()
        a = aiReq.requestResFromAI(userInput)

        self._append(f'{ai_Label}', a)
        self.inputLineEdit.clear()

        resText = a
        #code_res ไปอยู่ใน self เพื่อให้ทำงานข้าม def ได้

        self.code_res = aiReq.codeRequest(resText)
        self.codescript.setText(self.code_res)
        self.newcode = self.codescript.toPlainText()

    def saveCode(self, *args):
        print("save แล้ว")
        self.newcode = self.codescript.toPlainText()

        
    def runCode(self,  *arg):
        exec(self.newcode)
        print(self.newcode)

def run():
    global ui
    try:
        ui.close()
    except:
        pass
    mayaMainWindow = omui.MQtUtil.mainWindow()
    ptr = wrapInstance(int(mayaMainWindow), QtWidgets.QWidget)
    ui = mayaPilotDialog(parent=ptr)
    ui.show()
