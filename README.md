# 🚦 Urban Traffic Congestion Prediction & Signal Optimization System

An AI-powered system that predicts traffic congestion levels and optimizes signal timings using real traffic data. Built with Machine Learning, Streamlit, and Map Visualization.

---

## 🌐 Live Features

- ✅ **Congestion Predictor** – Predict congestion level (Low/Medium/High) from live traffic stats.
- ✅ **Signal Optimizer** – Auto-calculates green light durations using traffic volume per direction.
- ✅ **Congestion Map View** – Visualize congestion hotspots on a live map (Folium).
- ✅ **Animated Signal Simulation** – Blinking traffic signals per intersection using Pydeck.
- ✅ **Future Scope** – Auto-sync timing + smart deployment plans.

---

## 📦 Folder Structure

urban-traffic-ml/
├── app/
│ └── main.py # Streamlit UI
├── data/
│ ├── raw/ # Original datasets
│ └── processed/ # Cleaned, merged, feature-engineered
├── models/ # Trained model and label encoder
├── src/
│ ├── preprocess_data.py # Data cleaning & merging
│ ├── train_model.py # ML training
│ └── optimize_signals.py # PuLP signal optimizer
├── README.md
├── requirements.txt
└── .gitignore


---

## 📊 Tech Stack

- **Frontend**: Streamlit + Pydeck + Folium
- **Backend**: Python, Pandas, NumPy
- **ML**: XGBoost, Random Forest
- **Optimization**: PuLP (Linear Programming)
- **Map Viz**: Folium, Pydeck (DeckGL)
- **Deployment**: Streamlit Cloud

---

## 📁 Dataset

- Source: Toronto City Open Data Portal
- Includes: Volume data, speed bins, direction, timestamps
- Format: CSVs (Daily + Historical)

---

## 🚀 Run Locally

```bash
git clone https://github.com/your-username/urban-traffic-ml.git
cd urban-traffic-ml
pip install -r requirements.txt
streamlit run app/main.py


🛠️ Future Scope

Auto-blinking signals based on optimized timings (already designed)
Integration with real-time APIs
Scalable deployment across multiple city zones


📬 Contact
Srujith Bollam
GitHub: @SrujithBollam
