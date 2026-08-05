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
