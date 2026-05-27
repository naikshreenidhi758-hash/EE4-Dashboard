from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
    headless=True,
    args=["--no-sandbox", "--disable-dev-shm-usage"]
)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://ee.envision-energy.com")
    print("Login manually using Okta...")
    input("Press ENTER after login completes...")
    context.storage_state(path="auth.json")
    print("Session saved!")
    browser.close()
