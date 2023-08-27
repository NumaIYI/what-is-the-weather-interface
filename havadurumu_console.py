import sys
from PyQt5 import QtWidgets
from hava_durumu_tasarı import Ui_MainWindow 
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon,QPixmap
from bs4 import BeautifulSoup
import requests

class myApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(myApp,self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.btn_ok.clicked.connect(self.havaNasil)
        self.ui.btn_clear.clicked.connect(self.sifirla)
        self.url1 = "https://www.ntv.com.tr/"
        self.url3 = "-hava-durumu"
        self.ui.btn_bildir.clicked.connect(self.showDialog)
        
    def havaNasil(self):
        sehir = self.ui.txt_sehir.text().lower()
        final = self.url1+sehir+self.url3
        r = requests.get(final)
        soup = BeautifulSoup(r.content,"html.parser")
        the5 = soup.find_all("div",{"class":"container hava-durumu--detail-data-item"},limit=5)
        gunler = ["Bugün","Yarın","Sonraki gün","3 gün sonra","4 gün sonra"]
        lbl_list = [self.ui.lbl_bugun,self.ui.lbl_yarin,self.ui.lbl_3,self.ui.lbl_4,self.ui.lbl_5]
        lcdClst= [self.ui.lcdC_1,self.ui.lcdC_2,self.ui.lcdC_3,self.ui.lcdC_4,self.ui.lcdC_5]
        lcdAzlst = [self.ui.lcdAz_1,self.ui.lcdAz_2,self.ui.lcdAz_3,self.ui.lcdAz_4,self.ui.lcdAz_5]
        self.ui.txt_lbl_gosterilensehir.setText("Gösterilen Şehir: "+self.ui.txt_sehir.text())
        sayac = 0
        for a in the5:
            gunadi = gunler[sayac] 
            maxsicak = a.find("p",{"class":"hava-durumu--detail-data-item-bottom-temp-max"}).text
            minsicak = a.find("p",{"class":"hava-durumu--detail-data-item-bottom-temp-min"}).text
            havadurumu = a.find("div",{"class":"container hava-durumu--detail-data-item-bottom-desc"}).text.strip()
            lbl_list[sayac].setText(f"{sayac+1}-- {gunadi} {havadurumu}")
            lcdClst[sayac].display(int(maxsicak))
            lcdAzlst[sayac].display(int(minsicak))
            sayac += 1

    def sifirla(self):
        lbl_list = [self.ui.lbl_bugun,self.ui.lbl_yarin,self.ui.lbl_3,self.ui.lbl_4,self.ui.lbl_5]
        lcdClst= [self.ui.lcdC_1,self.ui.lcdC_2,self.ui.lcdC_3,self.ui.lcdC_4,self.ui.lcdC_5]
        lcdAzlst = [self.ui.lcdAz_1,self.ui.lcdAz_2,self.ui.lcdAz_3,self.ui.lcdAz_4,self.ui.lcdAz_5]
        sayac = 0
        while sayac<5:
            lbl_list[sayac].setText(" ")
            lcdClst[sayac].display(0)
            lcdAzlst[sayac].display(0)
            sayac+=1
        self.ui.txt_lbl_gosterilensehir.setText("Gösterilen Şehir: ")
        self.ui.lbl_bildir_tesk.setText(" ")

    def showDialog(self):
       
        result = QMessageBox.warning(self,"Bildiri ekranı","Bildiri kaydedilecek emin misniz?",QMessageBox.Yes | QMessageBox.Cancel,QMessageBox.Cancel)
        if result == QMessageBox.Yes:
            self.ui.lbl_bildir_tesk.setText("En kısa sürede bu sorunu çözeceğiz.")
        else:
            pass
    


def app():
    app = QtWidgets.QApplication(sys.argv)
    win = myApp()
    win.show()
    sys.exit(app.exec_())

app()