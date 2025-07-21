import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import os

# Các API proxy miễn phí
PROXY_SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://www.proxyscan.io/api/proxy?type=http",
    "https://openproxy.space/list/http",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://multiproxy.org/txt_all/proxy.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt"
]

# Tên file lưu
OUTPUT_FILE = "proxy.txt"

def fetch_proxies():
    proxies = set()
    for url in PROXY_SOURCES:
        try:
            print(f"🔗 Lấy proxy từ: {url}")
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                for line in res.text.splitlines():
                    line = line.strip()
                    if line and ":" in line:
                        proxies.add(line)
        except Exception as e:
            print(f"⚠️ Lỗi lấy proxy từ {url}: {e}")
    return list(proxies)

def check_proxy(proxy):
    try:
        start = time.time()
        proxy_url = f"http://{proxy}"
        r = requests.get("http://httpbin.org/ip", proxies={"http": proxy_url, "https": proxy_url}, timeout=1)
        duration = (time.time() - start) * 1000
        if r.status_code == 200 and duration < 900:
            print(f"✔ {proxy} - {int(duration)}ms")
            save_proxy(proxy)
            return proxy
    except:
        pass
    print(f"✖ {proxy}")
    return None

# Lưu proxy hợp lệ ngay lập tức
def save_proxy(proxy):
    with open(OUTPUT_FILE, "a") as f:
        f.write(proxy + "\n")

def scan_proxies(proxy_list, max_workers=50):
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)  # Xoá file cũ nếu tồn tại

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_proxy, proxy): proxy for proxy in proxy_list}
        for future in as_completed(futures):
            future.result()

if __name__ == "__main__":
    print("🚀 Đang tải danh sách proxy...")
    all_proxies = fetch_proxies()
    print(f"🔎 Tổng số proxy lấy được: {len(all_proxies)}")

    print("⚙️ Đang kiểm tra proxy...")
    scan_proxies(all_proxies)

    print(f"\n💾 Đã lưu proxy hợp lệ vào: {OUTPUT_FILE}")
    