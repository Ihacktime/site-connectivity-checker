# Site Connectivity Checker (Streamlit)

Check many URLs concurrently and see status + latency. Export results as CSV.

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python -m pip install -U pip
pip install -r requirements.txt
streamlit run app.py
