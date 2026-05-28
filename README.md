# 🚗 CNH Simulated 

A modern desktop application built with Python and PySide6 to help users prepare for the Brazilian Driver's License (CNH) theoretical exam. It provides a local offline database of questions and the ability to dynamically generate new, unique questions using the Google Gemini API.

## 📸 Screenshots

<!-- You can host images on Imgur or use raw GitHub URLs. Replace the placeholder links below with your real online image links. -->

### App Mockup
![App Mockup](https://i.pinimg.com/originals/8e/ba/eb/8ebaeb84f426e439f01c719adf9984e0.png)

### Running Application
![Dashboard Screenshot](https://i.pinimg.com/originals/64/2b/8d/642b8d4659ff22373a0989e7d9ffe54c.png)
![AI Generation Screenshot](https://i.pinimg.com/originals/7d/d8/15/7dd815b463d2d16184ebc09773217901.png)

## ✨ How it Works

The application works in two main modes:
- **Local Simulation:** Users can test their knowledge using a static, built-in offline JSON database of carefully curated CNH questions.
- **AI-Assisted Simulation:** By configuring a Google Gemini API Key in the settings, the app connects to Gemini models (like `gemini-flash-lite-latest`) to generate brand new questions on the fly. These questions can also be saved to the local database for future offline use.

## 📂 Project Structure

```text
CNH-Simulated/
├── core/               # Core functionalities (config loader, database parsing, styles)
├── json/               # Local JSON question bank (perguntas.json)
├── logic/              # Business logic and background threads (Gemini API worker)
├── ui/                 # UI components (pages, custom widgets, animations)
├── build.sh            # build program for linux (Ubuntu/Debian)
├── main.py             # Main entry point for the PySide6 application
├── pyproject.toml      # Project metadata and dependencies
└── README.md           # Project documentation
```

## 🚀 How to Run

This project uses uv as its fast Python package manager and resolver.

### Prerequisites
- Python >= 3.12
- uv installed on your system.

### Setup and Execution

1. **Clone the repository:**
   ```bash
   git clone https://github.com/guilherme23x/CNH-Simulated.git
   cd cnh-simulated
   ```

2. **Install dependencies and run the application:**
   ```bash
   uv run main.py
   ```
   *(Note: `uv run` will automatically resolve dependencies specified in `pyproject.toml`, create an isolated environment if needed, and run the entry script).*

## ⚙️ Configuration
To use the AI generation features, you will need a Google Gemini API Key.
1. Obtain a key from Google AI Studio.
2. Open the application.
3. Navigate to **Configurações** (Settings) in the sidebar.
4. Enter your API Key, select your preferred model, and hit save!
