# PhishLens AI

AI-powered phishing and scam URL detection platform that analyzes URLs using machine-learning classification, security heuristics, risk scoring, and explainable security signals.

## Overview

PhishLens AI is a defensive cybersecurity platform designed to identify potentially malicious URLs and explain the security signals behind each prediction.

Instead of returning only a phishing/legitimate result, PhishLens combines:

- Machine-learning-based URL classification
- URL feature engineering
- Risk scoring
- Security indicators
- Explainable analysis signals
- Scan history
- REST API integration
- Interactive React frontend

The system is designed for defensive analysis of suspicious URLs before users interact with them.

## Key Features

### AI-Based URL Detection

PhishLens extracts structural and lexical features from URLs and uses a trained machine-learning model to estimate phishing probability.

### Explainable Analysis

The system exposes the signals extracted from the URL, including:

- HTTPS usage
- IP-address usage
- `@` symbol presence
- URL length
- Number of subdomains
- Security-sensitive keywords
- Query parameters
- Special-character patterns

This makes the prediction easier to understand instead of presenting the model as a black box.

### Risk Scoring

The phishing probability is combined with security-rule adjustments to generate a final risk score from `0–100`.

The application classifies results as:

- Safe
- Suspicious
- Phishing

### Security Dashboard

The React frontend provides:

- URL scanner
- Analysis pipeline
- Threat assessment
- Risk score
- Model confidence
- Security indicators
- Explainable analysis
- Structural signal profile
- Scan history
- Light and dark themes

## How It Works

