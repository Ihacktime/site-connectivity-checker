# Site Connectivity Checker (Streamlit)

Check many URLs **concurrently** and see **status** + **latency**. Export results as **CSV**.

## Quick start
~~~bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -U pip
pip install -r requirements.txt
streamlit run app.py
~~~

## How to use
1. Paste **one URL per line** (scheme optional; `example.com` → `https://example.com`).
2. Set options in the sidebar:
   - **Concurrency**, **Timeout**, **Follow redirects**, **Verify SSL**
3. Click **“Check now”** to run.
4. View results table:
   - ✅/❌, **HTTP status**, **latency (ms)**, **final URL** (after redirects)
5. Click **Download CSV** to save results.

## Notes
- Normalizes and de-duplicates URLs.
- Uses a persistent `requests.Session` with a real User-Agent.
- Works locally and on Streamlit Community Cloud.

## Deploy (free)
- Go to **share.streamlit.io** → **Create app**  
  Repo: `ihacktime/site-connectivity-checker` · Branch: `main` · File: `app.py`
- After deploy, add the app URL to this repo’s **About → Website**.

## License
MIT
