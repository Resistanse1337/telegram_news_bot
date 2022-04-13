import os
import sys
import configparser
from PyQt5.Qt import *
from PyQt5 import QtWidgets
from functools import partial

from parser import *
from telegram import *


class ApplicationWindow(QWidget):
    """
    Главное окно приложения

    """
    def __init__(self):
        super().__init__()

        self.config_path = 'settings.cfg'
        self.config = configparser.ConfigParser()

        if not os.path.isfile(self.config_path):
            self.create_standard_config()

        self.config.read(self.config_path)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.setLayout(self.grid)

        self.setWindowTitle('News sender')
        self.setFixedSize(300, 200)

        self.input_label = QLabel("Введите id телеграм канала:")
        self.grid.addWidget(self.input_label, self.grid.rowCount()+1, 0)

        self.telegram_channel_edit = QLineEdit()
        self.telegram_channel_edit.setText(self.config.get("APP", "telegram_channel_id"))
        self.telegram_channel_edit.textChanged.connect(partial(self.save_line_edit, self.telegram_channel_edit,
                                                               "telegram_channel_id"))
        self.grid.addWidget(self.telegram_channel_edit, self.grid.rowCount(), 0)

        self.api_id_label = QLabel("Введите токен бота:")
        self.grid.addWidget(self.api_id_label, self.grid.rowCount(), 0)

        self.bot_token_edit = QLineEdit()
        self.bot_token_edit.setText(self.config.get("APP", "bot_token"))
        self.bot_token_edit.textChanged.connect(partial(self.save_line_edit, self.bot_token_edit, "bot_token"))
        self.grid.addWidget(self.bot_token_edit, self.grid.rowCount(), 0)

        self.send_button = QPushButton("Отправить последнюю новость")
        self.send_button.clicked.connect(self.send_news)
        self.grid.addWidget(self.send_button, self.grid.rowCount(), 0)

        self.show()

    def save_line_edit(self, obj, subsection):
        """Сохраняет настройку в конфиге"""
        self.config.set("APP", subsection, obj.text())
        self.save_config()

    def send_news(self):
        """Срабатывает по нажатию на 'Отправить новость'"""
        url, title, description = get_last_news()
        message = "\n".join([url, title.strip(), description.strip()])

        successful = send_message_to_channel(self.config.get("APP", "bot_token"), self.config.get("APP", "telegram_channel_id"),
                                message)
        if not successful:
            QMessageBox.about(self, "Информация", "Произошла ошибка, проверьте правильность ввода данных")
        else:
            QMessageBox.about(self, "Информация", "Новость успешно отправлена")

    def save_config(self):
        """Сохраняет изменения в конфиге"""
        with open(self.config_path, 'w') as config_file:
            self.config.write(config_file)

    def create_standard_config(self):
        """Создает стандартный конфиг"""
        self.config.add_section("APP")
        self.config.set("APP", "bot_token", "")
        self.config.set("APP", "telegram_channel_id", "")

        self.save_config()


def main():
    """Запускает приложение"""
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()



