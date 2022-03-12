import sys
import pathlib
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QFileDialog
from config import Config
from core import EafFile


class Gui(QtWidgets.QMainWindow):
    MAIN_MENU = "data/qui/main_menu.ui"
    OPTION_MENU = "data/qui/options_menu.ui"

    def __init__(self):
        super(Gui, self).__init__()
        self.load_main_page()
        self.setFixedSize(self.size())
        self.setAcceptDrops(True)
        self.show()

    def dragEnterEvent(self, event) -> None:
        if event.mimeData().text().rstrip().endswith(".wav"):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        file_url = event.mimeData().text().rstrip().replace("file://", '')
        if file_url.endswith(".wav"):
            event.accept()
            self.process_file(file_url)
        else:
            event.ignore()

    def load_main_page(self):
        uic.loadUi(self.MAIN_MENU, self)
        self.findChild(QtWidgets.QPushButton, 'option_button').clicked.connect(self.option_button_clicked)
        self.findChild(QtWidgets.QGroupBox, 'main_group') \
            .findChild(QtWidgets.QPushButton, 'open_button').clicked.connect(self.open_file_button_clicked)

    def load_option_page(self):
        uic.loadUi(self.OPTION_MENU, self)
        buttons_group = self.findChild(QtWidgets.QGroupBox, 'button_group_box')
        buttons_group.findChild(QtWidgets.QPushButton, 'save_button').clicked.connect(self.save_button_clicked)
        buttons_group.findChild(QtWidgets.QPushButton, 'cancel_button').clicked.connect(self.cancel_button_clicked)
        self.findChild(QtWidgets.QGroupBox, 'options_box')\
            .findChild(QtWidgets.QPushButton, 'reset_button').clicked.connect(self.reset_option_button_clicked)
        config: Config = Config()
        option_box = self.findChild(QtWidgets.QGroupBox, 'options_box').findChild(QtWidgets.QWidget, 'inputs')

        for key, value in config.get_collector_options().items():
            option_box.findChild(QtWidgets.QSlider, key).setValue(value)

        annotator_config = config.get_annotator_options()
        option_box.findChild(QtWidgets.QPlainTextEdit, 'tierA').document().setPlainText(
            annotator_config['tiers_names'][0]
        )
        option_box.findChild(QtWidgets.QPlainTextEdit, 'tierB').document().setPlainText(
            annotator_config['tiers_names'][1]
        )
        option_box.findChild(QtWidgets.QPlainTextEdit, 'annotator').document().setPlainText(
            annotator_config['annotator_name']
        )

    def option_button_clicked(self):
        self.load_option_page()

    def cancel_button_clicked(self):
        self.load_main_page()

    def reset_option_button_clicked(self):
        Config().reset_config()
        self.load_main_page()

    def save_button_clicked(self):
        config: Config = Config()
        option_box = self.findChild(QtWidgets.QGroupBox, 'options_box').findChild(QtWidgets.QWidget, 'inputs')
        new_collector_options = {key: option_box.findChild(QtWidgets.QSlider, key).value()
                                 for key, value in config.get_collector_options().items()}
        config.set_collector_config(new_collector_options)

        not_validated = False
        for text_edit in option_box.findChildren(QtWidgets.QPlainTextEdit):
            if text_edit.document().toPlainText() == "":
                not_validated = True
                break
        if not_validated:
            QtWidgets.QMessageBox(icon=QtWidgets.QMessageBox.Icon.Critical,
                                  text="Jedna z opcji została zostawiona pusta",
                                  ).exec_()
        else:

            new_annotator_options = {
                "tiers_names": [
                    option_box.findChild(QtWidgets.QPlainTextEdit, 'tierA').document().toPlainText(),
                    option_box.findChild(QtWidgets.QPlainTextEdit, 'tierB').document().toPlainText()
                ],
                "annotator_name": option_box.findChild(QtWidgets.QPlainTextEdit, 'annotator').document().toPlainText()
            }
            config.set_annotator_config(new_annotator_options)
        config.save_config()
        self.load_main_page()

    def open_file_button_clicked(self):
        fileName = QFileDialog.getOpenFileName(self,
                                               directory=Config().get_file_option('input_path'),
                                               caption="Wybierz plik",
                                               filter='Pliki wav (*.wav)'
                                               )[0]
        if fileName != '':
            self.process_file(fileName)

    def process_file(self, wav_file):

        savePath = QFileDialog.getSaveFileName(self,
                                               directory=Config().get_file_option('output_path'),
                                               caption="Zapisz plik",
                                               filter='Pliki eaf (*.eaf)'
                                               )[0]
        if savePath != '':
            file = EafFile(wav_file, savePath)
            result = file.start_processing()

            new_file_options = {
                "input_path": str(pathlib.Path(wav_file).parent),
                "output_path": str(pathlib.Path(savePath).parent)
            }

            Config().set_file_config_options(new_file_options)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Gui()
    app.exec_()
