# Weather Application

A comprehensive weather application with multiple interfaces including web, command-line, and desktop GUI.

## 🌟 Features

- **Multiple Interfaces**:
  - 🌐 Web interface (Flask)
  - 💻 Command-line interface
  - 🖥️ Desktop GUI (PyQt5)
- **Weather Data**:
  - Current weather conditions
  - Weather forecast
  - Location-based weather using geolocation
- **Voice Control** (experimental)
  - Voice commands for weather queries
  - Text-to-speech responses

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- OpenWeatherMap API key (get one from [OpenWeatherMap](https://openweathermap.org/api))

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ManX-Anon/Weather-Suite.git
   cd Weather-Suite
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your OpenWeatherMap API key.

## 🛠️ Usage

### Web Interface
```bash
python manage.py web
```
Then open `http://localhost:5000` in your browser.

### Command Line Interface
```bash
python manage.py cli
```

### Desktop Application
```bash
python manage.py desktop
```

## 🚀 Deployment

### Deployed on Render

## 📁 Project Structure

```
weather-app/
├── src/                    # Source code
│   ├── apps/              # Application modules
│   ├── utils/             # Utility functions
│   └── templates/         # Web templates
├── .env.example          # Example environment variables
├── .gitignore            # Git ignore file
├── manage.py             # Main entry point
├── Procfile              # For deployment
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ using Python, Flask, and PyQt5
- Weather data provided by [OpenWeatherMap](https://openweathermap.org/)
- Icons by [Font Awesome](https://fontawesome.com/)
