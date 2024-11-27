import threading
import time
import uuid
import random
import cloudscraper
from loguru import logger
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import ProxyError

def call_api(url, data, proxy, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://app.nodepay.ai",
    }

    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.post(url, json=data, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for 4xx/5xx responses
        return valid_resp(response.json())
    except ProxyError:
        # Silently ignore ProxyError, no logging or message shown
        return None
    except Exception:
        # Silently ignore all other errors and return None
        return None

# Constants
PING_INTERVAL = 1
RETRIES = 30

DOMAIN_API_ENDPOINTS = {
    "SESSION": ["http://api.nodepay.ai/api/auth/session"],
    "PING": [
        "http://13.215.134.222/api/network/ping",
        "http://18.139.20.49/api/network/ping",
        "http://18.142.29.174/api/network/ping",
        "http://18.142.214.13/api/network/ping",
        "http://52.74.31.107/api/network/ping",
        "http://52.74.35.173/api/network/ping",
        "http://52.77.10.116/api/network/ping"
    ]
}

CONNECTION_STATES = {
    "CONNECTED": 1,
    "DISCONNECTED": 2,
    "NONE_CONNECTION": 3
}

status_connect = CONNECTION_STATES["NONE_CONNECTION"]
browser_id = None
account_info = {}
last_ping_time = {}
def call_api(url, data, proxy, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://app.nodepay.ai",
    }

    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.post(url, json=data, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for 4xx/5xx responses
        return valid_resp(response.json())
    except Exception:
        # Suppress the error, do not log it, and return None
        return None
def render_profile_info(proxy, token):
    global browser_id, account_info

    try:
        np_session_info = load_session_info(proxy)
        if not np_session_info:
            browser_id = uuidv4()
            response = call_api(DOMAIN_API_ENDPOINTS["SESSION"][0], {}, proxy, token)
            if response is None:
                return proxy  # Skip this proxy without logging any error
            valid_resp(response)
            account_info = response["data"]
            if account_info.get("uid"):
                save_session_info(proxy, account_info)
                start_ping(proxy, token)
            else:
                handle_logout(proxy)
        else:
            account_info = np_session_info
            start_ping(proxy, token)
    except Exception:
        # Suppress the error without logging or printing any details
        return proxy  # Skip this proxy if there's an error
def start_ping(proxy, token):
    global last_ping_time, RETRIES, status_connect

    while True:
        current_time = time.time()
        if proxy in last_ping_time and (current_time - last_ping_time[proxy]) < PING_INTERVAL:
            time.sleep(PING_INTERVAL)
            continue

        last_ping_time[proxy] = current_time

        try:
            data = {
                "id": account_info.get("uid"),
                "browser_id": browser_id,
                "timestamp": int(time.time())
            }
            response = call_api(DOMAIN_API_ENDPOINTS["PING"][0], data, proxy, token)
            if response and response["code"] == 0:
                RETRIES = 0
                status_connect = CONNECTION_STATES["CONNECTED"]
            else:
                handle_ping_fail(proxy, response)
        except Exception:
            # No logging, just silently skip the proxy
            handle_ping_fail(proxy, None)

        time.sleep(PING_INTERVAL)

def get_random_endpoint(endpoint_type):
    return random.choice(DOMAIN_API_ENDPOINTS[endpoint_type])

def get_endpoint(endpoint_type):
    if endpoint_type not in DOMAIN_API_ENDPOINTS:
        raise ValueError(f"Unknown endpoint type: {endpoint_type}")
    return get_random_endpoint(endpoint_type)

def call_api(url, data, proxy, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://app.nodepay.ai",
    }

    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.post(url, json=data, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for 4xx/5xx responses
        return valid_resp(response.json())
    except Exception as e:
        logger.error(f"Error during API call to {url} with proxy {proxy}: {e}")
        return None
def call_api(url, data, proxy, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://app.nodepay.ai",
    }

    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.post(url, json=data, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for 4xx/5xx responses
        return valid_resp(response.json())
    except Exception:
        # Instead of logging the error, we simply suppress it by returning None
        return None

def valid_resp(resp):
    if not resp or "code" not in resp or resp["code"] < 0:
        raise ValueError("Invalid response")
    return resp

def uuidv4():
    return str(uuid.uuid4())

def handle_ping_fail(proxy, response):
    global RETRIES, status_connect
    RETRIES += 1
    if response and response.get("code") == 403:
        handle_logout(proxy)
    elif RETRIES < 2:
        status_connect = CONNECTION_STATES["DISCONNECTED"]
    else:
        status_connect = CONNECTION_STATES["DISCONNECTED"]

def handle_logout(proxy):
    global status_connect, account_info
    status_connect = CONNECTION_STATES["NONE_CONNECTION"]
    account_info = {}
    logger.info(f"Logged out and cleared session info for proxy {proxy}")

def start_ping(proxy, token):
    global last_ping_time, RETRIES, status_connect

    while True:
        current_time = time.time()
        if proxy in last_ping_time and (current_time - last_ping_time[proxy]) < PING_INTERVAL:
            logger.info(f"Skipping ping for proxy {proxy}, not enough time elapsed")
            time.sleep(PING_INTERVAL)
            continue

        last_ping_time[proxy] = current_time

        try:
            data = {
                "id": account_info.get("uid"),
                "browser_id": browser_id,
                "timestamp": int(time.time())
            }
            response = call_api(DOMAIN_API_ENDPOINTS["PING"][0], data, proxy, token)
            if response and response["code"] == 0:
                logger.info(f"Ping successful via proxy {proxy}: {response}")
                RETRIES = 0
                status_connect = CONNECTION_STATES["CONNECTED"]
            else:
                handle_ping_fail(proxy, response)
        except Exception as e:
            logger.error(f"Ping failed via proxy {proxy}: {e}")
            handle_ping_fail(proxy, None)

        time.sleep(PING_INTERVAL)

def render_profile_info(proxy, token):
    global browser_id, account_info

    try:
        np_session_info = load_session_info(proxy)
        if not np_session_info:
            browser_id = uuidv4()
            response = call_api(DOMAIN_API_ENDPOINTS["SESSION"][0], {}, proxy, token)
            if response is None:
                return proxy
            valid_resp(response)
            account_info = response["data"]
            if account_info.get("uid"):
                save_session_info(proxy, account_info)
                start_ping(proxy, token)
            else:
                handle_logout(proxy)
        else:
            account_info = np_session_info
            start_ping(proxy, token)
    except Exception as e:
        logger.debug(f"Error occurred for proxy {proxy}, continuing with next proxy.")
        return proxy

def load_proxies(proxy_file):
    try:
        with open(proxy_file, 'r') as file:
            proxies = file.read().splitlines()
        return proxies
    except Exception as e:
        logger.error(f"Failed to load proxies: {e}")
        raise SystemExit("Exiting due to failure in loading proxies")

def load_tokens(token_file):
    try:
        with open(token_file, 'r') as file:
            tokens = [line.strip() for line in file if line.strip()]
        return tokens
    except Exception as e:
        logger.error(f"Failed to load tokens: {e}")
        raise SystemExit("Exiting due to failure in loading tokens")

def load_session_info(proxy):
    return {}

def save_session_info(proxy, data):
    pass

def is_valid_proxy(proxy):
    return True

def run_for_token(token, all_proxies):
    with ThreadPoolExecutor(max_workers=100) as executor:
        active_proxies = [proxy for proxy in all_proxies if is_valid_proxy(proxy)][:1000]
        future_to_proxy = {executor.submit(render_profile_info, proxy, token): proxy for proxy in active_proxies}

        for future in future_to_proxy:
            try:
                result = future.result()
                if result is None:
                    failed_proxy = future_to_proxy[future]
                    logger.info(f"Removing and replacing failed proxy: {failed_proxy}")
            except Exception as exc:
                logger.error(f"Proxy execution generated an exception: {exc}")

def main():
    all_proxies = load_proxies('proxies.txt')
    tokens = load_tokens('token.txt')

    threads = []
    for token in tokens:
        thread = threading.Thread(target=run_for_token, args=(token, all_proxies))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
