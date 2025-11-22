"""Tkinter GUI weather app (Prompt 3)."""
from __future__ import annotations

import threading
import tkinter as tk
from tkinter import messagebox, ttk

from src.utils import WeatherAPI, WeatherError

ICON_MAP = {
    "01": "☀️",
    "02": "🌤️",
    "03": "☁️",
    "04": "☁️",
    "09": "🌧️",
    "10": "🌦️",
    "11": "⛈️",
    "13": "❄️",
    "50": "🌫️",
}


class WeatherApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Tkinter Weather App")
        self.geometry("420x320")
        self.configure(padx=20, pady=20)

        self.api = WeatherAPI()
        self.city_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Enter a city and press Search")

        self._build_layout()

    # ------------------------------------------------------------------
    def _build_layout(self) -> None:
        input_frame = ttk.Frame(self)
        input_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(input_frame, text="City:").pack(side="left")
        city_entry = ttk.Entry(input_frame, textvariable=self.city_var)
        city_entry.pack(side="left", fill="x", expand=True, padx=(8, 8))
        city_entry.bind("<Return>", lambda _: self.fetch_weather())

        ttk.Button(input_frame, text="Search", command=self.fetch_weather).pack(side="right")

        self.progress = ttk.Progressbar(self, mode="indeterminate")

        self.card = ttk.LabelFrame(self, text="Weather Details", padding=15)
        self.card.pack(fill="both", expand=True)

        self.icon_label = ttk.Label(self.card, text="", font=("Segoe UI", 28))
        self.icon_label.pack(pady=(0, 10))

        self.info_labels = {
            "temperature": ttk.Label(self.card, text="Temperature: --"),
            "humidity": ttk.Label(self.card, text="Humidity: --"),
            "wind": ttk.Label(self.card, text="Wind Speed: --"),
            "description": ttk.Label(self.card, text="Description: --"),
        }
        for label in self.info_labels.values():
            label.pack(anchor="w", pady=2)

        self.status_label = ttk.Label(self, textvariable=self.status_var)
        self.status_label.pack(pady=(10, 0))

    # ------------------------------------------------------------------
    def fetch_weather(self) -> None:
        city = self.city_var.get().strip()
        if not city:
            messagebox.showwarning("Input Required", "Please enter a city name.")
            return

        self.status_var.set("Fetching weather...")
        self.progress.pack(fill="x", pady=(0, 10))
        self.progress.start()

        threading.Thread(target=self._fetch_async, args=(city,), daemon=True).start()

    def _fetch_async(self, city: str) -> None:
        try:
            data = self.api.get_current_weather(city)
        except WeatherError as exc:
            self.after(0, lambda: self._handle_error(str(exc)))
            return
        self.after(0, lambda: self._update_view(data))

    def _handle_error(self, message: str) -> None:
        self.progress.stop()
        self.progress.pack_forget()
        self.status_var.set("Error: " + message)
        messagebox.showerror("Weather Error", message)

    def _update_view(self, data) -> None:
        self.progress.stop()
        self.progress.pack_forget()

        icon_key = data.icon[:2]
        self.icon_label.config(text=ICON_MAP.get(icon_key, "🌍"))
        self.info_labels["temperature"].config(text=f"Temperature: {data.temperature:.1f} °C")
        self.info_labels["humidity"].config(text=f"Humidity: {data.humidity}%")
        self.info_labels["wind"].config(text=f"Wind Speed: {data.wind_speed:.1f} m/s")
        self.info_labels["description"].config(text=f"Description: {data.description.title()}")
        self.status_var.set(f"Weather updated for {data.city}")


def run() -> None:
    app = WeatherApp()
    app.mainloop()


if __name__ == "__main__":
    run()
