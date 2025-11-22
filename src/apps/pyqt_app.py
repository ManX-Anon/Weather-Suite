"""PyQt5 weather application with dark theme (Prompt 4)."""
from __future__ import annotations

from PyQt5 import QtCore, QtGui, QtWidgets

from src.utils import WeatherAPI, WeatherError

ICON_MAP = {
    "01": "☀",
    "02": "🌤",
    "03": "☁",
    "04": "☁",
    "09": "🌧",
    "10": "🌦",
    "11": "⛈",
    "13": "❄",
    "50": "🌫",
}


class WeatherFetcher(QtCore.QObject):
    """Logic class that interacts with the WeatherAPI."""

    weather_ready = QtCore.pyqtSignal(object)
    error = QtCore.pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.api = WeatherAPI()

    @QtCore.pyqtSlot(str)
    def fetch(self, city: str) -> None:
        try:
            data = self.api.get_current_weather(city)
        except WeatherError as exc:
            self.error.emit(str(exc))
            return
        self.weather_ready.emit(data)


class WeatherWindow(QtWidgets.QMainWindow):
    """Main UI window with dark themed, card-style layout."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PyQt5 Weather App")
        self.resize(460, 320)

        self._setup_palette()
        self._init_widgets()
        self._init_worker()

    def _setup_palette(self) -> None:
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(30, 30, 30))
        palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(45, 45, 48))
        palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(37, 37, 38))
        palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(63, 63, 70))
        palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
        self.setPalette(palette)

    def _init_widgets(self) -> None:
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)

        layout = QtWidgets.QVBoxLayout(central)

        search_layout = QtWidgets.QHBoxLayout()
        self.input_field = QtWidgets.QLineEdit()
        self.input_field.setPlaceholderText("Enter city name")
        self.search_button = QtWidgets.QPushButton("Search")
        self.status_label = QtWidgets.QLabel("Ready")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)

        search_layout.addWidget(self.input_field)
        search_layout.addWidget(self.search_button)

        self.card = QtWidgets.QFrame()
        self.card.setObjectName("card")
        self.card.setStyleSheet(
            "#card { background-color: #3b3b40; border-radius: 12px; padding: 20px; }"
        )
        card_layout = QtWidgets.QVBoxLayout(self.card)
        self.icon_label = QtWidgets.QLabel("☀")
        self.icon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.icon_label.setStyleSheet("font-size: 48px;")

        self.temperature_label = QtWidgets.QLabel("-- °C")
        self.temperature_label.setAlignment(QtCore.Qt.AlignCenter)
        self.temperature_label.setStyleSheet("font-size: 42px; font-weight: bold;")

        self.description_label = QtWidgets.QLabel("Description")
        self.description_label.setAlignment(QtCore.Qt.AlignCenter)

        self.details_label = QtWidgets.QLabel("Humidity: -- | Pressure: -- | Wind: --")
        self.details_label.setAlignment(QtCore.Qt.AlignCenter)

        card_layout.addWidget(self.icon_label)
        card_layout.addWidget(self.temperature_label)
        card_layout.addWidget(self.description_label)
        card_layout.addWidget(self.details_label)

        layout.addLayout(search_layout)
        layout.addWidget(self.card)
        layout.addWidget(self.status_label)

        self.search_button.clicked.connect(self._handle_search)
        self.input_field.returnPressed.connect(self._handle_search)

    def _init_worker(self) -> None:
        self.worker = WeatherFetcher()
        self.thread = QtCore.QThread()
        self.worker.moveToThread(self.thread)
        self.worker.weather_ready.connect(self._update_weather)
        self.worker.error.connect(self._show_error)
        self.thread.start()

    # ------------------------------------------------------------------
    def _handle_search(self) -> None:
        city = self.input_field.text().strip()
        if not city:
            self.status_label.setText("Enter a city name.")
            return
        self.status_label.setText("Fetching weather...")
        QtCore.QMetaObject.invokeMethod(
            self.worker,
            "fetch",
            QtCore.Qt.QueuedConnection,
            QtCore.Q_ARG(str, city),
        )

    @QtCore.pyqtSlot(object)
    def _update_weather(self, data) -> None:
        icon_key = data.icon[:2]
        self.icon_label.setText(ICON_MAP.get(icon_key, "🌍"))
        self.temperature_label.setText(f"{data.temperature:.1f}°C")
        self.description_label.setText(data.description.title())
        self.details_label.setText(
            f"Feels Like: {data.feels_like:.1f}°C | Humidity: {data.humidity}% | Wind: {data.wind_speed:.1f} m/s"
        )
        self.status_label.setText(f"Updated: {data.city}")

    @QtCore.pyqtSlot(str)
    def _show_error(self, message: str) -> None:
        QtWidgets.QMessageBox.critical(self, "Weather Error", message)
        self.status_label.setText("Error: " + message)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:  # noqa: N802
        self.thread.quit()
        self.thread.wait()
        super().closeEvent(event)


def run() -> None:
    app = QtWidgets.QApplication([])
    window = WeatherWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    run()
