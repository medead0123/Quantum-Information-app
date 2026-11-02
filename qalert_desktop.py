# qalert_desktop.py - PyQt6 polished version

import sys, math, numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QSlider, QSpinBox, QStackedWidget,
    QFileDialog, QListWidget, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QMovie, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# ---------- Helpers ----------
def simulate_grover(n_qubits, max_iterations=10):
    N = 2 ** n_qubits
    theta = math.asin(1 / math.sqrt(N))
    iters = list(range(max_iterations + 1))
    probs = [math.sin((2*r + 1) * theta) ** 2 for r in iters]
    return iters, probs

class MplCanvas(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        self.fig.patch.set_facecolor("#fdfdfd")
        super().__init__(self.fig)
    def save_figure(self):
        path, _ = QFileDialog.getSaveFileName(None, "Save Graph", "", "PNG Files (*.png)")
        if path:
            self.fig.savefig(path)

# ---------- Pages ----------
class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        title = QLabel("🌐 Q-ALERT")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        desc = QLabel(
            "Quantum computing poses new risks to classical encryption.\n\n"
            "Q-ALERT is an interactive learning app to understand quantum threats "
            "and the need for Post-Quantum Cryptography."
        )
        desc.setFont(QFont("Segoe UI", 12))
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addStretch()
        self.setLayout(layout)

class QuantumBasicsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("🔹 Quantum Basics")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        text = QLabel(
            "A classical bit can be 0 or 1.\n"
            "A quantum bit (qubit) can exist in a superposition of states.\n"
            "Entanglement links qubits across distance."
        )
        text.setWordWrap(True)
        text.setFont(QFont("Segoe UI", 11))
        layout.addWidget(text)

        # GIF placeholder
        gif_label = QLabel()
        movie = QMovie("assets/qubit.gif")  # <-- put your GIF here
        gif_label.setMovie(movie)
        movie.start()
        gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(gif_label)

        self.setLayout(layout)

class ClassicalVsQuantumPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("🔹 Classical vs Quantum Computing")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        text = QLabel(
            "Classical computers process bits sequentially.\n"
            "Quantum computers leverage superposition and interference to process many states at once."
        )
        text.setWordWrap(True)
        text.setFont(QFont("Segoe UI", 11))
        layout.addWidget(text)

        # GIF placeholder
        gif_label = QLabel()
        movie = QMovie("assets/quantum_compare.gif")  # <-- add GIF
        gif_label.setMovie(movie)
        movie.start()
        gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(gif_label)

        self.setLayout(layout)

class GroverPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Sliders
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel("Qubits:"))
        self.slider_qubits = QSlider(Qt.Orientation.Horizontal)
        self.slider_qubits.setRange(2,12)
        self.slider_qubits.setValue(6)
        self.slider_qubits.valueChanged.connect(self.update_chart)
        slider_layout.addWidget(self.slider_qubits)

        slider_layout.addWidget(QLabel("Iterations:"))
        self.slider_iters = QSlider(Qt.Orientation.Horizontal)
        self.slider_iters.setRange(1,30)
        self.slider_iters.setValue(10)
        self.slider_iters.valueChanged.connect(self.update_chart)
        slider_layout.addWidget(self.slider_iters)

        layout.addLayout(slider_layout)

        # Chart
        self.canvas = MplCanvas()
        layout.addWidget(self.canvas)

        save_btn = QPushButton("💾 Save Graph")
        save_btn.setStyleSheet("background-color:#a3d2ca; border-radius:5px; padding:5px;")
        save_btn.clicked.connect(self.canvas.save_figure)
        layout.addWidget(save_btn, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)
        self.update_chart()

    def update_chart(self):
        n_qubits = self.slider_qubits.value()
        iters = self.slider_iters.value()
        xs, probs = simulate_grover(n_qubits, iters)
        self.canvas.ax.clear()
        self.canvas.ax.plot(xs, probs, marker="o", color="#e5989b")
        self.canvas.ax.set_ylim(0,1)
        self.canvas.ax.set_title(f"Grover Success Probability (n={n_qubits})")
        self.canvas.ax.set_xlabel("Iterations")
        self.canvas.ax.set_ylabel("Success Probability")
        self.canvas.draw()

# ---------- Main Window ----------
class QAlertApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Q-ALERT Interactive Desktop App")
        self.setGeometry(200,200,1000,700)

        self.stack = QStackedWidget()
        self.pages = {
            "Home": HomePage(),
            "Quantum Basics": QuantumBasicsPage(),
            "Classical vs Quantum": ClassicalVsQuantumPage(),
            "Grover Simulation": GroverPage()
        }
        for p in self.pages.values():
            self.stack.addWidget(p)

        sidebar = QVBoxLayout()
        sidebar.setSpacing(5)
        for name in self.pages.keys():
            btn = QPushButton(name)
            btn.setStyleSheet(
                "background-color:#fce8d5; border:none; padding:8px; border-radius:5px;"
            )
            btn.clicked.connect(lambda _, n=name: self.switch_page(n))
            sidebar.addWidget(btn)

        container = QWidget()
        main_layout = QHBoxLayout(container)
        side_widget = QWidget()
        side_widget.setLayout(sidebar)
        side_widget.setFixedWidth(200)
        side_widget.setStyleSheet("background-color:#fdf3e7;")
        main_layout.addWidget(side_widget)
        main_layout.addWidget(self.stack)

        self.setCentralWidget(container)
        self.switch_page("Home")

    def switch_page(self, name):
        self.stack.setCurrentWidget(self.pages[name])

# ---------- Run ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QAlertApp()
    window.show()
    sys.exit(app.exec())
