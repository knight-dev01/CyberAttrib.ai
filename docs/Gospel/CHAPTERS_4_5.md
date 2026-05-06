# Chapter 4: Results and Discussion

## 4.1 Overview of Results
The CyberAttrib.AI platform was evaluated using a comprehensive dataset of cyber-attack indicators mapped to the MITRE ATT&CK framework. Eight different machine learning and deep learning models were tested to determine their effectiveness in attributing attacks to specific Advanced Persistent Threat (APT) groups. The models were evaluated based on four key metrics: Accuracy, Precision, Recall, and F1-Score.

## 4.2 Model Performance Analysis
The results of the model evaluation are summarized in the table below:

| Model Name | Type | Accuracy | Precision | Recall | F1-Score |
|------------|------|----------|-----------|--------|----------|
| **LSTM** | Deep Learning | 95% | 94% | 93% | 94% |
| **CNN** | Deep Learning | 93% | 92% | 91% | 92% |
| **Random Forest** | Machine Learning | 92% | 91% | 90% | 90% |
| **ANN** | Deep Learning | 91% | 90% | 88% | 89% |
| **SVM** | Machine Learning | 88% | 86% | 84% | 85% |
| **RNN** | Deep Learning | 87% | 87% | 86% | 87% |
| **KNN** | Machine Learning | 83% | 82% | 81% | 82% |
| **Naïve Bayes** | Machine Learning | 79% | 78% | 77% | 78% |

### 4.2.1 Comparison of Deep Learning vs. Machine Learning
The experimental results demonstrate that Deep Learning models, particularly **LSTM (Long Short-Term Memory)** and **CNN (Convolutional Neural Networks)**, outperformed traditional Machine Learning models. 
- **LSTM** achieved the highest accuracy of 95%, likely due to its ability to capture temporal dependencies and sequential patterns in attack behaviors (e.g., the order of TTPs).
- **Random Forest** was the top performer among traditional ML models (92%), showcasing its robustness in handling high-dimensional feature sets like MITRE ATT&CK techniques.

## 4.3 Attribution Simulation Results
The Attribution Simulator provided real-time validation of the models. In scenarios such as **Operation Phantom Bear (APT28)** and **Operation DarkSeoul (Lazarus Group)**, the platform successfully matched indicators of compromise (IoCs) to the correct threat actor with over 90% confidence.

- **Scenario APT28:** The model correctly identified spear-phishing and lateral movement patterns as characteristic of Fancy Bear.
- **Scenario Lazarus:** The system flagged supply chain compromise and ransomware deployment as high-probability indicators for the Lazarus Group.

## 4.4 Discussion
The high accuracy across most models suggests that the MITRE ATT&CK framework provides a solid foundation for feature extraction in cyber attribution. However, the lower performance of **Naïve Bayes (79%)** indicates that the assumption of feature independence is not entirely valid in complex cyber attacks, where various techniques are often interlinked.

---

# Chapter 5: Conclusion and Recommendations

## 5.1 Conclusion
The CyberAttrib.AI project successfully demonstrated the feasibility of using AI-powered classification for cyber-attack attribution. By leveraging 8 different models, the project provided a comparative analysis that highlights the strengths of Deep Learning in the cybersecurity domain. 

Key takeaways include:
1. **Model Efficacy:** LSTM is currently the most effective model for sequence-based attribution.
2. **Framework Integration:** Mapping IoCs to the MITRE ATT&CK framework significantly enhances the interpretability and accuracy of the attribution engine.
3. **Real-time Capability:** The integration of a FastAPI backend allows for low-latency inference, making it suitable for live SOC environments.

## 5.2 Recommendations
Based on the findings of this project, the following recommendations are proposed:
1. **Hybrid Model Development:** Future iterations should explore ensemble or hybrid models (e.g., combining CNN and LSTM) to further increase accuracy and reduce false positives.
2. **Dynamic Dataset Updates:** The attribution engine should be integrated with live threat intelligence feeds (e.g., MISP or AlienVault OTX) to stay updated on evolving APT tactics.
3. **Explainable AI (XAI):** Implementing more advanced XAI techniques (like SHAP or LIME) would provide security analysts with deeper insights into *why* a specific model attributed an attack to a certain group.
4. **Adversarial Robustness:** Research into hardening these models against adversarial machine learning (where attackers intentionally manipulate features to evade detection) is highly recommended.
