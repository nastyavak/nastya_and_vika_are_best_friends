import sys
import sqlite3
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QComboBox


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)  # Загружаем дизайн
        self.label.setText('')
        self.pushButton.setText('Ok')
        self.pushButton.clicked.connect(self.run)

        self.btn_open = QPushButton('2 форма', self)
        self.btn_open.clicked.connect(self.open2)


        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute("""SELECT название_сорта FROM кофе""").fetchall()
        self.sp = []
        for elem in result:
            self.sp.append(elem[0])
        self.comboBox.addItems(self.sp)
        con.close()

    def run(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result2 = cur.execute("""SELECT * FROM кофе
        WHERE название_сорта = ?""", (self.comboBox.currentText(),)).fetchall()
        self.text = ''

        for elem in result2:
            self.text += 'название: ' + str(elem[1])
            self.text += '\n'
            self.text += 'степень обжарки: ' + str(elem[2])
            self.text += '\n'
            self.text += 'вид помола: ' + str(elem[3])
            self.text += '\n'
            self.text += 'описание вкуса: ' + str(elem[4])
            self.text += '\n'
            self.text += 'цена: ' + str(elem[5])
            self.text += '\n'
            self.text += 'объём упаковки: ' + str(elem[6])
            self.text += '\n'
        con.close()
        self.label.setText(self.text)

    def open2(self):
        self.second_form = SecondForm(self, "")
        self.second_form.show()


class SecondForm(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)  # Загружаем дизайн

        self.comboBox = QComboBox(self)
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute("""SELECT название_сорта FROM кофе""").fetchall()
        self.sp = []
        for elem in result:
            self.sp.append(elem[0])
        self.comboBox.addItems(self.sp)
        con.close()
        self.comboBox.setGeometry(250, 40, 150, 50)

        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.change)

    def add(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute("""INSERT INTO кофе(название_сорта, степень_обжарки, молотый_в_зёрнах,
                 описание_вкуса, цена, объём_упаковки) VALUES(?, ?, ?, ?, ?, ?)""", (self.lineEdit.text(),
                                                                                     self.lineEdit_2.text(),
                                                                                     self.lineEdit_3.text(),
                                                                                     self.lineEdit_4.text(),
                                                                                     self.lineEdit_5.text(),
                                                                                     self.lineEdit_6.text(),))
        con.commit()
        con.close()

    def change(self):
        print('change')
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute("""update кофе 
                                set степень_обжарки = ?
                                WHERE название_сорта = ?""", (self.lineEdit_2.text(), self.comboBox.currentText(),))
        result = cur.execute("""update кофе 
                        set молотый_в_зёрнах = ?
                        WHERE название_сорта = ?""", (self.lineEdit_3.text(), self.comboBox.currentText(),))
        result = cur.execute("""update кофе 
                        set описание_вкуса = ?
                        WHERE название_сорта = ?""", (self.lineEdit_4.text(), self.comboBox.currentText(),))
        result = cur.execute("""update кофе 
                        set цена = ?
                        WHERE название_сорта = ?""", (self.lineEdit_5.text(), self.comboBox.currentText(),))
        result = cur.execute("""update кофе 
                        set объём_упаковки = ?
                        WHERE название_сорта = ?""", (self.lineEdit_6.text(), self.comboBox.currentText(),))
        result = cur.execute("""update кофе 
                set название_сорта = ?
                WHERE название_сорта = ?""", (self.lineEdit.text(), self.comboBox.currentText(),))
        con.commit()
        con.close()
        print('change2')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())