```text
User enters URL
       |
       v
React Frontend
       |
       | REST API
       v
FastAPI Backend
       |
       v
URL Feature Extraction
       |
       v
Robust Logistic Regression Model
       |
       +-------------------+
       |                   |
       v                   v
   Risk Engine      Explainable Signals
       |                   |
       +---------+---------+
                 |
                 v
        Final Analysis Result
        - Classification
        - Risk Score
        - Probabilities
        - Indicators
        - Signals
Machine Learning Pipeline
Baseline Dataset
The project initially used the PhiUSIIL URL dataset for baseline experimentation.
The baseline dataset contained:
- 235,795 URLs
- 34 engineered URL features
- Binary phishing/legitimate labels
A Logistic Regression model was used as the initial baseline.
Baseline Model Results
The baseline model achieved:
- Accuracy: 95.22%
- Phishing Precision: 98.08%
- Phishing Recall: 90.62%
- Phishing F1-score: 94.20%
During evaluation, dataset-specific URL path characteristics were identified that could cause unrealistic performance on realistic legitimate URLs.
Robust Dataset
To reduce this dependency, a supplementary legitimate URL dataset was incorporated.
The resulting robust feature dataset contained:
- 405,687 URL records
- 34 URL features
- Binary labels
A balanced split was created using all available phishing samples and an equal number of legitimate samples.
Robust Model
The robust Logistic Regression model was evaluated on a held-out test set.
After threshold analysis, a phishing decision threshold of 0.55 was selected.
At this threshold:
- Accuracy: 82.67%
- Phishing Precision: 85.88%
- Phishing Recall: 78.19%
- Phishing F1-score: 81.85%
- Legitimate Recall: 87.15%
- False Positive Rate: 12.85%
The robust evaluation is preferred for assessing generalization because it includes more realistic legitimate URL structures.
URL Features
PhishLens extracts structural and lexical URL characteristics such as:
- URL length
- Hostname length
- Path length
- Dot count
- Hyphen count
- Underscore count
- Slash count
- Query parameters
- @ symbols
- Percent encoding
- Digit count
- HTTPS usage
- IP-address usage
- Subdomain count
- Security-sensitive keywords
Security-sensitive keywords include:
login, signin, verify, verification, secure, account, update, password, bank, confirm, authenticate, credential, wallet, and payment.
Explainable Analysis
For every URL analysis, PhishLens exposes the extracted security signals used to support the prediction.
The current analysis response contains 8 explainable signals, covering:
- HTTPS
- IP address
- @ symbol
- URL length
- Subdomains
- Security keywords
- Query parameters
- Special characters
Each signal contains:
- Signal name
- Observed value
- Interpretation
- Severity
This allows users to understand why a URL received its particular risk assessment.
Risk Engine
The risk engine combines the machine-learning phishing probability with additional security heuristics.
Additional risk adjustments may be applied when URLs contain characteristics such as:
- No HTTPS
- IP addresses instead of domain names
- @ symbols
- Unusually long URLs
- Excessive subdomains
- Multiple security-sensitive keywords
- Suspicious special-character patterns
The final risk score is constrained to:
0–100
Classification thresholds:
- 0–39 → Safe
- 40–74 → Suspicious
- 75–100 → Phishing
Technology Stack
Frontend
- React
- Vite
- JavaScript
- CSS
Backend
- Python
- FastAPI
- Pydantic
- Uvicorn
Machine Learning
- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Logistic Regression
Testing
- Pytest
- HTTPX
Version Control
- Git
- GitHub
Project Structure
PhishLens-AI/
|
+-- backend/
|   +-- app/
|       +-- api/
|       +-- core/
|       +-- models/
|       +-- schemas/
|       +-- services/
|       +-- utils/
|       +-- main.py
|
+-- frontend/
|   +-- src/
|   |   +-- App.jsx
|   |   +-- App.css
|   |   +-- index.css
|   +-- package.json
|
+-- ml/
|   +-- evaluation/
|   +-- features/
|   +-- models/
|   +-- services/
|   +-- training/
|   +-- dataset/
|
+-- tests/
|
+-- docs/
|
+-- .gitignore
+-- README.md

API
Analyze URL
POST /api/v1/analyze/url

Request:
{
  "url": "https://www.google.com/"
}

Example response structure:
{
  "url": "https://www.google.com/",
  "classification": "safe",
  "risk_score": 21,
  "phishing_probability": 0.2066,
  "legitimate_probability": 0.7934,
  "indicators": [],
  "signals": [
    {
      "name": "HTTPS",
      "value": "Enabled",
      "interpretation": "The URL uses HTTPS.",
      "severity": "low"
    }
  ]
}

The actual response contains the complete set of explainable signals generated by the analysis engine.
Health Check
GET /health

Response:
{
  "status": "healthy"
}

Installation
1. Clone the Repository
git clone https://github.com/Aayeshashk/PhishLens-AI.git
cd PhishLens-AI

2. Create the Python Environment
python -m venv backend/venv

On Windows:
backend\venv\Scripts\activate

3. Install Backend Dependencies
pip install fastapi uvicorn sqlalchemy psycopg[binary] python-dotenv pydantic[email] pandas numpy scikit-learn matplotlib seaborn joblib httpx pytest

4. Install Frontend Dependencies
cd frontend
npm install
cd ..

Running the Application
Start the Backend
From the project root:
uvicorn app.main:app --reload --app-dir backend

The API will be available at:
http://127.0.0.1:8000

Start the Frontend
Open another terminal:
cd frontend
npm run dev

Vite will display the local frontend URL in the terminal.
Testing
The backend test suite currently passes completely:
40 passed

Run the tests with:
backend\venv\Scripts\python.exe -m pytest -q

Production Build
The React frontend has been successfully built using:
cd frontend
npm run build

The production files are generated in:
frontend/dist/

Screenshots
Screenshots of the PhishLens AI dashboard can be added here.
Suggested screenshots:
- URL Scanner
- Threat Assessment
- Explainable Analysis
- Structural Signal Profile
- Light Mode
Security Notice
PhishLens AI is intended for defensive cybersecurity analysis and educational/research purposes.
A machine-learning prediction is not a guarantee that a URL is malicious or safe. Users should avoid interacting with suspicious URLs and use additional security controls when making security-critical decisions.
Limitations
- The current ML model is based on URL-level features.
- The system does not inspect webpage content or execute websites.
- Model performance depends on the characteristics of the training data.
- Risk heuristics supplement, rather than replace, machine-learning predictions.
- A prediction should not be treated as definitive proof of malicious intent.
Future Scope
Potential future improvements include:
- Transformer-based URL models
- Character-level deep learning
- Website content analysis
- Domain reputation intelligence
- DNS and WHOIS signals
- Real-time threat intelligence feeds
- Browser extension integration
- Email phishing analysis
- Improved probability calibration
- Larger and more diverse datasets
- Continuous model evaluation
Project Status
PhishLens AI currently has a functional end-to-end implementation:
- Machine-learning detection
- Robust dataset pipeline
- Threshold analysis
- Risk scoring
- Explainable security signals
- FastAPI backend
- React frontend
- Scan history
- Automated tests
- Production frontend build
Repository
GitHub:
https://github.com/Aayeshashk/PhishLens-AI
License
This project is intended for academic, research, and defensive cybersecurity purposes.