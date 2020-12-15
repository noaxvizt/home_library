from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import requests
import random
import sqlite3


START_IMAGE = 'books_background.jpg'
GENRES = {'Биографии и Мемуары': '67',
          'Деловая литература': '183',
          'Детективы и триллеры': '188',
          'Детская литература': '185',
          'Драматургия': '218',
          'Историческая литература': '45',
          'Классика': '180',
          'Книги о войне': '69',
          'Комиксы': '204',
          'Контркультура': '197',
          'Литературные формы': '239',
          'Личностный рост': '2',
          'Любовные романы': '187',
          'Магический реализм': '216',
          'Наука и образование': '186',
          'Поэзия': '193',
          'Приключения': '191',
          'Религия': '207',
          'Сверхъестественное': '119',
          'Современная литература': '182',
          'Ужасы': '68',
          'Фантастика': '189',
          'Фэнтези': '190',
          'Экранизация': '195',
          'Эротическая литература': '143',
          'Юмор и сатира': '85'}

GENRES_LIST = sorted(GENRES)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setFixedSize(500, 500)
        self.setObjectName('Библиотека')

        QToolTip.setFont(QFont('SansSerif', 10))
        self.startImage = QImage(START_IMAGE)
        sImage = self.startImage.scaled(QSize(500, 500))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        self.verticalLayoutWidget = QWidget(self)
        self.verticalLayoutWidget.setGeometry(QRect(150, 100, 200, 300))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.pushButton_recomendation = QPushButton(self.verticalLayoutWidget)
        self.pushButton_recomendation.setText('Если не знаете что почитать')
        self.pushButton_recomendation.setFixedSize(200, 70)
        self.pushButton_recomendation.setToolTip('Выберите случайную книгу')
        self.verticalLayout.addWidget(self.pushButton_recomendation)
        self.pushButton_recomendation.clicked.connect(self.recom_but_click)

        self.pushButton_add = QPushButton(self.verticalLayoutWidget)
        self.pushButton_add.setText('Добавить книгу')
        self.pushButton_add.setFixedSize(200, 70)
        self.pushButton_add.setToolTip('Добавьте книгу в свою библиотеку')
        self.verticalLayout.addWidget(self.pushButton_add)
        self.pushButton_add.clicked.connect(self.add_but_click)

        self.pushButton_view = QPushButton(self.verticalLayoutWidget)
        self.pushButton_view.setText('Обзор')
        self.pushButton_view.setFixedSize(200, 70)
        self.pushButton_view.setToolTip('Посмотрите свою библиотеку')
        self.verticalLayout.addWidget(self.pushButton_view)
        self.pushButton_view.clicked.connect(self.view_but_click)

        self.pushButton_help = QPushButton(self.verticalLayoutWidget)
        self.pushButton_help.setText('Помощь')
        self.pushButton_help.setFixedSize(200, 70)
        self.pushButton_help.setToolTip('Обратитесь за помощью')
        self.pushButton_help.clicked.connect(self.help_but_click)
        self.verticalLayout.addWidget(self.pushButton_help)

        self.setWindowIcon(QIcon('ico.jpg'))

    """def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Вы уверены, что хотите выйти?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    """

    def help_but_click(self):
        self.help_wid = HelpWidget()
        self.help_wid.show()
        self.close()

    def recom_but_click(self):
        self.recom_wid = ReccomWidget()
        self.recom_wid.show()
        self.close()

    def add_but_click(self):
        self.add_wid = AddWidget()
        self.add_wid.show()
        self.close()

    def view_but_click(self):
        self.view_wid = ViewWidget()
        self.view_wid.show()
        self.close()


class HelpWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setFixedSize(500, 500)
        self.setObjectName('Помощь')

        self.label = QLabel(self)
        self.label.move(50, 30)
        self.label.resize(400, 300)
        self.label.setFont(QFont("Times", 14))
        self.label.setText('\t    Помощь\n\n1)Первая кнопка позволяет вам выбрать \nслучайную книгу'
                           '\n2)Вторая кнопка позволяет добавить \nкнигу в вашу домашнюю библиотеку'
                           '\n3)Третья кнопка позволяет посмотреть \n книги из вашей библиотеки'
                           '\n4)Четвертая кнопка расскажет вам о \nфункционале программы.')
        self.push_button_retern = QPushButton(self)
        self.push_button_retern.resize(200, 50)
        self.push_button_retern.setText('Вернуться')
        self.push_button_retern.move(20, 400)
        self.push_button_retern.clicked.connect(self.retern_but_click)

        self.oImage = QImage("help_background.jpg")
        self.sImage = self.oImage.scaled(QSize(500, 500))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(self.sImage))
        self.setPalette(palette)

    def retern_but_click(self):
        self.main_wid = MainWindow()
        self.main_wid.show()
        self.close()


class ReccomWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.con = sqlite3.connect('my_books')
        self.cur = self.con.cursor()
        self.setFixedSize(700, 500)
        self.setObjectName('Случайная книга')

        self.label = QLabel(self)
        self.label.setFont(QFont("Times", 14))
        self.label.setText('   Выберите жанр и нажмите кнопку')
        self.label.move(30, 30)
        self.combo = QComboBox(self)
        self.combo.addItems(['Случайный жанр'] + list(GENRES_LIST))
        self.combo.move(50, 100)

        self.button = QPushButton(self)
        self.button.setText('Получить')
        self.button.move(280, 98)
        self.button.resize(100, 30)
        self.button.clicked.connect(self.get_rand_book)

        self.button_pic = QPushButton(self)
        self.button_pic.setText('Получить картинку')
        self.button_pic.move(200, 400)
        self.button_pic.resize(150, 30)
        self.button_pic.clicked.connect(self.givind_pic)

        self.label_status = QLabel(self)
        self.label_status.move(50, 200)
        self.label_status.resize(420, 50)
        self.label_status.setFont(QFont("Times", 14))

        self.button_return = QPushButton(self)
        self.button_return.setText('Вернуться')
        self.button_return.move(50, 400)
        self.button_return.resize(100, 30)
        self.button_return.clicked.connect(self.retern_but_click)

        self.process_label = QLabel(self)
        self.process_label.move(50, 350)
        self.process_label.resize(250, 30)

        self.import_but = QPushButton(self)
        self.import_but.setText('Загрузить в базу данных')
        self.import_but.move(50, 300)
        self.import_but.resize(200, 30)
        self.import_but.clicked.connect(self.adding_button)

        self.image = QLabel(self)
        self.image.move(500, 100)
        self.image.resize(160, 248)

        self.oImage = QImage("recom_background.jpg")
        self.sImage = self.oImage.scaled(QSize(700, 500))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(self.sImage))
        self.setPalette(palette)

    def parsing(self, gett):
        first, second = gett[227].strip(), gett[236].strip()
        first = first.split('"')
        second = second.split('/')
        name = first[5]
        if len(name) > 32:
            name = name[:32] + '...'
        image = first[3]
        author = second[3][2:-1]
        return (name, author, image)

    def adding_button(self):
        name, author, status = self.data[0], self.data[1], 'not_read'
        try:
            self.add_into_base([(name, author, status)])
            self.process_label.setText('Добавлено в базу данных')
        except Exception:
            self.process_label.setText('Произошла ошибка, уже разбираемся')

    def add_into_base(self, information):
        self.cur.execute(f"INSERT INTO books(title, author, status) VALUES " + str(information)[1:-1])
        self.con.commit()

    def get_rand_book(self):
        self.label_status.setText('Выполняется запрос')
        now_genre = self.combo.currentText()
        if now_genre == 'Случайный жанр':
            now_genre = random.choice(GENRES_LIST)
        now_url = f'http://readly.ru/books/i_am_lucky/?genre={GENRES[now_genre]}&show=1'
        getting = requests.get(now_url).text.split('\n')
        self.data = self.parsing(getting)
        self.label_status.setText('\n'.join(self.data[:-1]))
        getting_pic = requests.get('http://readly.ru' + self.data[-1])
        out = open("img.jpg", "wb")
        out.write(getting_pic.content)
        out.close()

    def givind_pic(self):
        self.pixmap = QPixmap('img.jpg')
        self.image.setPixmap(self.pixmap)

    def retern_but_click(self):
        self.main_wid = MainWindow()
        self.main_wid.show()
        self.close()


class AddWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.con = sqlite3.connect('my_books')
        self.cur = self.con.cursor()
        self.setFixedSize(500, 500)
        self.setObjectName('Добавление книг')

        self.label = QLabel(self)
        self.label.setFont(QFont("Times", 11))
        self.label.setText("Добавьте книгу")
        self.label.move(30, 30)

        self.name_label = QLabel(self)
        self.name_label.setText('Название книги')
        self.name_label.move(30, 70)

        self.name_in = QTextEdit(self)
        self.name_in.move(30, 100)
        self.name_in.resize(100, 30)
        self.name_in.setPlaceholderText('Название')

        self.author_label = QLabel(self)
        self.author_label.setText('Фамилия автора')
        self.author_label.move(150, 70)

        self.author_in = QTextEdit(self)
        self.author_in.move(150, 100)
        self.author_in.resize(100, 30)
        self.author_in.setPlaceholderText('Фамилия')

        self.status_label = QLabel(self)
        self.status_label.setText('Статус')
        self.status_label.move(270, 70)

        self.status_combo = QComboBox(self)
        self.status_combo.addItems(['not_read', 'in_process', 'read'])
        self.status_combo.move(270, 100)
        self.status_combo.resize(100, 30)

        self.add_button = QPushButton(self)
        self.add_button.resize(340, 30)
        self.add_button.move(30, 140)
        self.add_button.setText('Добавить книгу')
        self.add_button.clicked.connect(self.adding_button)

        self.process_label = QLabel(self)
        self.process_label.move(30, 320)
        self.process_label.setText('Ожидание команды')
        self.process_label.resize(200, 30)

        self.export_label = QLabel(self)
        self.export_label.move(30, 200)
        self.export_label.setFont(QFont("Times", 11))
        self.export_label.setText('Импортируйте таблицу в базу данных')

        self.export_button = QPushButton(self)
        self.export_button.move(30, 250)
        self.export_button.resize(150, 50)
        self.export_button.setText('Импорт')
        self.export_button.clicked.connect(self.importing)

        self.button_return = QPushButton(self)
        self.button_return.setText('Вернуться')
        self.button_return.move(30, 400)
        self.button_return.resize(100, 30)
        self.button_return.clicked.connect(self.retern_but_click)

    def adding_button(self):
        name, author, status = self.name_in.toPlainText(), self.author_in.toPlainText(), self.status_combo.currentText()
        try:
            self.add_into_base([(name, author, status)])
            self.process_label.setText('Добавлено в базу данных')
        except Exception:
            self.process_label.setText('Произошла ошибка, уже разбираемся')

    def add_into_base(self, information):
        self.cur.execute(f"INSERT INTO books(title, author, status) VALUES " + str(information)[1:-1])
        self.con.commit()

    def importing(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '', 'Файл (*.csv);;Все файлы (*)')[0]
        delimetr = QInputDialog.getItem(self, "Разделитель", "Выберите разделитель в csv-файле", (";", ".", ":"))[0]
        with open(fname, encoding='utf-8') as reader:
            data = list(map(str.strip, reader.readlines()))
            data = list(map(lambda x: tuple(x.split(delimetr)), data))
        try:
            self.add_into_base(data)
            self.process_label.setText('Добавлено в базу данных')
        except Exception:
            self.process_label.setText('Произошла ошибка, уже разбираемся')

    def retern_but_click(self):
        self.con.close()
        self.main_wid = MainWindow()
        self.main_wid.show()
        self.close()


class ViewWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(700, 500)
        self.setObjectName('Обзор библиотеки')

        self.con = sqlite3.connect('my_books')
        self.cur = self.con.cursor()
        self.data = self.cur.execute("""SELECT * from books""").fetchall()

        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setRowCount(len(self.data))
        self.table.setHorizontalHeaderLabels(['id', 'title', 'author', 'status'])
        self.table.resize(490, 300)
        self.table.move(10, 10)
        #self.table.setSortingEnabled(True)

        self.update_table()

        self.button_return = QPushButton(self)
        self.button_return.setText('Вернуться')
        self.button_return.move(30, 450)
        self.button_return.resize(100, 30)
        self.button_return.clicked.connect(self.retern_but_click)

        self.filter_label = QLabel(self)
        self.filter_label.setText('Фильтры по статусу')
        self.filter_label.move(530, 10)

        self.status_read = QCheckBox(self)
        self.status_read.move(510, 40)
        self.status_read.setText('read')

        self.status_in_process = QCheckBox(self)
        self.status_in_process.move(510, 70)
        self.status_in_process.setText('in_process')

        self.status_not_read = QCheckBox(self)
        self.status_not_read.move(510, 100)
        self.status_not_read.setText('not_read')

        self.update_but = QPushButton(self)
        self.update_but.setText('Обновить')
        self.update_but.move(510, 130)
        self.update_but.resize(100, 30)
        self.update_but.clicked.connect(self.filtration)

        self.delete_label = QLabel(self)
        self.delete_label.setText('Выделите ячейку и \nнажмите кнопку удалить')
        self.delete_label.move(510, 170)

        self.delete_but = QPushButton(self)
        self.delete_but.setText('Удалить элемент')
        self.delete_but.move(510, 210)
        self.delete_but.resize(150, 30)
        self.delete_but.clicked.connect(self.deletion)

        self.export_label = QLabel(self)
        self.export_label.setText('Выгрузить базу данных в файл')
        self.export_label.move(10, 320)

        self.export_line = QTextEdit(self)
        self.export_line.move(10, 350)
        self.export_line.resize(200, 30)
        self.export_line.setPlaceholderText('Имя файла')

        self.export_combo = QComboBox(self)
        self.export_combo.addItems(['csv', 'tsv', 'txt'])
        self.export_combo.move(220, 350)
        self.export_combo.resize(50, 30)

        self.export_but = QPushButton(self)
        self.export_but.setText('Выгрузить')
        self.export_but.move(280, 350)
        self.export_but.resize(100, 30)
        self.export_but.clicked.connect(self.exporting)

        self.export_label_sumbol = QLabel(self)
        self.export_label_sumbol.setText('')
        self.export_label_sumbol.move(10, 390)
        self.export_label_sumbol.resize(300, 30)

    def update_table(self):
        self.table.clear()
        self.table.setRowCount(len(self.data))
        for i in range(len(self.data)):
            for j in range(4):
                self.table.setItem(i, j, QTableWidgetItem(str(self.data[i][j])))

    def retern_but_click(self):
        self.con.close()
        self.main_wid = MainWindow()
        self.main_wid.show()
        self.close()

    def deletion(self):
        new_data = set()
        rows = set()
        for index in self.table.selectedIndexes():
            now = self.data[index.row()][0]
            new_data.add(index.row())
            rows.add(now)
        for index in rows:
            self.cur.execute(f"""DELETE from books WHERE id = {str(index)}""")
        counter = 0
        for i in new_data:
            del self.data[i - counter]
            counter += 1
        self.con.commit()
        self.update_table()

    def filtration(self):
        selected = []
        if self.status_read.isChecked():
            selected.append(self.status_read.text())
        if self.status_in_process.isChecked():
            selected.append(self.status_in_process.text())
        if self.status_not_read.isChecked():
            selected.append(self.status_not_read.text())
        if len(selected) == 0:
            self.data = self.cur.execute("""SELECT * from books""").fetchall()
        else:
            self.data = self.cur.execute(f"""SELECT * from books
                                        WHERE status in {'(' + str(selected)[1:-1] + ')'}""").fetchall()
        self.update_table()

    def exporting(self):
        if self.export_combo.currentText() == 'txt':
            delimetr = ','
        elif self.export_combo.currentText() == 'csv':
            delimetr = ';'
        else:
            delimetr = '\t'
        data = self.cur.execute("""SELECT * from books""").fetchall()
        data = list(map(lambda x: list(map(str, x)), data))
        data = '\n'.join(list(map(lambda x: delimetr.join(x), data)))
        with open(self.export_line.toPlainText() + '.' + self.export_combo.currentText(), 'w', encoding='utf-8') as writer:
            writer.write(data)
            self.export_label_sumbol.setText(f"Файл {self.export_line.toPlainText() + '.' + self.export_combo.currentText()} выгружен")

