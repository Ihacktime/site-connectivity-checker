# Site Connectivity Checker

Tiny async CLI that checks many URLs concurrently and reports status + latency. Optional CSV export.

## Run
```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python checker.py -u https://google.com -u example.com
python checker.py -f urls.txt -c 50 --timeout 8 --csv out.csv
