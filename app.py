import time, io, csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

import requests
import streamlit as st

st.set_page_config(page_title="Site Connectivity Checker", page_icon="🌐", layout="centered")
st.title("🌐 Site Connectivity Checker")

def normalize_url(u: str) -> str:
    u = u.strip()
    if not u:
        return ""
    parsed = urlparse(u if "://" in u else f"https://{u}")
    scheme = parsed.scheme or "https"
    netloc = parsed.netloc or parsed.path
    path = parsed.path if parsed.netloc else ""
    return f"{scheme}://{netloc}{path}"

def check_one(session: requests.Session, url: str, timeout: float, follow: bool, verify_ssl: bool):
    url = normalize_url(url)
    start = time.perf_counter()
    try:
        resp = session.get(url, timeout=timeout, allow_redirects=follow, verify=verify_ssl)
        elapsed = int((time.perf_counter() - start) * 1000)
        return {
            "url": url,
            "final_url": resp.url,
            "status": resp.status_code,
            "latency_ms": elapsed,
            "ok": 200 <= resp.status_code < 400,
            "error": "",
        }
    except Exception as e:
        elapsed = int((time.perf_counter() - start) * 1000)
        return {
            "url": url, "final_url": "", "status": None,
            "latency_ms": elapsed, "ok": False, "error": str(e)
        }

def run_checks(urls, workers, timeout, follow, verify_ssl):
    headers = {"User-Agent": "ihacktime-site-checker/1.0"}
    results = []
    urls = [u for u in {normalize_url(u) for u in urls} if u]
    if not urls:
        return results
    with requests.Session() as session:
        session.headers.update(headers)
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futures = {ex.submit(check_one, session, u, timeout, follow, verify_ssl): u for u in urls}
            progress = st.progress(0.0)
            total = len(futures)
            done = 0
            for fut in as_completed(futures):
                results.append(fut.result())
                done += 1
                progress.progress(done / total)
    return sorted(results, key=lambda r: (not r["ok"], r["latency_ms"]))

def results_table(rows):
    if not rows:
        st.warning("No results.")
        return
    st.write("### Results")
    st.write("| OK | Status | Latency (ms) | Final URL | Error |")
    st.write("|---:|:------:|-------------:|-----------|-------|")
    for r in rows:
        ok = "✅" if r["ok"] else "❌"
        st.write(f"| {ok} | {r['status'] if r['status'] is not None else ''} | {r['latency_ms']} | {r['final_url'] or r['url']} | {r['error'][:80]} |")

    # CSV download
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=["url", "final_url", "status", "latency_ms", "ok", "error"])
    writer.writeheader()
    for r in rows:
        writer.writerow(r)
    st.download_button("Download CSV", buf.getvalue().encode("utf-8"), "site-checks.csv", "text/csv")

def main():
    with st.sidebar:
        st.header("Settings")
        workers = st.slider("Concurrency", 1, 100, 30)
        timeout = st.slider("Timeout (seconds)", 1, 30, 10)
        follow = st.toggle("Follow redirects", True)
        verify_ssl = st.toggle("Verify SSL", True)

    st.caption("Enter one URL per line. Scheme optional (e.g., `example.com` → `https://example.com`).")
    default_text = "google.com\nexample.com\nhttps://github.com"
    urls_text = st.text_area("URLs", value=default_text, height=140)
    urls_list = [line for line in urls_text.splitlines() if line.strip() and not line.strip().startswith("#")]

    if st.button("Check now", use_container_width=True):
        rows = run_checks(urls_list, workers, timeout, follow, verify_ssl)
        results_table(rows)

if __name__ == "__main__":
    main()
