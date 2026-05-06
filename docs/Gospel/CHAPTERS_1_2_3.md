# Chapter 1: Introduction

## 1.1 Background of the Study
As cyber-attacks become more sophisticated, identifying the perpetrators—a process known as cyber attribution—has become a critical challenge for national security, financial institutions, and private enterprises. Traditional attribution relies heavily on manual analysis of Indicators of Compromise (IoCs) and Tactics, Techniques, and Procedures (TTPs), which is time-consuming and often subjective. The rise of Advanced Persistent Threats (APTs) necessitates more robust, automated, and data-driven approaches.

## 1.2 Problem Statement
Cyber attribution is inherently difficult due to the "anonymity of the internet" and the use of "false flag" operations where one actor mimics the techniques of another. Current manual attribution methods cannot keep pace with the volume and velocity of modern cyber threats. There is a pressing need for an intelligent system that can analyze complex attack patterns and provide high-confidence attribution using state-of-the-art AI algorithms.

## 1.3 Aim and Objectives
The primary aim of this project is to develop **CyberAttrib.AI**, an AI-powered platform for cyber-attack attribution. The specific objectives include:
1. To design a 6-stage processing pipeline for ingesting and analyzing threat intelligence data.
2. To implement and compare 8 different Machine Learning and Deep Learning models for attack classification.
3. To map attack techniques to the **MITRE ATT&CK** framework for standardized feature extraction.
4. To develop an interactive dashboard for real-time threat monitoring and attribution simulation.

## 1.4 Scope of the Study
The project focuses on attributing attacks to well-known APT groups (such as APT28, Lazarus, and APT41) using a dataset of historical attack patterns. The study evaluates four Machine Learning models (SVM, Random Forest, Naïve Bayes, KNN) and four Deep Learning models (ANN, CNN, RNN, LSTM).

## 1.5 Significance of the Study
This study provides a scalable framework for Security Operation Centers (SOCs) to automate the attribution process. By providing probabilistic confidence scores, it enables security analysts to make faster, more informed decisions during incident response.

---

# Chapter 2: Literature Review

## 2.1 Evolution of Cyber Attribution
Historically, attribution was achieved through political intelligence and manual forensics. With the advent of Big Data, researchers began applying statistical methods to identify "attacker fingerprints." Modern research has shifted toward **Machine Learning (ML)** and **Deep Learning (DL)** to identify non-linear patterns in network traffic and malware behavior.

## 2.2 The MITRE ATT&CK Framework
The MITRE ATT&CK framework has emerged as the industry standard for documenting adversary behavior. Unlike IoCs (like IP addresses), which are easy for attackers to change, TTPs represent the "behavioral DNA" of an actor. This project leverages the ATT&CK matrix to create high-fidelity feature vectors for our AI models.

## 2.3 Machine Learning in Cybersecurity
- **Random Forest (RF):** Known for its high accuracy and resistance to overfitting, RF is widely used for classifying malware families.
- **Support Vector Machines (SVM):** Effective in high-dimensional spaces, making it suitable for sparse TTP datasets.
- **Naïve Bayes & KNN:** These serve as baseline models for evaluating the complexity of the attribution task.

## 2.4 Deep Learning and Sequence Modeling
Cyber-attacks are often sequential (e.g., Reconnaissance → Initial Access → Lateral Movement). 
- **Recurrent Neural Networks (RNN) and LSTM:** These are specifically designed to handle sequential data, allowing the system to learn the "story" of an attack rather than just isolated events.
- **Convolutional Neural Networks (CNN):** While typically used for images, CNNs are effective at detecting local patterns in binary data or network packet headers.

---

# Chapter 3: Methodology

## 3.1 System Architecture
CyberAttrib.AI is built on a decoupled architecture:
1. **Frontend:** A responsive web interface built with HTML5, CSS3, and Vanilla JavaScript for data visualization and simulation.
2. **Backend:** A high-performance API powered by **FastAPI** (Python), handling real-time requests and model inference.
3. **AI Layer:** A suite of models implemented using **Scikit-Learn, TensorFlow, and PyTorch**.

## 3.2 The 6-Stage Processing Pipeline
The system follows a rigorous data processing flow:
1. **Data Input:** Collection of raw threat data (JSON/CSV).
2. **Preprocessing:** Data cleaning and label encoding.
3. **Feature Extraction:** Mapping raw indicators to 143 unique MITRE ATT&CK techniques.
4. **AI Model Layer:** Concurrent processing of the feature vector across all 8 models.
5. **Attribution Engine:** Aggregating model outputs to produce a final verdict.
6. **Evaluation Module:** Real-time calculation of performance metrics.

## 3.3 Data Source and Dataset
The project utilizes a curated dataset derived from public threat intelligence repositories (e.g., AlienVault OTX, Mandiant reports) and simulated attack scenarios. The dataset includes 1,030 samples categorized by APT group and technique usage.

## 3.4 Model Training and Implementation
- **Machine Learning Models:** Trained using Scikit-Learn with 5-fold cross-validation.
- **Deep Learning Models:** Developed using TensorFlow/Keras with Dropout layers to prevent overfitting and Adam optimizer for efficient convergence.
- **Live Feed Simulation:** A Random Forest model is deployed in the production backend to provide immediate inference on incoming data streams via WebSockets.
