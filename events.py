from PyQt5.uic import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class ChangeDetection(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('gui_v2.ui', self)
        self.show()

        #self.berechnen.clicked.connect(self.calculate)
        self.speichern.clicked.connect(self.save)
        self.oeffnen.clicked.connect(self.get_files)

    #def calculate(self):

    def save(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Datei speichern", "", "GeoTiff(*.tiff)", options=options)
        if fileName:
            print(fileName)

    def get_files(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        openfile, _ = QFileDialog.getOpenFileNames(self, "Files auswählen", "", "LAS-Punktwolke(*.las *.laz)", options=options)


    def x_min(self):
        input = QInputDialog.getDouble(self, "x_coord_min", "Minimale X-Koordinate", deicmals=3)
        print(input)


app = QApplication([])
window = ChangeDetection()
app.exec()
