# Compar'IA Dashboard

A **Streamlit dashboard** to benchmark Large Language Models (LLMs) on **Quality, Latency, Energy, and CO₂ emissions**, supporting the Green AI initiative.

---

##  Project Overview

The goal of this project is to evaluate LLMs based on multiple metrics while considering environmental and performance trade-offs. The dashboard allows users to visualize the efficiency and environmental impact of models through interactive charts and tables.

Key metrics collected for each model:

- **Quality** – Model performance on a set of benchmark tasks (0-5 scale)
- **Latency** – Average response time per task (seconds)
- **CO₂** – Carbon emissions per query (kg eq.)
- **Energy** – Energy consumption per query (kWh)
- **Cost** – Optional: Cost per query (€ or $)

---

## Tasks for Benchmarking (30)

The evaluation tasks are divided into four categories based on difficulty and type:

### 1. Easy factual & rewriting (Tasks 1–10)
1. Who is the current UN Secretary-General?  
2. Summarize a 150-word news article in one sentence.  
3. Translate a paragraph about climate change into French.  
4. Classify sentiment of 3 tweets (positive/negative).  
5. Extract email & phone number from a text.  
6. Explain the difference between RAM and ROM.  
7. Name three renewable energy sources.  
8. Turn a dense paragraph into bullet points.  
9. Rewrite a sentence in a formal business tone.  
10. Create a catchy blog title about electric cars.  

### 2. Reasoning & quantitative (Tasks 11–15)
11. Solve a train problem: Train A leaves at 10:00 at 100 km/h, Train B at 11:00 at 120 km/h — when do they meet?  
12. Solve a system of equations: 2x+3y=12 and x−y=4.  
13. Compute the derivative of x³ + 2x² − 5x + 7.  
14. Explain “overfitting” simply.  
15. Convert 1500 W to kWh for 24 h and estimate yearly cost at 0.20 €/kWh.  

### 3. Programming & debugging (Tasks 16–20)
16. Write Python code to reverse a string.  
17. Fix the bug: `for i in range(5) print(i)`.  
18. Explain the output of a recursive Python function (provided).  
19. Suggest an optimization for a slow SQL query (given).  
20. Explain Big-O complexity of binary search.  

### 4. Harder knowledge & reasoning (Tasks 21–25)
21. Compare nuclear vs solar energy (3 pros / 3 cons each).  
22. Explain GDPR compliance steps for a SaaS startup.  
23. Summarize a Wikipedia article on climate change into 5 key bullet points.  
24. Describe the transformer architecture in detail (attention, encoder/decoder).  
25. List and explain three differences between supervised, unsupervised, and reinforcement learning.  

### 5. Advanced / creative & multi-step (Tasks 26–30)
26. Write a project plan for deploying AI to monitor deforestation using satellites.  
27. Draft a LinkedIn post convincing a company to adopt green AI.  
28. Create a short legal disclaimer about data privacy for an AI chatbot.  
29. Imagine and explain a new business model using AI to reduce carbon emissions in logistics.  
30. Analyze a research abstract and rewrite it for a non-technical policymaker.  

> Tasks 26–30 are intentionally complex, multi-step, requiring planning, reasoning, and domain knowledge.

---

## Dashboard & Visualizations

The Streamlit dashboard includes the following:

1. **Dataset Overview** – Inspect the raw data collected for each model and task.  
2. **Quality vs Energy** – Scatter plot to evaluate efficiency (higher quality with lower energy is better).  
3. **Quality vs Cost** – Compare model performance relative to cost per query (if cost data is available).  
4. **Latency comparison** – Bar charts and line plots to analyze average response times by model and task.  
5. **Best Trade-off Table** – Ranking of models based on a **composite score**, considering:
   - Quality
   - Latency
   - Energy consumption
   - CO₂ emissions  

### Composite Score Explanation

