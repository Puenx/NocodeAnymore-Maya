from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance
import importlib
import maya.OpenMayaUI as omui
from openai import OpenAI
from . import api_key 
from . import ai_request as aiReq
import re
import maya.cmds as cmds

importlib.reload(api_key)
importlib.reload(aiReq)
print(";")

class mayaPilotDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(700, 520)
        self.setWindowTitle('NoCodeAnymore Maya')

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.inputLayout = QtWidgets.QFormLayout()
        self.mainLayout.addLayout(self.inputLayout)

        self.userLabel = QtWidgets.QLabel('User:')
        self.userTextEdit = QtWidgets.QTextEdit()
        self.userTextEdit.setReadOnly(True)     

        self.aiLabel = QtWidgets.QLabel('Ai:')
        self.aiTextEdit = QtWidgets.QTextEdit()
        #self.aiTextEdit.setReadOnly(True)


        self.transcript = QtWidgets.QTextEdit()
        self.transcript.setReadOnly(True)
        self.inputLayout.addWidget(self.transcript)


        self.userLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.userLayout)
        
        self.setLayout(self.mainLayout)

        self.inputLineEdit = QtWidgets.QLineEdit()
        self.sendButton = QtWidgets.QPushButton('Send')
        self.sendButton.clicked.connect(self.on_send)


        self.userLayout.addWidget(self.inputLineEdit)
        self.userLayout.addWidget(self.sendButton)

        self.codeLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.codeLayout)

        self.codescript = QtWidgets.QTextEdit()
        self.codescript.setReadOnly(True)
        self.codeLayout.addWidget(self.codescript)
        #--------------------------------------------------------

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.buttonLayout)

        self.closeBtLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.addLayout(self.closeBtLayout)

        self.closeButton = QtWidgets.QPushButton('Close')
        self.closeBtLayout.addWidget(self.closeButton)
        self.closeButton.clicked.connect(self.close)       
        self.closeBtLayout.addStretch()

        self.clearButton = QtWidgets.QPushButton('Clear')
        self.buttonLayout.addWidget(self.clearButton)
        self.runButton = QtWidgets.QPushButton('Run Code')
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
        q = self.inputLineEdit.text()
        if not q:
            return

        self._append("User", q)  

        userInput = self.inputLineEdit.text()
        a = aiReq.requestResFromAI(userInput)

        self._append("AI", a)
        self.inputLineEdit.clear()

        resText = a
        #code_res ไปอยู่ใน self เพื่อให้ทำงานข้าม def ได้

        self.code_res = aiReq.codeRequest(resText)
        self.codescript.append(self.code_res)
        

    def runCode(self,  *arg):
        exec(self.code_res)
        print(self.code_res)

'''
    def on_answer(self, result):
        self._append("AI", result)
        userInput = self.inputLineEdit.text()
        a =aiReq.requestResFromAI(userInput)
        #print(f"รหัสลับที่ได้รับมาคือ: {se}")


        #code = extract_python_code(result)
        if code:
            self.code_edit.setPlainText(code)
        else:
            self._append_ai("ไม่พบ code block ในคำตอบ ลองพิมพ์ใหม่ให้ระบุว่า 'ขอโค้ด python สำหรับ Maya'")

        self.send_btn.setEnabled(True)
        userInput = self.inputLineEdit.text()
        aiReq.requestResFromAI(userInput)
'''
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
