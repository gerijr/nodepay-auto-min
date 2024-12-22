import asyncio
import time
import uuid
import sys
from loguru import logger
from fake_useragent import UserAgent
from curl_cffi import requests
import concurrent.futures
import threading

# Constants
PING_INTERVAL = 0.5
RETRIES = 60

DOMAIN_API = {
    "SESSION": "http://api.nodepay.ai/api/auth/session",
    "PING": "https://nw.nodepay.org/api/network/ping"
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

print(f'==============================================')
print(f'Farming & Daily Claim Nodepay Multiple Account')
print(f'==============================================')

# Suppress 429 and 403 HTTP errors in logs using a custom filter
def filter_403_429(record):
    if "HTTP Error 429" in record["message"] or "HTTP Error 403" in record["message"]:
        return False
    return True

# Apply the filter to the logger
logger.remove()
logger.add(sys.stderr, level="INFO", filter=filter_403_429)

def dailyclaim(token):
    try:
        url = f"https://api.nodepay.org/api/mission/complete-mission?"
        headers = {
                "Authorization": f"Bearer {token}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                "Content-Type": "application/json",
                "Origin": "https://app.nodepay.ai",
                "Referer": "https://app.nodepay.ai/"
        }
        
        data = {
                "mission_id": "1"
        }
        
        response = requests.post(url, headers=headers, json=data, impersonate="chrome110")
        if response.json().get('success'):
            logger.info('Claim Reward Success!')
        else:
            logger.info('No reward claimed.')
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during claim request: {e}")

def uuidv4():
    return str(uuid.uuid4())

def valid_resp(resp):
    if not resp or "code" not in resp or resp["code"] < 0:
        raise ValueError("Invalid response")
    return resp

async def render_profile_info(token):
    global browser_id, account_info

    try:
        np_session_info = load_session_info()

        if not np_session_info:
            # Generate new browser_id
            browser_id = uuidv4()
            response = await call_api(DOMAIN_API["SESSION"], {}, token)
            valid_resp(response)
            account_info = response["data"]
            if account_info.get("uid"):
                save_session_info(account_info)
                await start_ping(token)
            else:
                handle_logout()
        else:
            account_info = np_session_info
            await start_ping(token)
    except Exception as e:
        logger.error(f"Error in render_profile_info: {e}")
        error_message = str(e)
        if any(phrase in error_message for phrase in [
            "sent 1011 (internal error) keepalive ping timeout; no close frame received",
            "500 Internal Server Error"
        ]):
            logger.info("Removing error account info due to invalid response.")
            handle_logout()
        else:
            logger.error(f"Connection error: {e}")

async def call_api(url, data, token):
    user_agent = UserAgent(os=['windows', 'macos', 'linux'], browsers='chrome')
    random_user_agent = user_agent.random
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": random_user_agent,
        "Content-Type": "application/json",
        "Origin": "chrome-extension://lgmpfmgeabnnlemejacfljbmonaomfmm",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
    }

    try:
        response = requests.post(url, json=data, headers=headers, impersonate="chrome110", timeout=30)
        response.raise_for_status()  # Will raise an exception for 4xx/5xx status codes
        return valid_resp(response.json())
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during API call to {url}: {e}")
        return {}
    except Exception as e:
        logger.error(f"Unexpected error during API call to {url}: {e}")
        return {}

async def start_ping(token):
    try:
        while True:
            await ping(token)
            await asyncio.sleep(PING_INTERVAL)
    except asyncio.CancelledError:
        logger.info(f"Ping task was cancelled")
    except Exception as e:
        logger.error(f"Error in start_ping: {e}")

async def ping(token):
    global last_ping_time, RETRIES, status_connect

    current_time = time.time()
    last_ping_time["last_ping_time"] = current_time

    try:
        data = {
            "id": account_info.get("uid"),
            "browser_id": browser_id,
            "timestamp": int(time.time()),
            "version": "2.2.7"
        }

        response = await call_api(DOMAIN_API["PING"], data, token)
        if response.get("code") == 0:
            logger.info(f"Connected: {response}")
            RETRIES = 0
            status_connect = CONNECTION_STATES["CONNECTED"]
            dailyclaim(token)
        else:
            handle_ping_fail(response)
    except Exception as e:
        logger.error(f"Ping failed: {e}")
        handle_ping_fail(None)

def handle_ping_fail(response):
    global RETRIES, status_connect

    RETRIES += 1
    if response and response.get("code") == 403:
        handle_logout()
    elif RETRIES < 2:
        status_connect = CONNECTION_STATES["DISCONNECTED"]
    else:
        status_connect = CONNECTION_STATES["DISCONNECTED"]

def handle_logout():
    global status_connect, account_info

    status_connect = CONNECTION_STATES["NONE_CONNECTION"]
    account_info = {}
    logger.info("Logged out and cleared session info.")

def save_session_info(data):
    # Implement saving session info (to file or database)
    pass

def load_session_info():
    return {}  # Simulated empty session

def render_profile_info_thread(token):
    asyncio.run(render_profile_info(token))

async def process_tokens(tokens):
    tasks = [render_profile_info(token) for token in tokens]
    await asyncio.gather(*tasks)

def read_tokens_from_file():
    try:
        with open('tokens.txt', 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logger.error("File tokens.txt not found.")
        exit()

def main():
    tokens = read_tokens_from_file()

    if not tokens:
        logger.error("No tokens found. Please add tokens to tokens.txt.")
        exit()

    asyncio.run(process_tokens(tokens))

if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Program terminated by user.")