The **overall score** for each model is calculated as a weighted combination of normalized metrics:
Score = 0.4 * Quality_norm + 0.2 * Latency_norm + 0.2 * CO2_norm + 0.2 * Energy_norm


- `Quality_norm` = Quality / max(Quality)  
- `Latency_norm` = 1 - (Latency / max(Latency))  
- `CO2_norm` = 1 - (CO₂ / max(CO₂))  
- `Energy_norm` = 1 - (Energy / max(Energy))  

> Higher scores indicate better trade-offs between performance and environmental impact.

---

## Deliverables

- **Spreadsheet** – Contains all collected metrics per model and task.  
- **Dashboard** – Interactive Streamlit app including:
  - Quality vs Energy graph    
  - Latency comparison plots  
  - Final “Best Trade-off” ranking table

The project includes an **interactive Streamlit application** to explore and compare the performance of language models (LLMs) across multiple dimensions: quality, energy consumption, CO₂ emissions, and latency.

### Data Upload

The dashboard have somme data by default.

Inside the app, you will see a file uploader in the sidebar (Import Data).

You can either:

- Upload **Green AI V2.xlsx** (provided in this repo which contains the benchmark dataset used in this project)

- Upload your own file, as long as it contains the same columns:
  Models | Size | Question | Quality | Latency | CO2 | Energy | Questions class


If the uploaded file does not match this structure, the app will raise an error.

### Key Features

- **Overview**
  - Key metrics: total CO₂, total energy consumption, average quality, number of tests.
  - Dataset preview (Excel/CSV upload).
  - Interactive plots: energy and CO₂ evolution per question, performance heatmap by question category.

- **Quality vs Energy**
  - Interactive scatter plots showing the trade-off between **quality** and **energy consumption**.
  - **Efficiency Score (Quality / Energy)**: a metric to compare how effective models are.
  - Environmental impact analysis (energy usage & CO₂ emissions).

- **Latency**
  - Comparison of average latency across models.
  - Latency distribution by model size.
  - Latency evolution across different tasks.

- **Best Trade-off Ranking**
  - Global ranking of models based on an **Efficiency Score** combining quality, speed, energy, and CO₂.
  - **Interactive tables** showing:
    - Best models per **size** (Small / Medium / Large) and **question category**.
    - Best models per **question category only** (ignoring size).
  - Normalized scores (0–100) with comparative bar charts.

### Efficiency Score Explanation

The **Efficiency Score** evaluates the balance between performance and sustainability:

- **Quality (40%)** → higher quality improves the score  
- **Latency (20%)** → faster response times improve the score  
- **CO₂ emissions (20%)** → lower emissions improve the score  
- **Energy consumption (20%)** → lower energy usage improves the score  

**Formula:** Score = 0.4 * Quality_norm + 0.2 * Latency_norm + 0.2 * CO2_norm + 0.2 * Energy_norm

Each metric is **normalized between 0 and 1** to ensure comparability across models.  
A higher score indicates a **better trade-off between accuracy, speed, and environmental impact**.


---

## Technologies Used

- **Python**  
- **Streamlit with ngrok** – Dashboard development  
- **Plotly & Altair** – Interactive charts  
- **Pandas & NumPy** – Data processing and aggregation  

##  Launch the App

You can run the dashboard either **locally** on your machine or directly on **Google Colab**.

### Option 1 – Run on Google Colab
If you want to run the dashboard without installing anything locally:
Open the provided Colab notebook: Comparai_dashboard.ipynb
Run all the cells.

At the end of execution, Colab will display a link to access the Streamlit app in your browser.
Tip: On Colab, you may need to install Streamlit and configure ngrok or localtunnel to expose the app online.

### Option 2 – Run locally (Bash)
Make sure you have installed the dependencies (see Installation section), then run:

``bash
streamlit run app.py

This will start a local server, and Streamlit will give you a link (usually http://localhost:8501) to open the dashboard in your browser.
