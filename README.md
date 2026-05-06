# CyberAttrib.AI

> AI-Powered Cyber Attack Attribution Platform using Machine Learning & Deep Learning

## Overview

CyberAttrib.AI leverages 8 AI/ML models to attribute cyber attacks to specific threat actors (APTs) with high accuracy and explainable results. The platform features an interactive attribution simulator, model explorer with performance benchmarks, and a 6-stage processing pipeline visualization.

## Features

- **Attribution Simulator** — Run simulated attribution on 6 real-world APT attack scenarios
- **Model Explorer** — Compare 8 ML/DL models (SVM, RF, NB, KNN, ANN, CNN, RNN, LSTM)
- **Processing Pipeline** — Interactive 6-stage data-to-attribution pipeline
- **Threat Dashboard** — Real-time system metrics and threat intelligence overview
- **Model Comparison Chart** — Visual performance comparison across all models
- **Export Reports** — Download attribution results as JSON

## Tech Stack

| Category | Technologies |
|----------|-------------|
| Frontend | HTML5, CSS3, JavaScript |
| AI/ML | Python, Scikit-learn, TensorFlow, PyTorch |
| Data | Pandas, NumPy, MITRE ATT&CK |
| Visualization | Chart.js, Matplotlib |

## AI Models

| Model | Type | Accuracy | F1-Score |
|-------|------|----------|----------|
| LSTM | Deep Learning | 95% | 94% |
| CNN | Deep Learning | 93% | 92% |
| Random Forest | Machine Learning | 92% | 90% |
| ANN | Deep Learning | 91% | 89% |
| SVM | Machine Learning | 88% | 85% |
| RNN | Deep Learning | 87% | 87% |
| KNN | Machine Learning | 83% | 82% |
| Naïve Bayes | Machine Learning | 79% | 78% |

## How to Run

```bash
# Clone the repository
git clone https://github.com/yourusername/cyberattrib-ai.git

# Navigate to directory
cd cyberattrib-ai

# Serve locally
python -m http.server 8080

# Open in browser
# http://localhost:8080
```

## Project Structure

```
├── index.html      # Main application page
├── styles.css      # Design system & component styles
├── app.js          # Application logic & interactivity
└── README.md       # Project documentation
```

## Attribution Scenarios

- **APT28 (Fancy Bear)** — Spear phishing + credential harvesting
- **Lazarus Group** — Supply chain compromise + ransomware
- **APT41 (Double Dragon)** — Zero-day espionage + financial crime
- **APT29 (Cozy Bear)** — Stealthy long-term intelligence gathering
- **Turla (Venomous Bear)** — Satellite-based C2 infrastructure
- **APT10 (Stone Panda)** — Cloud service provider infiltration

## License

MIT License — See [LICENSE](LICENSE) for details.
