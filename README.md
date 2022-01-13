# LiDAR-Chance-Detection
Immer wie mehr Daten aus Airborne LiDAR-Messungen aus mehreren Zeitabständen stehen online zur Verfügung, so Beispielsweise vom ganzen Kanton Solothurn. Im Rahmen der beiden Blockwochen sollen diese Daten auf die Brauchbarkeit und Genauigkeit überprüft werden. Zusätzlich soll die Erstellung einer Rasteranalyse automatisiert und somit vereinfacht werden. Das Programm, welches in diesem Rahmen geschrieben wurde, erstellt nach dem  Einlesen der Daten des Users  zuerst einzelne GeoTIFF's, die einzelnen Files mit den Punktwolken werden also zuerst gerastert und einzeln abgespeichert. Anschliessend werden diese GeoTIFF's zu einem Grossen zusammengefügt. Die zuvor erstellten einzelnen Files werden wieder gelöscht. Somit ist das Resultat des Programms ein TIFF über das gesamte eingelesene Gebiet.

Die Daten von den Airborne LiDAR-Messungen aus den Jahren 2014 und 2019 eines Teilgebietes des Kanton Solothurns wurden für die Bearbeitung der Aufgabe bereitgestellt. Zusätzlich wurden noch theoretische Hilfestellungen zu den Themen Airborne Laserscanning und Python zur Verfügung gestellt. Die Bearbeitung der Daten soll mit Python gemacht werden.

Konzept & Gedanken zu den Aufgaben:
https://miro.com/app/board/uXjVOYfTuDk=/
