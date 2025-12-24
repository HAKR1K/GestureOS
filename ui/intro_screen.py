from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer

class IntroScreen(QWidget):
    def __init__(self, switch_callback):
        super().__init__()

        self.setStyleSheet("""
        background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
        stop:0 #141e30, stop:1 #243b55);
        color: white;
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Welcome to GestureOS")
        title.setStyleSheet("font-size:32px;font-weight:bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("AI-Powered Touchless Control")
        subtitle.setStyleSheet("font-size:20px;margin-bottom:30px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.dots = QLabel("•")
        self.dots.setStyleSheet("font-size:26px;color:#00b4db;")
        self.dots.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.state = 0
        self.timer.start(500)

        enter_btn = QPushButton("🚀 Enter Gesture OS")
        enter_btn.setFixedWidth(220)
        enter_btn.clicked.connect(switch_callback)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.dots)
        layout.addWidget(enter_btn)

        self.setLayout(layout)

    def animate(self):
        self.state = (self.state + 1) % 3
        self.dots.setText("•" * (self.state + 1))
