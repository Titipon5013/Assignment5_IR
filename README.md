# Split Search Engine: Elasticsearch vs. Manual TF-IDF

**Name:** Titipon Tawong  
**Student ID:** 662115013

---

## Project Overview

This project is a split-screen search engine designed to compare the performance and ranking algorithms of two different systems:

- **Left Panel (Elasticsearch + PageRank):** Utilizes Elasticsearch's built-in BM25 algorithm combined with a pre-calculated PageRank score.

- **Right Panel (Manual TF-IDF + PageRank):** Utilizes a custom-built Inverted Index calculating TF-IDF from scratch in memory, combined with the same PageRank score.

The data was collected using a custom Multi-Threaded Crawler set to Depth = 2, resulting in a rich dataset of documents.

---

## Architecture

### Data Collection
- Python-based web crawler (BeautifulSoup, requests) with concurrent threading.

### Ranking Computation
- Power Iteration method applied to generate PageRank scores for all crawled URLs.

### Backend
- Flask API (`app.py`) serving two endpoints:
  - `/api/search_es`: Queries Elasticsearch using a function_score to multiply BM25 by PageRank.
  - `/api/search_manual`: Computes term frequencies, accesses the in-memory inverted index, applies IDF, and multiplies by PageRank.

### Frontend
- Vue 3 + Tailwind CSS, featuring a responsive, brutalist-inspired dark gradient UI with real-time loading states and execution time metrics.

---

## How to Run

### 1. Prerequisites

- Ensure Elasticsearch is running locally on `https://localhost:9200`.
- Python 3.x installed.
- Node.js and npm installed.

### 2. Backend Setup

1. Open a terminal in the project root.

2. Ensure the `crawled/` folder (containing the `.txt` files from the Depth 2 crawl) is placed in the same directory as `app.py`.

3. Install required Python packages:
   ```bash
   pip install flask flask-cors elasticsearch
   ```

4. Start the Flask server:
   ```bash
   python app.py
   ```
   > **Note:** The server will take a few moments to build the manual Inverted Index in memory before starting.

### 3. Frontend Setup

1. Open a second terminal and navigate to the UI folder (e.g., `split-search-ui`).

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open the provided localhost link in your browser to use the search engine.

---

## AI Usage Report

### AI Tool Used
**Gemini**

### Prompts Used
I provided Gemini with the Python code from my previous Hands-on assignments (Crawler, PageRank, and Indexer). I asked the AI to help me adapt this Jupyter Notebook code into a proper Flask backend architecture. For the frontend, I asked the AI to generate a modern, visually appealing UI using Vue.js and Tailwind CSS, while specifying that I would handle the actual API integration, state management, and data fetching myself.

### Expected vs. Actual Output

**Expected:** I expected basic Flask route templates to wrap my existing indexer logic, a standard HTML/CSS layout for the split screen.

**Actual:** The AI provided a highly structured approach for the backend, suggesting loading the Inverted Index and PageRank scores into memory before starting the Flask app to drastically reduce query times. For the UI, it generated a polished, streetwear-inspired dark gradient theme with hover effects and responsive grid layouts.

### How I Used It & My Understanding

I used the AI primarily as an architectural consultant and UI designer.

- **Backend:** I did not blindly copy-paste the backend logic. I adapted my own TF-IDF and PageRank formulas from the hands-on sessions. I utilized the AI to understand how to efficiently structure the Flask API.

- **Frontend:** I utilized the AI to rapidly prototype the visual CSS design (Tailwind classes, gradients, and layout structure). However, I manually wrote the Vue setup script, implemented the fetch API calls to route data to `/api/search_es` and `/api/search_manual`, and managed the reactive states (ref) for loading indicators, total hits, and execution times to ensure the UI successfully communicated with my custom backend.


