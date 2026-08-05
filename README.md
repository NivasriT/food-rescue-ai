# 🥗 RescueAI - Intelligent Food Redistribution MVP

RescueAI is a modern, lightweight, single-file Streamlit web application designed for hackathon demos. It solves surplus food redistribution by connecting restaurants with local non-profit organizations (NGOs). By utilizing rule-based visual classifier simulations, freshness algorithms, and spatial Euclidean distance mappings, it automates the matching of surplus stock to nearby NGOs, maximizing recovery speed and tracking carbon footprint savings.

---

## 🚀 Key Features & Capabilities

* **🏠 Centralized Command Dashboard (Home)**: High-impact KPI rows demonstrating cumulative kilograms of rescued food, active supplier and distributor nodes, and equivalent CO2 emission savings. Includes real-time listings of active donations.
* **🏢 Partner Registration Registry**: Interactive forms to onboard new Restaurants and NGO warehouses. Collects custom latitude/longitude coordinates to construct an active urban matching grid (pre-populated with Bengaluru coordinates for out-of-the-box demo testing).
* **📤 Automated Donation Dispatch Wizard**: The core transaction pipeline:
  1. Input donation details or upload food packages.
  2. The **mock AI Scanner** matches categories (Produce, Bakery, Dairy, cooked meals, Meat) and reports confidence.
  3. The **Freshness Score Algorithm** projects a remaining safe shelf life based on storage temp (Ambient, Refrigerated, Frozen) and hours since prep.
  4. The **NGO Proximity Matcher** calculates the closest active NGO using Euclidean distance.
  5. The **Carbon Offset Module** registers environmental impact (2.5 kg CO2 saved per kg of food).
  6. Sends the notification and saves the record to the local JSON datastore.
* **🤖 AI Food Detection Playground**: Standalone visual classification simulator. Upload any food image and receive softmax probability charts for class matching.
* **🍏 Spoilage & Freshness Simulator**: Diagnostic calculator showing safe holding thresholds and storage guidelines.
* **🤝 Proximity NGO Matcher**: Urban coordinates grid displaying spatial distributions. Draws direct 2D line vectors between origin restaurants and recommended NGOs.
* **📊 Sustainability Analytics**: Responsive Plotly charts visualizing trends, status percentages, category weight distribution, and leadership tables.

---

## 🛠️ System Architecture

RescueAI is built entirely in Python using modern, offline libraries to guarantee zero lag, zero setup costs, and instant execution.

* **Frontend Wrapper (`app.py`)**: UI layouts, navigation systems, custom green glassmorphism CSS styling, and dashboard rendering.
* **Data Layer (`database.py`)**: Automatic JSON directory initialization and data writes. Implements pre-seeded restaurant and NGO structures on startup.
* **Predictive Engines (`ml_models.py`)**: Holds all rule-based class matching, Euclidean spacing, and freshness math.
* **JSON Databases (`data/*.json`)**: Flat-file relational tables storing restaurants, NGOs, and donations.

---

## ⚡ Local Setup & Execution

### 1. Prerequisites
Ensure you have Python 3.8 or higher installed on your system.

### 2. Installation
Install the necessary Streamlit and visualization dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the App
Launch the Streamlit web server locally:
```bash
streamlit run app.py
```
Open your browser and navigate to **`http://localhost:8501`**.

---

## 📤 Git & GitHub Upload Instructions

If Git is not yet configured on your machine, follow these steps to push the project files to your GitHub repository at `https://github.com/NivasriT/food-rescue-ai`:

### 1. Install Git
If git is not recognized in your terminal, download and install Git from [https://git-scm.com/downloads](https://git-scm.com/downloads).

### 2. Initialize and Upload via Command Line
Run the following commands in your project root directory (ensure you run in Git Bash or your terminal path after installation):

```bash
# Initialize local git repository
git init

# Add all files to staging, excluding venv files (which are in .gitignore)
git add .

# Create initial commit
git commit -m "feat: complete Streamlit Food Rescue AI MVP"

# Link your remote GitHub repository
git remote add origin https://github.com/NivasriT/food-rescue-ai.git

# Set main branch
git branch -M main

# Push code to GitHub
git push -u origin main --force
```

---

## 🌐 Render Cloud Deployment

Render is a robust cloud platform for hosting Python web applications. Follow these steps to host your Streamlit application live:

### 1. Quick Config using Blueprint (`render.yaml`)
We have created a `render.yaml` file in the root directory. When you connect your GitHub repository to Render, it will automatically detect this blueprint and set up a Web Service with the correct configurations.

### 2. Manual Config on Render Dashboard
If you prefer configuring it manually via the Render web GUI:
1. Log in to [Render](https://render.com/) and click **New > Web Service**.
2. Connect your GitHub repository: `https://github.com/NivasriT/food-rescue-ai`.
3. Set the following settings:
   - **Name**: `food-rescue-ai`
   - **Environment/Runtime**: `Python`
   - **Branch**: `main`
   - **Region**: Select the region closest to you.
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```bash
     streamlit run app.py --server.port $PORT --server.address 0.0.0.0
     ```
4. Under **Instance Type**, select the **Free** tier.
5. Click **Create Web Service**. Your app will build and be live at `https://food-rescue-ai.onrender.com` (or a similar custom sub-domain generated by Render).

*Note: Since the app persistent data is saved to local JSON files, any donations logged while running on Render's free tier will reset when the container spins down due to inactivity. This is standard behavior for stateless cloud deployments and is perfect for hackathon evaluations.*
