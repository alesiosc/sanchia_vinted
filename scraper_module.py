import sys, asyncio

# ─── Ensure ProactorEventLoop on Windows ───────────────────────────────────────
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import random
import requests
from playwright.async_api import async_playwright

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
]

async def get_auth_headers():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=random.choice(USER_AGENTS))
        page = await context.new_page()
        await page.goto("https://www.vinted.co.uk")
        await asyncio.sleep(2)
        cookies = await context.cookies()
        await browser.close()
        cookie_header = "; ".join(f"{c['name']}={c['value']}" for c in cookies)
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "application/json",
            "Cookie": cookie_header
        }

async def scrape_vinted_api(params: dict):
    headers = await get_auth_headers()
    response = requests.get(
        "https://www.vinted.co.uk/api/v2/catalog/items",
        params=params,
        headers=headers
    )
    if response.status_code == 200:
        return response.json()
    return {"error": f"Status {response.status_code}"}
