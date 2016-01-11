#!/usr/bin/env python

import sys, socket
from PyQt4 import QtGui, QtCore

class Permitter(QtGui.QMainWindow):
    def __init__(self):
        super(Permitter, self).__init__()
        self.initUI()

    def initUI(self): 
        def isHostAvailable(host):
          port = 135                                                # port for checking remote registry
          s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          s.settimeout(0.5)
          try:
            print('Trying %s' % host)
            check = s.connect((host, port))
            return True
            s.close()
          except OSError:
            return False
            s.close()

        def mkSmth(host):
          print('host is %s' % host)

        self.setGeometry(500, 500, 400, 500)
        self.setWindowTitle("Permitter")
        self.show()

        with open("hosts.lst", 'r') as hosts:
          online_hosts=[]
          for host in hosts.read().splitlines():
            if host.strip() == '' or '#' in host[0]:                   # don`t touch empty and commented lines
              pass
            else:
              if isHostAvailable(host) == False:
                print("%s is unavailable" % host)
                pass
              else:
                online_hosts.append(host)
                  
        if online_hosts:
          table = QtGui.QTableWidget(self)
          table.resize(400, 400)
          table.setColumnCount(3)
          row_count = len(online_hosts)
          table.setRowCount(row_count)
          table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)    # to deny row editing
          table.setSelectionMode(QtGui.QTableWidget.NoSelection)    # to deny row selecting
          table.setHorizontalHeaderLabels(('Hostname', 'State', 'Button'))
          btn = QtGui.QPushButton(table)
          btn.setText('Change')
          table.itemDoubleClicked.connect(mkSmth)
          row_num = 0
          for online_host in sorted(online_hosts):
            table.setItem(row_num, 0, QtGui.QTableWidgetItem(online_host))
            table.setItem(row_num, 1, QtGui.QTableWidgetItem("status"))
            table.item(row_num, 1).setBackground(QtGui.QColor("green"))   # this may change background color
            
            table.setCellWidget(row_num, 2, btn)
            row_num += 1
          table.show()
        else:
          self.statusBar().showMessage('no host is available!')

def main():
    app = QtGui.QApplication(sys.argv)
    ex = Permitter()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
