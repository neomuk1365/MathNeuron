# Math Intuition Platform 🧠

A premium, interactive educational platform designed to teach Mathematics for Data Science, Machine Learning, AI, and Statistics. 

Unlike traditional tutorial websites, this platform focuses entirely on **intuition-building over formula memorization**. It rewires how students think about math by forcing them to understand the foundational logic (the "why") before they ever see a formula (the "how").

## ✨ Key Features

- **Intuition-First Learning:** Guides the user through mental models (e.g., "slot filling" for factorials) rather than forcing them to memorize symbols.
- **Visual Interactive Trees:** Dynamically renders HTML/CSS branching logic trees to visually prove concepts like the Multiplication Principle without exploding the DOM.
- **Intelligent Mistake Analysis:** The Quiz Engine doesn't just say "Wrong." It catches specific logical fallacies (e.g., "You added instead of multiplying") and explains exactly where the user's intuition failed.
- **Zero-Latency Practice Arena:** Practice problems are JSON-embedded directly into the template on load, resulting in 0.00ms network latency when testing intuition.
- **LaTeX Math Rendering:** Integrates MathJax for beautiful, industry-standard mathematical typography.
- **Dynamic Dashboard:** Tracks "Intuition Checks Passed" and "Experience (XP)" in real-time.
- **Premium UI/UX:** Built with a sleek, responsive design featuring seamless dark mode integration and micro-animations.

## 🛠️ Technology Stack

- **Backend:** Python, Flask, SQLAlchemy (SQLite for development)
- **Frontend:** HTML5, Vanilla JavaScript (ES6+), CSS3 (CSS Variables for theming)
- **Content Engine:** A custom JSON ingestion system (`load_content.py`) that parses structured curriculum files into the database, allowing for infinite scaling of topics without touching frontend code.
- **Typography:** Google Fonts (Inter, Outfit) & MathJax.

## 🚀 Local Setup & Installation

1. **Clone the repository** (and ensure you have Python 3 installed).
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```
3. **Activate the virtual environment:**
   - Windows: `.\venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Populate the Database:**
   Run the content ingestion script. This parses the theory and quiz JSON files and builds the SQLite database.
   ```bash
   python scripts/load_content.py
   ```
6. **Run the Application:**
   ```bash
   python run.py
   ```
7. Visit `http://127.0.0.1:5000` in your browser.

## 🌍 Live Deployment (Render Free-Tier)

This application is fully prepared for production deployment on [Render](https://render.com). 

1. Connect this private repository to Render as a **Web Service**.
2. Set the **Build Command** to:
   ```bash
   pip install -r requirements.txt && python scripts/load_content.py
   ```
   *(Note: Running the load script during build ensures the ephemeral SQLite database is populated every time the free-tier server spins up).*
3. Set the **Start Command** to:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:$PORT run:app
   ```
4. Deploy and enjoy your live MVP!

---
*Built for the future of AI and Data Science education.*
