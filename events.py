from PyQt5.uic import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

#define GUI functions
class ChangeDetection(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('gui_v2.ui', self)
        self.show()

        # self.berechnen.clicked.connect(self.calculate)
        self.speichern.clicked.connect(self.save)

    # def calculate(self):

    def save(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename = QFileDialog.getSaveFileName(self, "Datei speichern", "", "GeoTiff(*.tiff)", options=options)
        print(filename)

    def get_files(self):
        global path_a
        global path_b
        path_a = QInputDialog.getText(self, "pfad_a", "Pfad zu Dateien")
        path_b = QInputDialog.getText(self, "pfad_b", "Pfad zu Dateien")

    def cooridnates(self):
        global minx
        global miny
        global maxx
        global maxy
        global extent
        minx = QInputDialog.getDouble(self, "x_coord_min", "Minimale X-Koordinate", deicmals=3)
        miny = QInputDialog.getDouble(self, "y_coord_min", "Minimale X-Koordinate", deicmals=3)
        maxx = QInputDialog.getDouble(self, "x_coord_max", "Minimale X-Koordinate", deicmals=3)
        maxy = QInputDialog.getDouble(self, "y_coord_max", "Minimale X-Koordinate", deicmals=3)
        extent = (minx, miny, maxx, maxy)

    def year(self):
        global prefix_a
        global prefix_b
        prefix_a = year_a.currentText()
        prefix_b = year_b.currentText()

app = QApplication([])
window = ChangeDetection()
app.exec()
