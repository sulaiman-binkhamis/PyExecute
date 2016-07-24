import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import pyqtSlot
import StringIO
import contextlib

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

if __name__ == '__main__':
    app = QApplication(sys.argv)

    layout = QGridLayout()

    grid1 = QGridLayout()
    grid2 = QGridLayout()
    
    editor = QTextEdit()
    editor.setFontPointSize(10)
    output = QTextEdit()
    output.setFontPointSize(10)
    output.setEnabled(False)
    error = QTextEdit()
    error.setFontPointSize(10)
    error.setEnabled(False)

    l1 = QLabel()
    l1.setText("Output ->")
    l2 = QLabel()
    l2.setText("Errors ->")

    run = QPushButton('Run')
    @pyqtSlot()
    def on_click():
        code = str(editor.toPlainText())
        code = "errors=[]\n" + code
        code = code.split('\n')

        for i in range(1,len(code)):
            try:
                code[i]=code[i].replace('    ','\t\t')
            except:
                pass
            try:
                x = code[i].strip()
                if(x[0]=='#'):
                    code.remove(code[i])
            except:
                pass

        for i in range(1,len(code)):
            if(len(code[i])==0):
                continue
            if(':' in code[i] or '@' in code[i] or '__name' in code[i]):
                continue
            x = code[i]
            cnt = x.count('\t')
            x = (cnt*'\t')+"try:\n\t"+code[i]+'\n'+(cnt*'\t')+"except Exception as e:\n"+cnt*'\t'+"\terrors.append('Line '+str("+str(i)+")+' : '+str(e))"
            code[i] = x

        code_formatted = ""
        for x in code:
            code_formatted += x+'\n'

        #code_formatted += "sys.exit()"

        #print(code_formatted)

        with stdoutIO() as res:
            exec code_formatted

        output.setText(res.getvalue())
        
        err = ""
        for x in errors:
            err += x+'\n'

        error.setText(err)
        
    run.clicked.connect(on_click)

    grid1.addWidget(editor,0,1)
    grid1.addWidget(run,1,1)
    grid2.addWidget(l1,0,1)
    grid2.addWidget(l2,0,2)
    grid2.addWidget(output,1,1)
    grid2.setSpacing(20)
    grid2.addWidget(error,1,2)
    layout.addItem(grid1)
    layout.addItem(grid2)

    editor_window = QWidget()
    editor_window.setLayout(layout)
    editor_window.showMaximized()
    app.exec_()
