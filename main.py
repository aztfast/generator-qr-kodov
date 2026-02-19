import sys
import qrcode
from io import BytesIO
from PyQt6.QtWidgets import (QApplication, QLineEdit, QPushButton, QWidget, QLayout, QLabel, QVBoxLayout,
                             QHBoxLayout, QFileDialog)
from PyQt6.QtGui import QPixmap, QIcon, QImage
from PyQt6.QtCore import Qt


class Generator(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('QR Code Generator')
        self.lay1 = QHBoxLayout()
        self.Url_line = QLineEdit(self)
        self.lay = QVBoxLayout()
        self.qr_label = QLabel(self)
        self.lay.addWidget(self.qr_label)
        self.lay1.addWidget(self.Url_line)
        self.start_button = QPushButton(self)
        self.start_button.setText("Start")
        self.save_button = QPushButton(self)
        self.save_button.setText("Save")
        self.lay.addWidget(self.save_button)
        self.lay1.addWidget(self.start_button)
        self.QRcode = QPixmap()
        self.lay.addLayout(self.lay1)
        self.setLayout(self.lay)
        self.save_button.clicked.connect(self.save)
        self.start_button.clicked.connect(self.generate)

    def generate(self):
        text = self.Url_line.text().strip()
        if not text:
            return

        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=1,
            )
            qr.add_data(text)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            pixmap = QPixmap()
            pixmap.loadFromData(buffer.getvalue())
            self.qr_label.setPixmap(pixmap.scaled(
                self.width() - 75, self.height() - 75,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))

        except Exception as e:
            print(f"Не удалось сгенерировать QR-код:\n{str(e)}")

    def save(self):
        try:
            fname = QFileDialog.getSaveFileName(
                self, 'сохранить', '',
                'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]
            if not fname:
                return
            self.qr_label.pixmap().save(fname)
        except Exception as e:
            print(str(e))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    generator = Generator()
    generator.show()
    app.exec()

