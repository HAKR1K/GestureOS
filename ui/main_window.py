from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QCheckBox, QGroupBox, QStackedLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from core.action_thread import ActionThread
from core.gesture_thread import GestureThread
from ui.intro_screen import IntroScreen
from ui.styles import MAIN_STYLE


class GestureOSGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GestureOS – AI Touchless Control")
        self.resize(740, 840)

        self.stack = QStackedLayout()
        self.intro = IntroScreen(self.show_main_ui)
        self.main_ui = QWidget()

        self.stack.addWidget(self.intro)
        self.stack.addWidget(self.main_ui)
        self.setLayout(self.stack)

        self.thread = None
        self.action_thread = None  # 🔥 added

        self.build_main_ui()

    def show_main_ui(self):
        self.stack.setCurrentWidget(self.main_ui)

    def build_main_ui(self):
        self.main_ui.setStyleSheet(MAIN_STYLE)

        self.status = QLabel("Status: Waiting")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.video = QLabel()
        self.video.setMinimumSize(640, 480)
        self.video.setStyleSheet("border:3px solid #00b4db;border-radius:20px;")

        self.start_btn = QPushButton("🚀 Start Gesture Control")
        self.stop_btn = QPushButton("⛔ Stop Gesture Control")
        self.stop_btn.setEnabled(False)

        self.checkboxes = [
            QCheckBox("🖐️ Copy"),
            QCheckBox("📋 Paste"),
            QCheckBox("⬆️ Scroll Up"),
            QCheckBox("⬇️ Scroll Down"),
        ]
        for cb in self.checkboxes:
            cb.setChecked(True)

        group = QGroupBox("🧠 Gesture Feature Control Panel")
        vbox = QVBoxLayout()
        for cb in self.checkboxes:
            vbox.addWidget(cb)
        group.setLayout(vbox)
        group.setMaximumWidth(250)

        top = QHBoxLayout()
        top.addWidget(self.video)
        top.addWidget(group)

        layout = QVBoxLayout()
        layout.addWidget(self.status)
        layout.addLayout(top)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)

        self.main_ui.setLayout(layout)

        self.start_btn.clicked.connect(self.start)
        self.stop_btn.clicked.connect(self.stop)

    # ==================================================
    # 🔥 ONLY REAL LOGIC CHANGE IS HERE
    # ==================================================

    def start(self):
        # Gesture detection thread (camera + mediapipe)
        self.thread = GestureThread({})

        # Action execution thread (OS actions)
        self.action_thread = ActionThread()

        self.thread.frame_signal.connect(
            lambda img: self.video.setPixmap(QPixmap.fromImage(img))
        )
        self.thread.status_signal.connect(
            lambda text: self.status.setText(f"Status: {text}")
        )

        # 🔥 CONNECT GESTURE → ACTION
        self.thread.gesture_detected.connect(
            self.action_thread.set_gesture
        )

        self.thread.start()
        self.action_thread.start()

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def stop(self):
        
        if self.thread:
            self.thread.stop()
            self.thread.quit()
            self.thread.wait()
            self.thread = None

        if self.action_thread:
            # 🔥 Force reset gesture before stopping
            self.action_thread.set_gesture("NONE")
            self.action_thread.stop()
            self.action_thread.quit()
            self.action_thread.wait()
            self.action_thread = None

        self.status.setText("Status: Stopped")
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

